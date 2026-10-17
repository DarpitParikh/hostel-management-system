"""Rooms tab: shows capacity, vacancies and who lives in each room."""
from base_tab import BaseTab
from ui_helpers import make_table, fill_table


class RoomTab(BaseTab):
    def build(self):
        columns = ("Room", "Capacity", "Occupied", "Vacant", "Students")
        frame, self.table = make_table(self, columns, height=14)
        self.table.column("Students", width=350)
        frame.pack(fill="both", expand=True)

    def refresh(self):
        rows = []
        for room in self.hostel.rooms.values():
            names = ", ".join(self.hostel.student_name(i) for i in room.occupants)
            rows.append((room.room_no, room.capacity, len(room.occupants),
                         room.vacancies(), names))
        fill_table(self.table, rows)
