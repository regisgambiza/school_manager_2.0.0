# main.py
import sys
import sqlite3
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
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


def generate_receipt_html(payment_id, date_of_payment, student_id, amount_paid,
                          student_name="Unknown Student"):
    CURRENT_DATE = datetime.now().date()

    receipt_html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 20px;
                    border: 1px solid #000;
                    padding: 10px;
                }}
                .invoice-header {{
                    text-align: center;
                }}
                .invoice-details {{
                    margin-top: 20px;
                }}
                .thank-you {{
                    text-align: center;
                    margin-top: 20px;
                }}
                .contact-info {{
                    text-align: center;
                    margin-top: 10px;
                }}
            </style>
        </head>
        <body>

        <div class="invoice-header">
            <h2>Green Haven Academy</h2>
            <p>Invoice</p>
        </div>

        <div class="invoice-details">
            <p><strong>Payment ID:</strong> {payment_id}</p>
            <p><strong>Date:</strong> {date_of_payment}</p>
            <p><strong>Student ID:</strong> {student_id}</p>
            <p><strong>Student Name:</strong> {student_name}</p>
            <p><strong>Amount Paid:</strong> {amount_paid}</p>
        </div>

        <div class="thank-you">
            <p>Thank you for your payment!</p>
        </div>

        <div class="contact-info">
            <p>For any inquiries, please contact us at:</p>
            <p>Phone Number: 0617751307</p>
            <p>Email Address: regisgambiza@gmail.com</p>
        </div>

        </body>
        </html>
    """

    return receipt_html


class SchoolManagerApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # This sets up the UI from the generated file
        self.fetch_and_display_payments()
        self.ui.stackedWidget.setCurrentIndex(1)

        # self.setWindowFlags(Qt.FramelessWindowHint)

        # Connecting signals and slots
        self.ui.pay_now.clicked.connect(self.save_payment_info)
        self.ui.pushButton_2.clicked.connect(self.print_receipt_2)

    def save_payment_info(self):
        print("PayNow Clicked")
        # Fetch payment information from the GUI
        global db_connection
        student_id = self.ui.lineEdit.text()
        amount_paid = self.ui.lineEdit_2.text()

        print(f"{amount_paid}")

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

            # Display the receipt in the QTextBrowser
            self.ui.textBrowser.setHtml(generate_receipt_html(
                payment_id=cursor.lastrowid,  # Retrieve the last inserted payment_id
                date_of_payment=datetime.now().date(),
                student_id=student_id,
                amount_paid=amount_paid,
                student_name=student_name
            ))

        except sqlite3.Error as e:
            print(f"Error: {e}")

        finally:
            # Close the connection
            if db_connection:
                db_connection.close()

    def print_receipt_2(self):
        # Get the QTextDocument from the QTextBrowser
        global db_connection
        document = self.ui.textBrowser.document()

        try:
            # Connect to the SQLite database
            db_connection = sqlite3.connect('school_database.db')
            cursor = db_connection.cursor()

            # Fetch the details of the most recent payment
            cursor.execute('''
                SELECT payment_id, date_of_payment, student_id, amount_paid
                FROM financial_info
                ORDER BY date_of_payment DESC
                LIMIT 1
            ''')
            current_payment = cursor.fetchone()

            if current_payment:
                # Add payment details to the HTML
                receipt_html = generate_receipt_html(
                    payment_id=current_payment[0],
                    date_of_payment=current_payment[1],
                    student_id=current_payment[2],
                    amount_paid=current_payment[3]
                )

                # Set the HTML content to the QTextBrowser
                document.setHtml(receipt_html)

                # Create a QPrinter
                printer = QPrinter()

                # Create a QPrintDialog
                print_dialog = QPrintDialog(printer, self)

                if print_dialog.exec_() == QPrintDialog.Accepted:
                    # If the user accepts the print dialog, print the document
                    document.print_(printer)

            else:
                print("No payment found to print.")

        except sqlite3.Error as e:
            print(f"Error: {e}")

        finally:
            # Close the connection
            if db_connection:
                db_connection.close()


    def fetch_and_display_payments(self):
        global db_connection
        try:
            # Connect to the SQLite database
            db_connection = sqlite3.connect('school_database.db')
            cursor = db_connection.cursor()

            # Fetch all payments made in ascending order based on date_of_payment
            cursor.execute('''
                   SELECT payment_id, date_of_payment, student_id, amount_paid
                   FROM financial_info
                   ORDER BY date_of_payment ASC
               ''')
            payments = cursor.fetchall()

            # Format the payments as a list
            payments_list = [
                "Payment ID: {0}, Date: {1}, Student ID: {2}, Amount Paid: {3}".format(*payment)
                for payment in reversed(payments)  # Reverse the order to have the last payment at the top
            ]

            # Display the payments list in the QTextBrowser
            self.ui.textBrowser_2.setPlainText("\n".join(payments_list))

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
