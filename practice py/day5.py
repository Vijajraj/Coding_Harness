students = {
    "vijay": 19,
    "raj": 20,
    "ajay": 28.2,
    "sanjay":21
}
sorted_students = dict(sorted(students.items(), key= lambda item: item[1]))
print(sorted_students)
rank = 1
for name, age in sorted_students.items():
    print(rank, name, "->", age)
    rank += 1