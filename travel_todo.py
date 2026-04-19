"""
Travel Todo App - Manage your travel tasks and check flight status.

Usage:
  python travel_todo.py <command> [arguments]

Commands:
  list                 List all todos
  add <description>    Add a new todo
  complete <id>        Mark a todo as completed
  delete <id>          Delete a todo
  flight <number>      Check flight status
  help                 Show this help message
"""

import json
import os
import sys
from datetime import datetime

TODOS_FILE = "todos.json"

# Simulated flight status database
FLIGHTS = {
    "AA100": {"airline": "American Airlines", "from": "JFK", "to": "LAX", "departure": "08:00", "arrival": "11:30", "status": "On Time"},
    "UA200": {"airline": "United Airlines",   "from": "ORD", "to": "SFO", "departure": "10:15", "arrival": "13:45", "status": "Delayed - 45 min"},
    "DL300": {"airline": "Delta Airlines",    "from": "ATL", "to": "MIA", "departure": "14:30", "arrival": "16:00", "status": "On Time"},
    "SW400": {"airline": "Southwest",         "from": "DAL", "to": "DEN", "departure": "09:00", "arrival": "11:15", "status": "Boarding"},
    "BA500": {"airline": "British Airways",   "from": "LHR", "to": "JFK", "departure": "11:00", "arrival": "14:30", "status": "On Time"},
}


def load_todos():
    if os.path.exists(TODOS_FILE):
        with open(TODOS_FILE, "r") as f:
            return json.load(f)
    return []


def save_todos(todos):
    with open(TODOS_FILE, "w") as f:
        json.dump(todos, f, indent=2)


def cmd_add(args):
    if not args:
        print("Error: Please provide a description.")
        print("  Usage: python travel_todo.py add <description>")
        return
    todos = load_todos()
    # Auto-increment id based on max existing id
    next_id = max((t["id"] for t in todos), default=0) + 1
    todo = {
        "id": next_id,
        "description": " ".join(args),
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    todos.append(todo)
    save_todos(todos)
    print(f"Added  #{todo['id']}: {todo['description']}")


def cmd_list(_args):
    todos = load_todos()
    if not todos:
        print("Your todo list is empty.")
        print("  Add one: python travel_todo.py add \"Pack luggage\"")
        return
    print("\n Travel Todo List")
    print(" " + "-" * 40)
    for todo in todos:
        mark = "x" if todo["completed"] else " "
        print(f"  [{mark}] #{todo['id']:>2} - {todo['description']}")
    print(" " + "-" * 40)
    done = sum(1 for t in todos if t["completed"])
    print(f"  {done}/{len(todos)} completed\n")


def cmd_complete(args):
    if not args:
        print("Error: Please provide a todo ID.")
        return
    try:
        todo_id = int(args[0])
    except ValueError:
        print("Error: ID must be a number.")
        return
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            if todo["completed"]:
                print(f"Todo #{todo_id} is already completed.")
            else:
                todo["completed"] = True
                save_todos(todos)
                print(f"Done   #{todo_id}: {todo['description']}")
            return
    print(f"Todo #{todo_id} not found.")


def cmd_delete(args):
    if not args:
        print("Error: Please provide a todo ID.")
        return
    try:
        todo_id = int(args[0])
    except ValueError:
        print("Error: ID must be a number.")
        return
    todos = load_todos()
    filtered = [t for t in todos if t["id"] != todo_id]
    if len(filtered) == len(todos):
        print(f"Todo #{todo_id} not found.")
    else:
        save_todos(filtered)
        print(f"Deleted #{todo_id}")


def cmd_flight(args):
    if not args:
        print("Error: Please provide a flight number.")
        print(f"  Available: {', '.join(FLIGHTS)}")
        return
    code = args[0].upper()
    if code not in FLIGHTS:
        print(f"Flight {code} not found.")
        print(f"  Available: {', '.join(FLIGHTS)}")
        return
    f = FLIGHTS[code]
    print(f"\n Flight Status: {code}")
    print(f"  Airline  : {f['airline']}")
    print(f"  Route    : {f['from']} -> {f['to']}")
    print(f"  Departure: {f['departure']}")
    print(f"  Arrival  : {f['arrival']}")
    print(f"  Status   : {f['status']}\n")


def cmd_help(_args):
    print(__doc__)


COMMANDS = {
    "add":      cmd_add,
    "list":     cmd_list,
    "complete": cmd_complete,
    "delete":   cmd_delete,
    "flight":   cmd_flight,
    "help":     cmd_help,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        cmd_help([])
        return
    command = sys.argv[1]
    COMMANDS[command](sys.argv[2:])


if __name__ == "__main__":
    main()
