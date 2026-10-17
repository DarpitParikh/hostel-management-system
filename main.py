"""
HOSTEL MANAGEMENT SYSTEM  (Python + Tkinter)
=============================================
Login:  admin / admin123     or     warden / warden123

PYTHON CONCEPTS USED (for viva)
  Classes & objects ........ Student, Warden, Room, Visitor, Complaint, Hostel ...
  Inheritance .............. Student and Warden inherit from Person
  Abstract class ........... Person (abc.ABC, @abstractmethod get_role)
  Polymorphism ............. get_info() / get_role() behave differently in Student & Warden;
                             every tab overrides refresh()
  Encapsulation ............ private __fee_paid inside Student
  Class variable ........... Student.TOTAL_FEE
  Static method ............ Person.is_valid_phone()
  Dunder methods ........... __init__, __str__
  Custom exceptions ........ HostelError, RoomFullError, InvalidInputError
  List / dict / set-like ... rooms dict, students dict, visitors list, occupants list
  List comprehension ....... filtering and summary in Hostel
  Lambda + sort ............ Hostel.get_students()
  File handling ............ JSON (JsonStorage) and CSV (CsvExporter)
  datetime module .......... visitor time in / out, complaint date
  Tkinter .................. Frame, Notebook, Treeview, Combobox, messagebox, filedialog

SOLID PRINCIPLES (where to point in the viva)
  S - Single Responsibility : each class has ONE job
        Hostel = rules/logic, JsonStorage = saving, CsvExporter = CSV,
        Authenticator = login check, each Tab class = one screen.
  O - Open/Closed           : to add a new screen, write a new Tab class and add it to the
        list in HostelApp.build_tabs(); no existing tab is changed.
        To add a new kind of person, inherit from Person.
  L - Liskov Substitution   : a Student or a Warden can be used anywhere a Person is
        expected (get_info(), get_role(), __str__ work for both).
  I - Interface Segregation : small focused classes (storage only saves/loads, exporter only
        exports, authenticator only logs in). Nobody is forced to use methods it doesn't need.
  D - Dependency Inversion  : Hostel receives its storage from outside (Hostel(storage)) and
        Authenticator receives its users from outside, so they don't depend on a fixed file
        or a fixed user list.

FILES (read them in this order)
  exceptions.py     our own error classes
  models.py         Person, Student, Warden, Room, Visitor, Complaint
  storage.py        JsonStorage (save/load) and CsvExporter
  auth.py           Authenticator (login check)
  hostel.py         Hostel - all the rules / logic
  ui_helpers.py     colours, styling, table helpers
  base_tab.py       BaseTab - parent class of every tab
  student_tab.py, room_tab.py, warden_tab.py, visitor_tab.py, complaint_tab.py
  screens.py        LoginScreen and HostelApp (main window)
  main.py           this file - starts the program (run:  python main.py)
"""

import tkinter as tk
from storage import JsonStorage
from auth import Authenticator
from hostel import Hostel
from ui_helpers import setup_style
from screens import LoginScreen, HostelApp

DATA_FILE = "hostel_data.json"
USERS = {"admin": "admin123", "warden": "warden123"}


def main():
    root = tk.Tk()
    root.title("Hostel Management System")
    root.geometry("1100x720")
    root.minsize(950, 650)
    setup_style(root)

    hostel = Hostel(JsonStorage(DATA_FILE))
    hostel.load()
    authenticator = Authenticator(USERS)

    def show_login():
        LoginScreen(root, authenticator, show_app)

    def show_app(username):
        HostelApp(root, hostel, username, show_login)

    def on_close():
        hostel.save()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    show_login()
    root.mainloop()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
