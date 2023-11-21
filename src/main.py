# main.py
import sys
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic.properties import QtWidgets

from src.app.ui.school_manager import Ui_MainWindow

# TODO: Connect signals and slots for Add Student dialog
# class AddStudentDialog(QDialog, Ui_AddStudentDialog):
# def __init__(self):
# super().__init__()
# self.setupUi(self)

# TODO: Connect signals and slots for Add Student dialog
# Example:
# self.addButton.clicked.connect(self.add_student)

# TODO: Implement functions for handling Add Student dialog events
# Example:
# def add_student(self):
#     # TODO: Implement logic to add a new student
#     print("Adding a new student")


db_connection = ''


def create_school_database():
    global db_connection
    try:
        # Connect to the SQLite database (or create it if not exists)
        db_connection = sqlite3.connect('school_database.db')
        cursor = db_connection.cursor()

        # Check if the students table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students'")
        students_table_exists = cursor.fetchone() is not None

        if students_table_exists:
            print("Database 'school_database.db' already exists.")
        else:
            # Create students table with separate columns for name and surname
            cursor.execute('''
                CREATE TABLE students (
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

            # Create financial information table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS financial_info (
                    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date_of_payment TEXT,
                    student_id INTEGER,
                    amount_paid REAL,
                    FOREIGN KEY (student_id) REFERENCES students (student_id)
                )
            ''')

            print("New database 'school_database.db' has been created.")

        # Commit the changes
        db_connection.commit()

    except sqlite3.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        if db_connection:
            db_connection.close()


class SchoolManagerApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # This sets up the UI from the generated file

        # self.setWindowFlags(Qt.FramelessWindowHint)

        # TODO: Connect signals and slots for main window UI elements
        # Example:

        # self.stackedWidget.widget(0).connect(self.save_payment_info) # TODO: Fix this connection

    import sqlite3

    # FEES MODULE********************************************************************

    # def show_fees_module(self):
    # TODO: Implement the function to switch to the fees module page
    # using QStackedWidget.
    # Example:
    # self.stackedWidget.setCurrentWidget(self.fees_module_widget)

    # def add_fee(self):
    # TODO: Implement the logic to add a new fee record.
    # Example:
    #   - Retrieve data from UI components.
    #   - Perform validation.
    #   - Insert the new fee record into the database.
    #   - Provide appropriate user feedback.
    #   - Display transaction information on text-browser

    def save_payment_info(self):
        # Fetch payment information from the GUI
        global db_connection
        student_id = self.line_edit1.text()
        amount_paid = self.line_edit2.text()

        try:
            # Connect to the SQLite database
            db_connection = sqlite3.connect('school_database.db')
            cursor = db_connection.cursor()

            # Insert payment information into the financial_info table
            cursor.execute('''
                INSERT INTO financial_info (student_id, date_of_payment, amount_paid)
                VALUES (?, CURRENT_DATE, ?)
            ''', (student_id, amount_paid))

            # Commit the changes
            db_connection.commit()

            # Fetch the student's name for display in the receipt
            cursor.execute('SELECT first_name, last_name FROM students WHERE student_id = ?', (student_id,))
            student_name = cursor.fetchone()
            student_name = f"{student_name[0]} {student_name[1]}" if student_name else "Unknown Student"

            # Format the receipt
            CURRENT_DATE = datetime.now().date()
            receipt = f"Receipt\nDate: {CURRENT_DATE}\nStudent ID: {student_id}\nStudent Name: {student_name}\nAmount Paid: {amount_paid}"

            # Display the receipt in the QTextBrowser
            self.text_browser.setPlainText(receipt)

        except sqlite3.Error as e:
            print(f"Error: {e}")

        finally:
            # Close the connection
            if db_connection:
                db_connection.close()

    # def print_receipt(self):
    # TODO: Implement the logic to print a receipt to a physical printer.
    # Example:
    #   - Retrieve information from the text-browser.
    #   - Use a printing library or framework (e.g., QtPrintSupport) to send
    #     the receipt data to the physical printer.
    #   - Handle any necessary formatting for the printed receipt.
    #   - Provide appropriate user feedback.
    #   (Remember to replace the print statement with actual logic.)
    # Get information from text-browser
    # Print out a physical copy through printer

    # STUDENT MODULE****************************************************************

    # def show_students_page(self):
    # TODO: Implement the function to switch to the fees module page
    # using QStackedWidget.
    # Example:
    # self.stackedWidget.setCurrentWidget(students_page)

    # def view_student_list(self):
    # TODO: Implement the logic to display a list of students.
    # Example:
    #   - Retrieve student data from the database.
    #   - Format the data for display.
    #   - Populate the UI with the list of students.
    #   (Remember to replace the print statement with actual logic.)
    # print("Viewing student list")


def main():
    app = QApplication(sys.argv)

    # TODO: SQLite database connection
    # 1. Connect to the SQLite database
    #    - Use the sqlite3 module to establish a connection.
    # 2. Handle potential exceptions
    #    - Implement error handling for connection issues.
    # 3. Consider connection parameters
    #    - Review and adjust connection parameters as needed.
    # Example:
    # db_connection = sqlite3.connect('school_database.db')

    create_school_database()

    # TODO: Initialize and run the main application
    # 3. Create an instance of the SchoolManagerApp and pass the database connection
    # school_manager_app = SchoolManagerApp(db_connection)
    school_manager_app = SchoolManagerApp()  # replace this one with one above when database has been implemented

    school_manager_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
