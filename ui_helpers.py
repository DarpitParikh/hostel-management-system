"""Colours, ttk styling and table helper functions shared by all screens."""
from tkinter import ttk

# colours used by the GUI
BG = "#f4f6fb"
PRIMARY = "#243b7a"
ACCENT = "#3b82f6"
DANGER = "#dc2626"
MUTED = "#6b7280"
BORDER = "#d5dbea"
STRIPE = "#eef2fb"


def setup_style(root):
    root.configure(bg=BG)
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TFrame", background=BG)
    style.configure("TLabel", background=BG, font=("Arial", 10))
    style.configure("TLabelframe", background=BG, bordercolor=BORDER)
    style.configure("TLabelframe.Label", background=BG, foreground=PRIMARY,
                    font=("Arial", 10, "bold"))
    style.configure("TCheckbutton", background=BG, font=("Arial", 10))
    style.configure("TButton", background=ACCENT, foreground="white",
                    font=("Arial", 10, "bold"), padding=6, borderwidth=0)
    style.map("TButton", background=[("active", "#2563eb")])
    style.configure("Danger.TButton", background=DANGER)
    style.map("Danger.TButton", background=[("active", "#b91c1c")])
    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab", padding=(18, 8), font=("Arial", 10, "bold"))
    style.map("TNotebook.Tab", background=[("selected", PRIMARY)],
              foreground=[("selected", "white")])
    style.configure("Treeview", rowheight=26, font=("Arial", 10), fieldbackground="white")
    style.configure("Treeview.Heading", background=PRIMARY, foreground="white",
                    font=("Arial", 10, "bold"))
    style.map("Treeview", background=[("selected", ACCENT)])


def make_table(parent, columns, height=10):
    """Creates a table with a scrollbar. Returns (frame_to_pack, table)."""
    frame = ttk.Frame(parent)
    table = ttk.Treeview(frame, columns=columns, show="headings", height=height)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=110, anchor="center")
    table.tag_configure("odd", background=STRIPE)
    table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return frame, table


def fill_table(table, rows):
    selected = [table.item(item)["values"][0] for item in table.selection()]
    table.delete(*table.get_children())
    for number, row in enumerate(rows):
        tag = "odd" if number % 2 == 1 else ""      # alternate row colours
        item = table.insert("", "end", values=row, tags=(tag,))
        if row[0] in selected:                      # keep the same row selected
            table.selection_add(item)
