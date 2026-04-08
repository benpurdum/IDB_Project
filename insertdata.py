from random import randint
from werkzeug.security import generate_password_hash

departments = ["Music", "History", "Biology", "Comp. Sci.", "Elec. Eng.", "Finance", "Physics"]
first_names = ["Ben", "Jacob", "Zoe", "Kyle", "Irving", "Charlie", "Archie", "Colin", "Sean", "Rowan"]
last_names = ["Purdum", "Ford", "Smith", "Mallory", "Six", "Burrows", "Horne", "Grant", "Shea", "Ess"]
building = ["Bowman", "MSB", "Smith", "Kent", "Taylor", "Crawford", "Franklin"]
courses = ["CS1", "Physics 1", "World History 1", "Biology 1", "Engineering 1", "Finance 1", "Physics 1",
           "CS2", "Physics 2", "World History 2", "Biology 2", "Engineering 2", "Finance 2", "Physics 2", "Scuba Diving"]
course_ids = ["CS-10001", "PY-10001", "WH-10001", "BO-10001", "EG-10001", "FN-10001", "PH-10001",
              "CS-20002", "PY-20002", "WH-20002", "BO-20002", "EG-20002", "FN-20002", "PH-20002", "SD-10001"]

flcourse = ["CS-10001", "PY-10001", "WH-10001", "BO-10001", "EG-10001", "FN-10001", "PH-10001"] #first level
slcourse = ["CS-20002", "PY-20002", "WH-20002", "BO-20002", "EG-20002", "FN-20002", "PH-20002"] #second level

semesters = ["Fall", "Winter", "Spring", "Summer"]
day = ["M", "T", "W", "R", "F"]
grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"]

sql = []

class Student:
    def __init__(self, id):
        self.id = id
    
class Instructor:
    def __init__(self, id):
        self.id = id

class Room:
    def __init__(self, r_id, building, room_num):
        self.r_id = r_id
        self.building = building
        self.room_num = room_num

class Section:
    def __init__(self, course_id, sec_id, semester, year, building, room_id, time_slot_id):
        self.course_id = course_id
        self.sec_id = sec_id
        self.semester = semester
        self.year = year
        self.building = building
        self.room_id = room_id
        self.time_slot_id = time_slot_id

students = []
instructors = []
rooms = []
sections = []

n_id = 1 #name id
id = 10000 #person id
r_id = 20000 #room id
s_id = 1 # section id

#departments
for i in range(len(departments)):
    budget = randint(40000, 100000)
    sql.append(f"INSERT INTO department VALUES ('{departments[i]}', '{building[i]}', '{budget}');")

#classroom
for i in range(10):
    buil = building[randint(0, len(building) - 1)]
    r_num = randint(100, 999)
    sql.append(f"INSERT INTO classroom VALUES ('{r_id}', '{buil}', '{r_num}', '{randint(25, 200)}');")
    rooms.append(Room(r_id, buil, r_num))
    r_id += 1

#students
for i in range(20):
    ran = randint(0, len(first_names) - 1)
    fname = first_names[ran]
    ran = randint(0, len(last_names) - 1)
    lname = last_names[ran]

    user = fname+lname
    pas = generate_password_hash("password")
    sql.append(f"INSERT INTO accounts VALUES ('{id}', '{user}', '{pas}', 'Student');")

    sql.append(f"INSERT INTO name VALUES ('{n_id}', '{fname}', 'NULL', '{lname}', 'NULL');")

    ran = randint(0, len(departments) - 1)
    dept = departments[ran]
    sql.append(f"INSERT INTO student VALUES ('{id}', '{n_id}', '{dept}');")
    students.append(Student(id))

    n_id += 1
    id += 1

#instructors
id = 20000
for i in range(10):
    ran = randint(0, len(first_names) - 1)
    fname = first_names[ran]
    ran = randint(0, len(last_names) - 1)
    lname = last_names[ran]
    sql.append(f"INSERT INTO name VALUES ('{n_id}', '{fname}', 'NULL', '{lname}', 'NULL');")

    ran = randint(0, len(departments) - 1)
    dept = departments[ran]
    salary = randint(40000, 120000)

    user = fname+lname
    pas = generate_password_hash("password")
    sql.append(f"INSERT INTO accounts VALUES ('{id}', '{user}', '{pas}', 'Instructor');")

    sql.append(f"INSERT INTO instructor VALUES ('{id}', '{n_id}', '{dept}', '{salary}');")
    instructors.append(Instructor(id))

    n_id += 1
    id += 1

#add an admin to accounts
pas = generate_password_hash("admin")
sql.append(f"INSERT INTO accounts VALUES ('99999', 'admin', '{pas}', 'Administrator');")

#course - course_id	title	dept_name	credits	
for i in range(len(courses)):
    dept = departments[randint(0, len(departments) - 1)]
    sql.append(f"INSERT INTO course VALUES ('{course_ids[i]}', '{courses[i]}', '{dept}', '{randint(1,4)}');")

#section - course_id	sec_id	semester	year	building	room_id	time_slot_id	
for i in course_ids:
    for j in range(randint(1, 3)):
        sem = semesters[randint(0, len(semesters) - 1)]
        year = randint(2018, 2026)
        roomclass = rooms[randint(0, len(rooms) - 1)]
        buil = roomclass.building
        room = roomclass.r_id
        slot = randint(1, 20)
        sql.append(f"INSERT INTO section VALUES ('{i}', '{s_id}', '{sem}', '{year}', '{buil}', '{room}', '{slot}');")
        sections.append(Section(i, s_id, sem, year, buil, room, slot))
        
        s_id += 1
    s_id = 1

#time_slot - time_slot_id	day	start_hr	start_min	end_hr	end_min	
for j in range(20):
    i = j + 1
    if i < 5:
        day = "M"
    elif i < 9:
        day = "T"
    elif i < 13:
        day = "W"
    elif i < 17:
        day = "R"
    else:
        day = "F"
    
    if (i % 4) == 1:
        shr = "08"
        smin = "15"
        ehr = "09"
        emin = "20"
    elif (j % 4) == 2:
        shr = "09"
        smin = "35"
        ehr = "10"
        emin = "50"
    elif (j % 4) == 3:
        shr = "11"
        smin = "05"
        ehr = "12"
        emin = "20"
    else:
        shr = "12"
        smin = "35"
        ehr = "1"
        emin = "50"

    sql.append(f"INSERT INTO time_slot VALUES ('{i}', '{day}', '{shr}', '{smin}', '{ehr}', '{emin}');")

#takes - ID	course_id	sec_id	semester	year	grade
taking = []
for i in students:
    for j in range(randint(2, 4)):
        c = sections[randint(0, len(sections) - 1)]
        if c not in taking:
            taking.append(c)
            grade = grades[randint(0, len(grades) - 1)]
            sql.append(f"INSERT INTO takes VALUES ('{i.id}', '{c.course_id}', '{c.sec_id}', '{c.semester}', '{c.year}', '{grade}');")
    taking = []

#teaches - ID	course_id	sec_id	semester	year
for c in sections:
    i = instructors[randint(0, len(instructors) - 1)]
    sql.append(f"INSERT INTO teaches VALUES ('{i.id}', '{c.course_id}', '{c.sec_id}', '{c.semester}', '{c.year}');")

#prereq - course_id  prereq_id
for i in range(len(slcourse)):
    sql.append(f"INSERT INTO prereq VALUES ('{slcourse[i]}', '{flcourse[i]}');")



#write
if __name__ == "__main__":
    with open("data.sql", "w") as f:
        for line in sql:
            f.write(line + "\n")

    print("data.sql generated!")
