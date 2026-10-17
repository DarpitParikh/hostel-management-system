"""Wardens tab: add / remove wardens."""
import tkinter as tk
from tkinter import ttk, messagebox
from base_tab import BaseTab
from ui_helpers import make_table, fill_table


class WardenTab(BaseTab):
    def build(self):
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.block_var = tk.StringVar()

        form = ttk.LabelFrame(self, text=" Add Warden ", padding=8)
        form.pack(fill="x")
        self.add_field(form, "Name", self.name_var, 0)
        self.add_field(form, "Phone", self.phone_var, 1)
        self.add_field(form, "Block", self.block_var, 2, width=8)
        ttk.Button(form, text="Add Warden", command=self.add_warden).grid(row=0, column=6, padx=10)

        frame, self.table = make_table(self, ("ID", "Name", "Phone", "Block", "Role"), height=12)
        frame.pack(fill="both", expand=True, pady=8)

        actions = ttk.Frame(self)
        actions.pack(fill="x")
        ttk.Button(actions, text="Show Info", command=self.show_info).pack(side="left")
        ttk.Button(actions, text="Remove Warden", style="Danger.TButton",
                   command=self.remove_warden).pack(side="left", padx=8)

    def refresh(self):
        rows = [(w.warden_id, w.name, w.phone, w.block, w.get_role())
                for w in self.hostel.wardens.values()]
        fill_table(self.table, rows)

    def add_warden(self):
        def action():
            self.hostel.add_warden(self.name_var.get().strip(), self.phone_var.get().strip(),
                                   self.block_var.get().strip())
            for variable in (self.name_var, self.phone_var, self.block_var):
                variable.set("")
        self.run(action, "Warden added")

    def show_info(self):
        def action():
            warden_id = self.selected_number(self.table)
            warden = self.hostel.wardens[warden_id]
            messagebox.showinfo(warden.get_role(), warden.get_info())     # polymorphism
        self.run(action)

    def remove_warden(self):
        self.run(lambda: self.hostel.remove_warden(self.selected_number(self.table)))
