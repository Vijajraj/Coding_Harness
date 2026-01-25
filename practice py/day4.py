class ContactBook:
    def __init__(self):
        self.contacts = {}
        self.load()

    def load(self):
        try:
            with open("contacts.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if line == "":
                        continue
                    try:
                        name, phone = line.split(",")
                        self.contacts[name] = phone
                    except ValueError:
                        print(f"Invalid line format: {line}")
        except FileNotFoundError:
            pass

    def save(self):
        with open("contacts.txt", "w") as f:
            for name, phone in self.contacts.items():
                f.write(name + "," + phone + "\n")

    def add(self, name, phone):
        self.contacts[name] = phone
        self.save()
        if not phone.isdigit() or len(phone) != 10:
            print("Invalid phone number. Please enter a 10-digit number.")
            return
        if name in self.contacts:
            ans = input("Contact already exists. Do you want to update it? (y/n): ")
            if ans.lower() != "y":
                self.contacts[name] = phone
                self.save()

    def view_all(self):
        if len(self.contacts) == 0:
            print("No contacts")
        else:
            for name, phone in self.contacts.items():
                print(name, "->", phone)

    def search(self, name):
        if name in self.contacts:
            print(name, "->", self.contacts[name])
        else:
            print("Not found")

    def delete(self, name):
        if name in self.contacts:
            del self.contacts[name]
            self.save()
            print("Deleted")
        else:
            print("Not found")


book = ContactBook()

while True:
    print("\n--- Contact Book (OOP) ---")
    print("1.Add  2.View  3.Search  4.Delete  5.Save & Exit")
    choice = input("Enter: ")

    if choice == "1":
        name = input("Name: ")
        phone = input("Phone: ")
        book.add(name, phone)

    elif choice == "2":
        book.view_all()

    elif choice == "3":
        name = input("Search name: ")
        book.search(name)

    elif choice == "4":
        name = input("Delete name: ")
        book.delete(name)

    elif choice == "5":
        book.save()
        break

    else:
        print("Invalid")
