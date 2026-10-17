"""File handling: JSON for saving data, CSV for exporting students."""
import csv
import json


class JsonStorage:
    """Only saves / loads a dictionary to a JSON file."""

    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def load(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return None                      # first run or broken file


class CsvExporter:
    """Only writes students to a CSV file."""

    def export(self, filename, students):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Phone", "Course", "Room", "Fee Paid", "Fee Due"])
            for s in students:
                writer.writerow([s.student_id, s.name, s.phone, s.course,
                                 s.room_no, s.get_fee_paid(), s.get_fee_due()])
