"""The two main screens: LoginScreen and HostelApp (header + dashboard + tabs)."""
import tkinter as tk
from tkinter import ttk
from ui_helpers import PRIMARY, ACCENT, DANGER, BORDER, MUTED
from student_tab import StudentTab
from room_tab import RoomTab
from warden_tab import WardenTab
from visitor_tab import VisitorTab
from complaint_tab import ComplaintTab


class LoginScreen(ttk.Frame):
    def __init__(self, root, authenticator, on_success):
        super().__init__(root)
        self.pack(fill="both", expand=True)
        self.authenticator = authenticator
        self.on_success = on_success
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.show_var = tk.BooleanVar(value=False)

        # one white card, split into a blue left panel and a form on the right
        card = tk.Frame(self, bg="white", highlightbackground=BORDER, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center")
        self.build_left_panel(card)
        self.build_form(card)
        self.username_entry.focus()

    def build_left_panel(self, card):
        panel = tk.Frame(card, bg=PRIMARY, width=300, height=420)
        panel.pack(side="left", fill="y")
        panel.pack_propagate(False)                     # keep the fixed size
        tk.Label(panel, text="HMS", bg=PRIMARY, fg="white",
                 font=("Arial", 40, "bold")).pack(pady=(110, 0))
        tk.Label(panel, text="Hostel Management\nSystem", bg=PRIMARY, fg="white",
                 font=("Arial", 15, "bold")).pack()
        tk.Label(panel, text="Rooms  |  Students  |  Fees", bg=PRIMARY, fg="#c7d2fe",
                 font=("Arial", 10)).pack(pady=(15, 0))

    def build_form(self, card):
        form = tk.Frame(card, bg="white")
        form.pack(side="left", padx=45, pady=40)

        tk.Label(form, text="Welcome back", bg="white", fg=PRIMARY,
                 font=("Arial", 20, "bold")).pack(anchor="w")
        tk.Label(form, text="Log in to your account", bg="white", fg=MUTED,
                 font=("Arial", 10)).pack(anchor="w", pady=(0, 20))

        tk.Label(form, text="Username", bg="white", fg=MUTED).pack(anchor="w")
        self.username_entry = self.make_entry(form, self.username_var)
        tk.Label(form, text="Password", bg="white", fg=MUTED).pack(anchor="w")
        self.password_entry = self.make_entry(form, self.password_var, show="*")

        tk.Checkbutton(form, text="Show password", variable=self.show_var, bg="white",
                       activebackground="white", fg=MUTED, command=self.toggle_password
                       ).pack(anchor="w")

        self.error_label = tk.Label(form, text="", bg="white", fg=DANGER, font=("Arial", 9))
        self.error_label.pack(anchor="w", pady=(8, 0))

        ttk.Button(form, text="Login", command=self.login).pack(fill="x", ipady=4, pady=(5, 0))
        tk.Label(form, text="Demo:  admin / admin123", bg="white", fg=MUTED,
                 font=("Arial", 9)).pack(pady=(15, 0))

    def make_entry(self, parent, variable, show=""):
        """A flat entry box whose border turns blue when you click inside it."""
        entry = tk.Entry(parent, textvariable=variable, show=show, width=28, font=("Arial", 11),
                         relief="flat", highlightthickness=1,
                         highlightbackground=BORDER, highlightcolor=ACCENT)
        entry.pack(ipady=6, pady=(2, 12))
        entry.bind("<Return>", lambda event: self.login())    # Enter key also logs in
        return entry

    def toggle_password(self):
        self.password_entry.config(show="" if self.show_var.get() else "*")

    def login(self):
        username = self.username_var.get().strip()
        if self.authenticator.login(username, self.password_var.get()):
            self.destroy()
            self.on_success(username)
        else:
            self.error_label.config(text="Wrong username or password")
            self.password_var.set("")
            self.password_entry.focus()
class HostelApp(ttk.Frame):
    def __init__(self, root, hostel, username, on_logout):
        super().__init__(root)
        self.pack(fill="both", expand=True)
        self.hostel = hostel
        self.on_logout = on_logout
        self.build_header(username)
        self.build_cards()
        self.build_tabs()
        self.refresh_all()

    def build_header(self, username):
        header = tk.Frame(self, bg=PRIMARY)
        header.pack(fill="x")
        tk.Label(header, text="Hostel Management System", bg=PRIMARY, fg="white",
                 font=("Arial", 16, "bold")).pack(side="left", padx=15, pady=12)
        ttk.Button(header, text="Logout", style="Danger.TButton",
                   command=self.logout).pack(side="right", padx=15)
        tk.Label(header, text="Logged in as " + username, bg=PRIMARY, fg="#c7d2fe",
                 font=("Arial", 10)).pack(side="right")

    def build_cards(self):
        """Dashboard: one small card per number."""
        self.cards = {}
        row = ttk.Frame(self)
        row.pack(fill="x", padx=12, pady=10)
        for title in self.hostel.get_summary():
            card = tk.Frame(row, bg="white", highlightbackground=BORDER, highlightthickness=1)
            card.pack(side="left", expand=True, fill="x", padx=5)
            value = tk.Label(card, text="0", bg="white", fg=PRIMARY, font=("Arial", 18, "bold"))
            value.pack(pady=(8, 0))
            tk.Label(card, text=title, bg="white", fg=MUTED, font=("Arial", 9)).pack(pady=(0, 8))
            self.cards[title] = value

    def build_tabs(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        # to add a new screen, just add one line here (open/closed principle)
        tab_list = [("Students", StudentTab), ("Rooms", RoomTab), ("Wardens", WardenTab),
                    ("Visitors", VisitorTab), ("Complaints", ComplaintTab)]
        self.tabs = []
        for title, tab_class in tab_list:
            tab = tab_class(notebook, self.hostel, self.refresh_all)
            notebook.add(tab, text=title)
            self.tabs.append(tab)

    def refresh_all(self):
        for title, number in self.hostel.get_summary().items():
            text = f"Rs {number}" if "Fees" in title else str(number)
            self.cards[title].config(text=text)
        for tab in self.tabs:
            tab.refresh()                    # same call, every tab does its own thing

    def logout(self):
        self.destroy()
        self.on_logout()
