# Hostel Management System

A desktop app made with Python and Tkinter. It manages students, rooms, wardens, visitors, complaints and fees.

## Run
```
python main.py
```
Needs Python 3.8+ (Tkinter comes with it). No other installs.

**Login:** `admin / admin123` or `warden / warden123`

## Features
- Login screen with logout
- Dashboard: students, vacant beds, fees collected and pending, open complaints
- Students: add, search, sort, filter by fee due, pay fee, check out, export CSV
- Rooms, Wardens, Visitors (check in/out) and Complaints (open/resolved)
- Data saved automatically to `hostel_data.json` when the window is closed

## Files
| File | Purpose |
|---|---|
| `main.py` | Starts the program |
| `models.py` | Person (abstract), Student, Warden, Room, Visitor, Complaint |
| `hostel.py` | All the logic (no GUI code) |
| `storage.py` | JSON save/load and CSV export |
| `auth.py` | Login check |
| `exceptions.py` | Custom errors |
| `ui_helpers.py`, `base_tab.py` | Styling and shared tab code |
| `*_tab.py` | One file per tab |
| `screens.py` | Login screen and main window |

## Concepts used
Classes, inheritance, abstract class, polymorphism, encapsulation, custom exceptions, file handling (JSON/CSV), `datetime`, lambda, list comprehensions, and the SOLID principles (listed in the top comment of `main.py`).

To start with fresh data, delete `hostel_data.json`.
