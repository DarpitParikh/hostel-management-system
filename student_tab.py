"""Students tab: add, search, sort, filter, pay fee, check out, export CSV."""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from base_tab import BaseTab
from ui_helpers import make_table, fill_table
from storage import CsvExporter


class StudentTab(BaseTab):
    def build(self):
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.course_var = tk.StringVar()
        self.room_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.sort_var = tk.StringVar(value="ID")
        self.dues_var = tk.BooleanVar(value=False)
        self.fee_var = tk.StringVar()

        # --- add student form ---
        form = ttk.LabelFrame(self, text=" Add Student ", padding=8)
        form.pack(fill="x")
        self.add_field(form, "Name", self.name_var, 0)
        self.add_field(form, "Phone", self.phone_var, 1)
        self.add_field(form, "Course", self.course_var, 2)
        ttk.Label(form, text="Room").grid(row=0, column=6, padx=5, sticky="e")
        self.room_box = ttk.Combobox(form, textvariable=self.room_var, state="readonly", width=7)
        self.room_box.grid(row=0, column=7)
        ttk.Button(form, text="Add Student", command=self.add_student).grid(row=0, column=8, padx=10)

        # --- search / sort / filter bar ---
        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=8)
        ttk.Label(bar, text="Search name:").pack(side="left")
        ttk.Entry(bar, textvariable=self.search_var, width=18).pack(side="left", padx=5)
        ttk.Label(bar, text="Sort by:").pack(side="left", padx=(15, 0))
        sort_box = ttk.Combobox(bar, textvariable=self.sort_var, state="readonly", width=9,
                                values=["ID", "Name", "Fee Due"])
        sort_box.pack(side="left", padx=5)
        ttk.Checkbutton(bar, text="Only students with fee due", variable=self.dues_var,
                        command=self.refresh).pack(side="left", padx=15)

        # --- table ---
        columns = ("ID", "Name", "Phone", "Course", "Room", "Fee Paid", "Fee Due")
        frame, self.table = make_table(self, columns)
        frame.pack(fill="both", expand=True)

        # --- buttons for the selected student ---
        actions = ttk.LabelFrame(self, text=" Selected student ", padding=8)
        actions.pack(fill="x", pady=(8, 0))
        ttk.Label(actions, text="Fee amount").pack(side="left", padx=5)
        ttk.Entry(actions, textvariable=self.fee_var, width=12).pack(side="left")
        ttk.Button(actions, text="Pay Fee", command=self.pay_fee).pack(side="left", padx=8)
        ttk.Button(actions, text="Show Info", command=self.show_info).pack(side="left")
        ttk.Button(actions, text="Check Out", style="Danger.TButton",
                   command=self.remove_student).pack(side="left", padx=8)
        ttk.Button(actions, text="Export CSV", command=self.export_csv).pack(side="right")

        # refresh the table when search / sort changes
        self.search_var.trace_add("write", lambda *args: self.refresh())
        sort_box.bind("<<ComboboxSelected>>", lambda event: self.refresh())

    def refresh(self):
        students = self.hostel.get_students(self.search_var.get(), self.sort_var.get(),
                                            self.dues_var.get())
        rows = [(s.student_id, s.name, s.phone, s.course, s.room_no,
                 s.get_fee_paid(), s.get_fee_due()) for s in students]
        fill_table(self.table, rows)
        self.room_box["values"] = self.hostel.available_rooms()

    def add_student(self):
        def action():
            room_no = self.to_number(self.room_var.get(), "Room")
            self.hostel.add_student(self.name_var.get().strip(), self.phone_var.get().strip(),
                                    self.course_var.get().strip(), room_no)
            for variable in (self.name_var, self.phone_var, self.course_var, self.room_var):
                variable.set("")
        self.run(action, "Student added")

    def pay_fee(self):
        def action():
            student_id = self.selected_number(self.table)
            amount = self.to_number(self.fee_var.get(), "Fee amount")
            self.hostel.pay_fee(student_id, amount)
            self.fee_var.set("")
        self.run(action, "Fee updated")

    def show_info(self):
        def action():
            student = self.hostel.get_student(self.selected_number(self.table))
            messagebox.showinfo(student.get_role(), student.get_info())   # polymorphism
        self.run(action)

    def remove_student(self):
        def action():
            student_id = self.selected_number(self.table)
            if messagebox.askyesno("Confirm", "Check out this student?"):
                self.hostel.remove_student(student_id)
        self.run(action)

    def export_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV file", "*.csv")])
        if filename == "":
            return                                    # user pressed cancel
        students = self.hostel.get_students(self.search_var.get(), self.sort_var.get(),
                                            self.dues_var.get())
        CsvExporter().export(filename, students)
        messagebox.showinfo("Exported", "Students saved to " + filename)
