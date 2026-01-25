from tracemalloc import start


students = []
File_name = 'students.txt'
def read_int(msg, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(msg))
            if min_val is not None and value < min_val:
                print("value is too small")
                continue
            if max_val is not None and value > max_val:
                print("value is too large")
                continue
            return value
        except ValueError:
            print("invalid input")
def read_non_empty_string(msg):
    while True:
        value = input(msg).strip()
        if value == '':
            print("cannot be empty")
        else:
            return value
def yes_no(msg):
    while True:
        value = input(msg + " (y/n):").strip().lower()
        if value in ['y', 'yes']:
            return True
        elif value in ['n', 'no']:
            return False
        print("enter y or n")
def find_students(name):
    for i, s in enumerate(students):
        if s['name'].lower() == name.lower():
            return i
    return -1
def load_students():
    loaded = 0
    skipped = 0
    try:
        with open(File_name, 'r') as f:
            for line in f:
                line = line.strip()
                if line == '':
                    continue
                parts = line.split(',')
                if len(parts) < 2:
                    skipped += 1
                    continue
                names = parts[0].strip()
                mark_str = parts[1].strip()
                if names == '':
                    skipped += 1
                    continue
                try:
                    mark = int(mark_str)
                except ValueError:
                    skipped += 1
                    continue
                if mark < 0 or mark > 100:
                    skipped += 1
                    continue
                idx = find_students(names)
                if idx != -1:
                    students[idx]['mark'] = mark
                else:
                    students.append({'name': names, 'mark': mark})
                    loaded += 1
        print(f"loaded {loaded} students, skipped {skipped} invalid entries")
    except FileNotFoundError:
        print("no student records found")
def save_data():
    with open(File_name, 'w') as f:
        for s in students:
            f.write(f"{s['name']},{s['mark']}\n")
    print(f"data saved {len(students)} to {File_name}")
def add_students():
    name = read_non_empty_string("enter student name:")
    mark = read_int("enter mark (0-100):", 0, 100)
    idx = find_students(name)
    if idx != -1:
        overwrite = yes_no("name already exists, overwrite mark? (y/n):")
        if not overwrite:
            print("not overwrite")
            return
        students[idx]["mark"] = mark
        print("updated.")
    else:
        students.append({"name":name, "mark":mark})
        print("added.")
def view_all():
    if len(students) == 0:
        print("no records")
        return
    for s in students:
        print(s["name"], "->", s["mark"])
def search_name():
    name = read_non_empty_string("enter name to search:")
    idx = find_students(name)
    if idx == -1:
        print("not found")
    else:
        print("found:", students[idx]["name"], "->", students[idx]["mark"])
def show_topper():
    if len(students) == 0:
        print("no records")
        return
    topper = max(students, key=lambda s: s["mark"])
    print("topper is:", topper["name"], "->", topper["mark"])
def rank_list():
    if len(students) == 0:
        print("no records")
        return
    ranked = sorted(students, key=lambda s: s['mark'], reverse=True)
    for i,s in enumerate(ranked, start=1):
        print(f"{i}. {s['name']}")
def stats():
    if len(students)==0:
        print("no records")
        return
    marks = [s['mark'] for s in students]
    avg = sum(marks)/len(marks)
    minimum = min(marks)
    maximum = max(marks)
    print(f"average: {avg:.2f}, min: {minimum}, max: {maximum}")
    
load_students()
while True:
    print("\n--- Marks Manager (Safe) ---")
    print("1.Add  2.View  3.Search  4.Topper  5.Rank  6.Stats  7.Save & Exit")

    ch = read_int("Enter choice: ", 1, 7)  

    if ch == 1:
        add_students()
    elif ch == 2:
        view_all()
    elif ch == 3:
        search_name()
    elif ch == 4:
        show_topper()
    elif ch == 5:
        rank_list()
    elif ch == 6:
        stats()
    elif ch == 7:
        save_data()
        break