"""The Hostel class: ALL business logic lives here (no GUI code)."""
from exceptions import InvalidInputError, RoomFullError
from models import Person, Student, Warden, Room, Visitor, Complaint, now_text


class Hostel:
    def __init__(self, storage):
        self.storage = storage               # given from outside (dependency inversion)
        self.rooms = {}                      # room_no -> Room
        self.students = {}                   # student_id -> Student
        self.wardens = {}                    # warden_id -> Warden
        self.visitors = []                   # list of Visitor
        self.complaints = []                 # list of Complaint
        self.next_student_id = 1
        self.next_warden_id = 1
        self.create_rooms()

    def create_rooms(self):
        for number in range(101, 106):       # 101-105 : 2 beds
            self.rooms[number] = Room(number, 2)
        for number in range(201, 206):       # 201-205 : 3 beds
            self.rooms[number] = Room(number, 3)

    # ---------- students ----------
    def get_student(self, student_id):
        if student_id not in self.students:
            raise InvalidInputError("Student not found")
        return self.students[student_id]

    def student_name(self, student_id):
        student = self.students.get(student_id)
        return student.name if student else "(left hostel)"

    def add_student(self, name, phone, course, room_no):
        if name == "" or course == "":
            raise InvalidInputError("Name and course cannot be empty")
        if not Person.is_valid_phone(phone):
            raise InvalidInputError("Phone must be exactly 10 digits")
        if room_no not in self.rooms:
            raise InvalidInputError("Room does not exist")
        if self.rooms[room_no].is_full():
            raise RoomFullError(f"Room {room_no} is full")

        student = Student(self.next_student_id, name, phone, course, room_no)
        self.students[student.student_id] = student
        self.rooms[room_no].occupants.append(student.student_id)
        self.next_student_id += 1

    def remove_student(self, student_id):
        student = self.get_student(student_id)
        self.rooms[student.room_no].occupants.remove(student_id)
        del self.students[student_id]

    def pay_fee(self, student_id, amount):
        self.get_student(student_id).pay_fee(amount)

    def get_students(self, text="", sort_by="ID", only_dues=False):
        result = [s for s in self.students.values() if text.lower() in s.name.lower()]
        if only_dues:
            result = [s for s in result if s.get_fee_due() > 0]
        if sort_by == "Name":
            result.sort(key=lambda s: s.name.lower())
        elif sort_by == "Fee Due":
            result.sort(key=lambda s: s.get_fee_due(), reverse=True)
        return result

    def available_rooms(self):
        return [no for no, room in self.rooms.items() if not room.is_full()]

    # ---------- wardens ----------
    def add_warden(self, name, phone, block):
        if name == "" or block == "":
            raise InvalidInputError("Name and block cannot be empty")
        if not Person.is_valid_phone(phone):
            raise InvalidInputError("Phone must be exactly 10 digits")
        warden = Warden(self.next_warden_id, name, phone, block)
        self.wardens[warden.warden_id] = warden
        self.next_warden_id += 1

    def remove_warden(self, warden_id):
        if warden_id not in self.wardens:
            raise InvalidInputError("Warden not found")
        del self.wardens[warden_id]

    # ---------- visitors ----------
    def add_visitor(self, student_id, visitor_name):
        self.get_student(student_id)
        if visitor_name == "":
            raise InvalidInputError("Visitor name cannot be empty")
        self.visitors.append(Visitor(student_id, visitor_name, now_text()))

    def mark_visitor_out(self, index):
        if index < 0 or index >= len(self.visitors):
            raise InvalidInputError("Visitor not found")
        if self.visitors[index].time_out != "":
            raise InvalidInputError("Visitor is already marked out")
        self.visitors[index].time_out = now_text()

    # ---------- complaints ----------
    def add_complaint(self, student_id, text):
        self.get_student(student_id)
        if text == "":
            raise InvalidInputError("Complaint cannot be empty")
        self.complaints.append(Complaint(student_id, text, now_text()))

    def resolve_complaint(self, index):
        if index < 0 or index >= len(self.complaints):
            raise InvalidInputError("Complaint not found")
        self.complaints[index].status = "Resolved"

    # ---------- dashboard numbers ----------
    def get_summary(self):
        total_beds = sum(room.capacity for room in self.rooms.values())
        used_beds = sum(len(room.occupants) for room in self.rooms.values())
        return {
            "Students": len(self.students),
            "Vacant Beds": total_beds - used_beds,
            "Fees Collected": sum(s.get_fee_paid() for s in self.students.values()),
            "Fees Pending": sum(s.get_fee_due() for s in self.students.values()),
            "Open Complaints": len([c for c in self.complaints if c.status == "Open"]),
        }

    # ---------- save / load ----------
    def save(self):
        data = {
            "next_student_id": self.next_student_id,
            "next_warden_id": self.next_warden_id,
            "students": [s.to_dict() for s in self.students.values()],
            "wardens": [w.to_dict() for w in self.wardens.values()],
            "visitors": [v.to_dict() for v in self.visitors],
            "complaints": [c.to_dict() for c in self.complaints],
        }
        self.storage.save(data)

    def load(self):
        data = self.storage.load()
        if data is None:
            return
        self.next_student_id = data["next_student_id"]
        self.next_warden_id = data["next_warden_id"]
        for item in data["students"]:
            student = Student(item["student_id"], item["name"], item["phone"],
                              item["course"], item["room_no"], item["fee_paid"])
            self.students[student.student_id] = student
            self.rooms[student.room_no].occupants.append(student.student_id)
        for item in data["wardens"]:
            self.wardens[item["warden_id"]] = Warden(**item)     # ** unpacks the dictionary
        self.visitors = [Visitor(**item) for item in data["visitors"]]
        self.complaints = [Complaint(**item) for item in data["complaints"]]
