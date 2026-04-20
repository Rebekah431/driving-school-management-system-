import sqlite3

DB_NAME = "database.db"

# ---------- Database Setup ----------

def connect():
    return sqlite3.connect(DB_NAME)

def setup():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS instructors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        instructor_id INTEGER,
        vehicle_id INTEGER,
        lesson_time TEXT
    )
    """)

    conn.commit()
    conn.close()

# ---------- Add Data ----------

def add_instructor():
    name = input("Instructor name: ")
    conn = connect()
    conn.execute("INSERT INTO instructors (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    print("Instructor added.")

def add_vehicle():
    model = input("Vehicle model: ")
    conn = connect()
    conn.execute("INSERT INTO vehicles (model) VALUES (?)", (model,))
    conn.commit()
    conn.close()
    print("Vehicle added.")

# ---------- View Data ----------

def view_instructors():
    conn = connect()
    for row in conn.execute("SELECT * FROM instructors"):
        print(row)
    conn.close()

def view_vehicles():
    conn = connect()
    for row in conn.execute("SELECT * FROM vehicles"):
        print(row)
    conn.close()

def view_bookings():
    conn = connect()
    query = """
    SELECT bookings.id, student_name, instructors.name, vehicles.model, lesson_time
    FROM bookings
    JOIN instructors ON bookings.instructor_id = instructors.id
    JOIN vehicles ON bookings.vehicle_id = vehicles.id
    """
    for row in conn.execute(query):
        print(row)
    conn.close()

# ---------- Booking Logic ----------

def is_conflict(instructor_id, vehicle_id, lesson_time):
    conn = connect()
    query = """
    SELECT * FROM bookings 
    WHERE lesson_time = ? AND (instructor_id = ? OR vehicle_id = ?)
    """
    result = conn.execute(query, (lesson_time, instructor_id, vehicle_id)).fetchone()
    conn.close()
    return result is not None

def create_booking():
    student = input("Student name: ")
    instructor_id = input("Instructor ID: ")
    vehicle_id = input("Vehicle ID: ")
    lesson_time = input("Lesson time (e.g. 2026-05-01 10:00): ")

    if is_conflict(instructor_id, vehicle_id, lesson_time):
        print("Booking conflict detected! Instructor or vehicle unavailable.")
        return

    conn = connect()
    conn.execute("""
        INSERT INTO bookings (student_name, instructor_id, vehicle_id, lesson_time)
        VALUES (?, ?, ?, ?)
    """, (student, instructor_id, vehicle_id, lesson_time))
    conn.commit()
    conn.close()

    print("Booking created successfully.")

# ---------- Menu ----------

def menu():
    while True:
        print("\n--- Driving School System ---")
        print("1. Add Instructor")
        print("2. Add Vehicle")
        print("3. View Instructors")
        print("4. View Vehicles")
        print("5. Create Booking")
        print("6. View Bookings")
        print("7. Exit")

        choice = input("Select option: ")

        if choice == "1":
            add_instructor()
        elif choice == "2":
            add_vehicle()
        elif choice == "3":
            view_instructors()
        elif choice == "4":
            view_vehicles()
        elif choice == "5":
            create_booking()
        elif choice == "6":
            view_bookings()
        elif choice == "7":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    setup()
    menu()
