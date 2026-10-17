"""BaseTab: the parent class of every tab. Holds helpers they all share."""
from tkinter import ttk, messagebox
from exceptions import HostelError, InvalidInputError


class BaseTab(ttk.Frame):
    def __init__(self, parent, hostel, on_change):
        super().__init__(parent, padding=10)
        self.hostel = hostel
        self.on_change = on_change           # function to refresh the whole window
        self.build()

    def build(self):
        """Child classes draw their widgets here."""

    def refresh(self):
        """Child classes reload their data here."""

    # ----- helpers shared by all tabs -----
    def run(self, action, success_message=""):
        """Runs an action, shows any HostelError as a pop-up, then refreshes the window."""
        try:
            action()
        except HostelError as error:
            messagebox.showerror("Error", str(error))
            return
        if success_message:
            messagebox.showinfo("Success", success_message)
        self.on_change()

    def selected_number(self, table):
        selected = table.selection()
        if not selected:
            raise InvalidInputError("Please select a row in the table first")
        return int(table.item(selected[0])["values"][0])

    def to_number(self, text, label):
        if not text.strip().isdigit():
            raise InvalidInputError(f"{label} is required and must be a number")
        return int(text)

    def student_choices(self):
        return [f"{s.student_id} - {s.name}" for s in self.hostel.students.values()]

    def choice_to_id(self, text):
        if text == "":
            raise InvalidInputError("Please select a student")
        return int(text.split(" - ")[0])

    def add_field(self, form, label, variable, column, width=16):
        ttk.Label(form, text=label).grid(row=0, column=column * 2, padx=5, pady=5, sticky="e")
        ttk.Entry(form, textvariable=variable, width=width).grid(row=0, column=column * 2 + 1)
