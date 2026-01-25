students = []
def add_student():
    name = input("Enter student name:").strip()
    marks = int(input("Enter student marks:"))
    if marks < 0 or marks > 100:
        print("invalid marks")
        return
    students.append({'name': name, 'marks': marks})
    print("added")
def view_all():
    if len(students) == 0:
        print("no records")
        return 
    for s in students:
        print( s['name'], "->", s['marks'])
def search_name():
    name = input("Enter name to search:").strip()
    for s in students:
        if s['name'].lower() == name.lower():
            print("found:", s["name"] , " ->" , s["marks"])
            return
    print("not found")
def show_topper():
    if len(students) == 0:
        print("no records")
        return
    topper = max(students, key=lambda s:s['marks'])
    print("topper:", topper['name'], "->", topper['marks'])
def rank_students():
    if len(students) == 0:
        print("no records")
    rank = sorted(students, key=lambda s:s['marks'], reverse=True)
    rank = 1
    for s in rank:
        print(rank, s['name'], "->" , s['marks'])
        rank += 1
def stats():
    if len(students) == 0:
        print("no records")
        return
    marks = [s['marks'] for s in students]
    print("average:", sum(marks)/len(marks))
    print("highest:", max(marks))
    print("lowest:", min(marks))
def load_data():
    try:
        with open("students.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line == "":
                    continue
                name,marks = line.split(",")
                students.append({'name': name, 'marks': int(marks)})
        print("data loaded", len(students), "from records")
    except FileNotFoundError:
        print("not found")
def save_data():
    with open("students.txt", "w") as f:
        for s in students:
            f.write(f"{s['name']},{s['marks']}\n")
    print("data saved", len(students), "to records")

while True:
    print("\n1. Add Student\n2. View All Students\n3. Search by Name\n4. Show Topper\n5. Rank Students\n6. Statistics\n7. Exit")
    choice = input("Enter your choice:")
    if choice == '1':
        add_student()
    elif choice == '2':
        view_all()
    elif choice == '3':
        search_name()
    elif choice == '4':
        show_topper()
    elif choice == '5':
        rank_students()
    elif choice == '6':
        stats()
    elif choice == '7':
        save_data()
        break
    else:
        print("Invalid choice, try again.")