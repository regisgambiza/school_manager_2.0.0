import sqlite3
from faker import Faker
from tqdm import tqdm


class DatabaseGenerator:
    def __init__(self):
        # Create an instance of the Faker class for generating fake data
        self.fake = Faker()

    def generate_random_student(self):
        # Generate random data for a student
        return (
            self.fake.first_name(),
            self.fake.last_name(),
            self.fake.random_element(["Class A", "Class B", "Class C"]),
            self.fake.phone_number(),
            self.fake.name(),
            self.fake.phone_number(),
            self.fake.email(),
            self.fake.address(),
        )

    def generate_random_payments(self, student_id, num_transactions):
        # Generate random payment data for a student
        payments_data = []
        for _ in range(num_transactions):
            payments_data.append((
                self.fake.date_of_birth(minimum_age=5, maximum_age=18).strftime('%Y-%m-%d'),
                student_id,
                self.fake.random_int(min=10, max=1000),
            ))
        return payments_data

    def generate_database(self, num_students, num_transactions_per_student):
        # Calculate the progress step for the progress bar
        progress_step = 100 / (num_students * (1 + num_transactions_per_student))  # 1 for student and transactions

        # Create a progress bar
        progress_bar = tqdm(total=num_students, desc="Generating Students", position=0, leave=True)

        # Connect to the SQLite database
        db_connection = sqlite3.connect('school_database.db')
        cursor = db_connection.cursor()

        # Create students and payments tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                class TEXT,
                phone_number TEXT,
                guardian_name TEXT,
                guardian_phone_number TEXT,
                guardian_email TEXT,
                physical_address TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS financial_info (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_of_payment TEXT,
                student_id INTEGER,
                amount_paid REAL,
                FOREIGN KEY (student_id) REFERENCES students (student_id)
            )
        ''')

        # Commit the changes
        db_connection.commit()

        for _ in range(num_students):
            # Generate random data for a student
            student_data = self.generate_random_student()
            # Insert the student data into the students table
            cursor.execute('''
                INSERT INTO students (
                    first_name, last_name, class, phone_number,
                    guardian_name, guardian_phone_number, guardian_email, physical_address
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', student_data)
            # Get the student ID of the last inserted student
            student_id = cursor.lastrowid

            # Generate and insert payments for the student
            payments_data = self.generate_random_payments(student_id, num_transactions_per_student)
            cursor.executemany('''
                INSERT INTO financial_info (date_of_payment, student_id, amount_paid)
                VALUES (?, ?, ?)
            ''', payments_data)

            # Update the progress bar
            progress_bar.update(1)

        # Commit the changes
        db_connection.commit()

        # Close the connection
        db_connection.close()

        # Close the progress bar
        progress_bar.close()


if __name__ == "__main__":
    # Take user input for the number of students and transactions per student
    num_students = int(input("Enter the number of students: "))
    num_transactions_per_student = int(input("Enter the number of transactions per student: "))

    # Generate the database using the DatabaseGenerator class
    generator = DatabaseGenerator()
    generator.generate_database(num_students, num_transactions_per_student)
