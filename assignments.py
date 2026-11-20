# assignments.py
from config import data, XP_ASSIGN_PART, XP_ASSIGN_KILL
from utils import (
    header, get_int, get_text, get_date, hp_bar, deadline_text,
    GREEN, YELLOW, RED, RESET
)
from profile import award_xp

# view assignment 
def view_assignments():
    header("ASSIGNMENTS (MINI-BOSSES)")
    if not data["assignments"]:
        print("  No mini-bosses yet. Add one from the menu.")
        return
    for i, a in enumerate(data["assignments"], 1):
        total = int(a["total_parts"])
        done = int(a["done_parts"])
        left = total - done
        print(YELLOW + f"{i}. {a['name']}" + RESET + f"  ({a['subject']})")
        if left == 0:
            print("   " + GREEN + "DEFEATED!" + RESET)
        else:
            print(f"   HP {hp_bar(left, total)} {left}/{total}   {deadline_text(a['deadline'])}")

#add assignment
def add_assignment():
    header("ADD NEW ASSIGNMENT")
    name = get_text("Assignment name: ")
    subject = get_text("Subject: ")
    deadline = get_date("Deadline (DD-MM-YYYY): ")
    parts = get_int("Number of parts / tasks (1-20): ", 1, 20)
    data["assignments"].append({
        "name": name, "subject": subject, "deadline": deadline.isoformat(),
        "total_parts": str(parts), "done_parts": "0"
    })
    print(GREEN + f"  A new mini-boss appeared: {name}" + RESET)

##remove assignment
def remove_assignment():
    header("REMOVE ASSIGNMENT")
    if not data["assignments"]:
        print("  No assignments to remove.")
        return
    for i, a in enumerate(data["assignments"], 1):
        print(f"  {GREEN}{i}.{RESET} {a['name']} ({a['subject']})")
    print(f"  {GREEN}0.{RESET} Back")
    choice = get_int("Choose assignment to remove: ", 0, len(data["assignments"]))
    if choice == 0:
        return
    removed = data["assignments"].pop(choice - 1)
    print(RED + f"  Removed mini-boss: {removed['name']}" + RESET)

#to work on assignment
def work_on_assignment():
    header("WORK ON ASSIGNMENT")
    active = [a for a in data["assignments"] if int(a["done_parts"]) < int(a["total_parts"])]
    if not active:
        print("  No active mini-bosses.")
        return
    for i, a in enumerate(active, 1):
        left = int(a["total_parts"]) - int(a["done_parts"])
        print(f"  {GREEN}{i}.{RESET} {a['name']} ({a['subject']}) - {left} part(s) left")
    print(f"  {GREEN}0.{RESET} Back")
    choice = get_int("Choose a mini-boss: ", 0, len(active))
    if choice == 0:
        return
    a = active[choice - 1]
    left = int(a["total_parts"]) - int(a["done_parts"])
    parts = get_int(f"How many parts did you finish (1-{left})? ", 1, left)
    a["done_parts"] = str(int(a["done_parts"]) + parts)
    print(f"  You hit {a['name']} for {parts} damage!")
    award_xp(XP_ASSIGN_PART * parts)
    if int(a["done_parts"]) == int(a["total_parts"]):
        print(YELLOW + f"  *** MINI-BOSS DEFEATED: {a['name']} ***" + RESET)
        award_xp(XP_ASSIGN_KILL)
