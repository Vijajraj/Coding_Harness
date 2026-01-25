contacts = {}

# Load existing contacts
try:
    with open("contacts.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            name, phone = line.split(",")
            contacts[name] = phone
except FileNotFoundError:
    pass

while True:
    print("\n--- Contact Book ---")
    print("1. Add")
    print("2. View All")
    print("3. Search")
    print("4. Delete")
    print("5. Save & Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Enter name: ")
        phone = input("Enter phone: ")
        contacts[name] = phone
        print("Contact saved.")

    elif choice == "2":
        if len(contacts) == 0:
            print("No contacts.")
        else:
            for name, phone in contacts.items():
                print(name, "->", phone)

    elif choice == "3":
        name = input("Enter name to search: ")
        if name in contacts:
            print(name, "->", contacts[name])
        else:
            print("Not found.")

    elif choice == "4":
        name = input("Enter name to delete: ")
        if name in contacts:
            del contacts[name]
            print("Deleted.")
        else:
            print("Not found.")

    elif choice == "5":
        with open("contacts.txt", "w") as f:
            for name, phone in contacts.items():
                f.write(name + "," + phone + "\n")
        print("Saved. Exiting.")
        break

    else:
        print("Invalid choice.")
