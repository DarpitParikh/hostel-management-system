"""Complaints tab: register complaints and mark them resolved."""
import tkinter as tk
from tkinter import ttk
from base_tab import BaseTab
from ui_helpers import make_table, fill_table


class ComplaintTab(BaseTab):
    def build(self):
        self.student_var = tk.StringVar()
        self.text_var = tk.StringVar()

        form = ttk.LabelFrame(self, text=" New Complaint ", padding=8)
        form.pack(fill="x")
        ttk.Label(form, text="Student").grid(row=0, column=0, padx=5, pady=5)
        self.student_box = ttk.Combobox(form, textvariable=self.student_var,
                                        state="readonly", width=22)
        self.student_box.grid(row=0, column=1)
        self.add_field(form, "Complaint", self.text_var, 1, width=34)
        ttk.Button(form, text="Submit", command=self.add_complaint).grid(row=0, column=4, padx=10)

        frame, self.table = make_table(self, ("No", "Student", "Complaint", "Date", "Status"),
                                       height=12)
        self.table.column("Complaint", width=260)
        frame.pack(fill="both", expand=True, pady=8)
        ttk.Button(self, text="Mark Selected as Resolved", command=self.resolve).pack(anchor="w")

    def refresh(self):
        self.student_box["values"] = self.student_choices()
        rows = []
        for number, c in enumerate(self.hostel.complaints, start=1):
            rows.append((number, self.hostel.student_name(c.student_id), c.text, c.date, c.status))
        fill_table(self.table, rows)

    def add_complaint(self):
        def action():
            student_id = self.choice_to_id(self.student_var.get())
            self.hostel.add_complaint(student_id, self.text_var.get().strip())
            self.text_var.set("")
        self.run(action, "Complaint submitted")

    def resolve(self):
        self.run(lambda: self.hostel.resolve_complaint(self.selected_number(self.table) - 1))
