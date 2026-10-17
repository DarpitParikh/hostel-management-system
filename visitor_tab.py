"""Visitors tab: check visitors in and out."""
import tkinter as tk
from tkinter import ttk
from base_tab import BaseTab
from ui_helpers import make_table, fill_table


class VisitorTab(BaseTab):
    def build(self):
        self.student_var = tk.StringVar()
        self.visitor_var = tk.StringVar()

        form = ttk.LabelFrame(self, text=" New Visitor ", padding=8)
        form.pack(fill="x")
        ttk.Label(form, text="Visiting student").grid(row=0, column=0, padx=5, pady=5)
        self.student_box = ttk.Combobox(form, textvariable=self.student_var,
                                        state="readonly", width=22)
        self.student_box.grid(row=0, column=1)
        self.add_field(form, "Visitor name", self.visitor_var, 1, width=20)
        ttk.Button(form, text="Check In", command=self.add_visitor).grid(row=0, column=4, padx=10)

        frame, self.table = make_table(self, ("No", "Student", "Visitor", "Time In", "Time Out"),
                                       height=12)
        frame.pack(fill="both", expand=True, pady=8)
        ttk.Button(self, text="Mark Selected Visitor Out", command=self.mark_out).pack(anchor="w")

    def refresh(self):
        self.student_box["values"] = self.student_choices()
        rows = []
        for number, v in enumerate(self.hostel.visitors, start=1):
            rows.append((number, self.hostel.student_name(v.student_id), v.name,
                         v.time_in, v.time_out or "Inside"))
        fill_table(self.table, rows)

    def add_visitor(self):
        def action():
            student_id = self.choice_to_id(self.student_var.get())
            self.hostel.add_visitor(student_id, self.visitor_var.get().strip())
            self.visitor_var.set("")
        self.run(action, "Visitor checked in")

    def mark_out(self):
        self.run(lambda: self.hostel.mark_visitor_out(self.selected_number(self.table) - 1))
