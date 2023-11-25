# main.py
import sys
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from src.app.ui.school_manager import Ui_MainWindow
from src.app.ui.Add_student_dialog import Ui_Dialog

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


class AddStudentDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.add_student)
        self.buttonBox.rejected.connect(self.reject)

    def add_student(self):
        # Retrieve user input from the dialog
        first_name = self.lineEdit.text()
        last_name = self.lineEdit_2.text()
        class_name = self.lineEdit_3.text()
        phone_number = self.lineEdit_4.text()
        guardian_name = self.lineEdit_5.text()
        guardian_phone_number = self.lineEdit_6.text()
        guardian_email = self.lineEdit_7.text()
        physical_address = self.lineEdit_8.text()

        # Add the student to the database
        try:
            # Connect to the SQLite database
            db_connection = sqlite3.connect('school_database.db')
            cursor = db_connection.cursor()

            # Insert the student information into the students table
            cursor.execute('''
                INSERT INTO students (first_name, last_name, class, phone_number,
                                       guardian_name, guardian_phone_number, guardian_email, physical_address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, last_name, class_name, phone_number,
                  guardian_name, guardian_phone_number, guardian_email, physical_address))

            # Commit the changes
            db_connection.commit()

            # Close the dialog
            self.accept()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            # Display an error message to the user
            QMessageBox.critical(self, "Error", "Failed to add the student to the database.")

        finally:
            # Close the connection
            if db_connection:
                db_connection.close()


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
        self.ui.textBrowser_3.anchorClicked.connect(
            self.show_student_info)  # Add a signal for the student list item clicked

        # self.setWindowFlags(Qt.FramelessWindowHint)

        # Connecting signals and slots
        self.ui.pay_now.clicked.connect(self.save_payment_info)
        self.ui.pushButton_2.clicked.connect(self.print_receipt_2)
        self.ui.fees_push_button.clicked.connect(lambda: self.change_page(1))
        self.ui.students_push_button.clicked.connect(lambda: self.change_page(2))
        self.ui.students_push_button.clicked.connect(self.show_students_list)
        self.ui.pushButton_5.clicked.connect(self.show_add_student_dialog)
        self.ui.lineEdit.textChanged.connect(self.search_student_by_id)
        self.ui.pushButton.clicked.connect(self.show_students_list)

    def show_students_list(self):
        global db_connection
        try:
            # Connect to the SQLite database
            db_connection = sqlite3.connect('school_database.db')
            cursor = db_connection.cursor()

            # Fetch all students from the database, ordered by first name and last name
            cursor.execute('SELECT student_id, first_name, last_name FROM students ORDER BY first_name, last_name')
            students = cursor.fetchall()

            # Format the students list as HTML for display in QTextBrowser
            students_list_html = "<ul>"
            for student in students:
                student_id, first_name, last_name = student
                students_list_html += f'<li><a href="{student_id}">{first_name} {last_name}</a></li>'
            students_list_html += "</ul>"

            # Display the students list in QTextBrowser
            self.ui.textBrowser_3.setHtml(students_list_html)

        except sqlite3.Error as e:
            print(f"Error: {e}")

        finally:
            # Close the connection
            if db_connection:
                db_connection.close()

    def show_student_info(self, link):
        # Extract student_id from the link and fetch detailed information
        student_id = int(link.toString())
        student_info = self.get_student_info(student_id)

        # Display the detailed information in QTextBrowser
        self.ui.textBrowser_3.setHtml(student_info)

    def get_student_info(self, student_id):
        global db_connection
        try:
            # Connect to the SQLite database
            db_connection = sqlite3.connect('school_database.db')
            cursor = db_connection.cursor()

            # Fetch detailed information of the selected student
            cursor.execute('''
                SELECT * FROM students
                WHERE student_id = ?
            ''', (student_id,))

            student_info = cursor.fetchone()

            # Fetch student payments arranged by date with the latest payment at the top
            cursor.execute('''
                SELECT date_of_payment, amount_paid, payment_id
                FROM financial_info
                WHERE student_id = ?
                ORDER BY date_of_payment DESC
            ''', (student_id,))
            payments = cursor.fetchall()

            # Format the student information and payments for display
            if student_info:
                student_info_text = f"<h2>Student ID: {student_info[0]}</h2>"
                student_info_text += f"<p>Name: {student_info[1]} {student_info[2]}</p>"
                student_info_text += f"<p>Class: {student_info[3]}</p>"
                student_info_text += f"<p>Phone Number: {student_info[4]}</p>"
                student_info_text += f"<p>Guardian: {student_info[5]}</p>"
                student_info_text += f"<p>Guardian Phone: {student_info[6]}</p>"
                student_info_text += f"<p>Guardian Email: {student_info[7]}</p>"
                student_info_text += f"<p>Physical Address: {student_info[8]}</p>"

                if payments:
                    student_info_text += "<h3>Payments:</h3>"
                    total_amount_paid = 0

                    for payment in payments:
                        student_info_text += (
                            f"<p>Payment ID: {payment[2]}, Date: {payment[0]}, Amount Paid: {payment[1]}</p>"
                        )
                        total_amount_paid += payment[1]

                    student_info_text += f"<p><strong>Total Amount Paid: {total_amount_paid}</strong></p>"

                return student_info_text
            else:
                return "Student not found."

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return "Error fetching student information."

        finally:
            # Close the connection
            if db_connection:
                db_connection.close()

    def search_student_by_id(self):
        # Get the entered student ID
        student_id = self.ui.lineEdit.text()

        # Perform a search in the database based on the entered student ID
        student_info = self.fetch_student_info(student_id)

        # Display the student's name in lineEdit_2
        if student_info:
            full_name = f"{student_info[1]} {student_info[2]}"  # Adjust indices based on your database schema
            self.ui.lineEdit_3.setText(full_name)
        else:
            # Clear lineEdit_2 if no matching student is found
            self.ui.lineEdit_3.clear()

    def fetch_student_info(self, student_id):
        # Implement the logic to fetch student information from the database
        global db_connection
        try:
            # Connect to the SQLite database
            db_connection = sqlite3.connect('school_database.db')
            cursor = db_connection.cursor()

            # Fetch detailed information of the selected student
            cursor.execute('''
                SELECT * FROM students
                WHERE student_id = ?
            ''', (student_id,))

            student_info = cursor.fetchone()

            return student_info

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:
            # Close the connection
            if db_connection:
                db_connection.close()

    def show_add_student_dialog(self):
        # Create an instance of the AddStudentDialog
        add_student_dialog = AddStudentDialog()

        # Show the dialog
        if add_student_dialog.exec_() == QDialog.Accepted:
            # TODO: Refresh the student list or perform any other necessary actions
            print("Student added successfully")

    def change_page(self, index):
        # Change the current page of the stacked widget
        self.ui.stackedWidget.setCurrentIndex(index)

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
            self.fetch_and_display_payments()
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

            # Fetch all payments made in descending order based on date_of_payment
            cursor.execute('''
                SELECT payment_id, date_of_payment, student_id, amount_paid
                FROM financial_info
                ORDER BY date_of_payment DESC
            ''')
            payments = cursor.fetchall()

            # Generate HTML table for payments
            table_html = """
                <html>
                <head>
                    <style>
                        table {
                            border-collapse: collapse;
                            width: 100%;
                        }
                        th, td {
                            border: 1px solid #dddddd;
                            text-align: left;
                            padding: 8px;
                        }
                    </style>
                </head>
                <body>
                <table>
                    <tr>
                        <th>Payment ID</th>
                        <th>Date</th>
                        <th>Student ID</th>
                        <th>Amount Paid</th>
                    </tr>
            """

            for payment in payments:
                table_html += f"""
                    <tr>
                        <td>{payment[0]}</td>
                        <td>{payment[1]}</td>
                        <td>{payment[2]}</td>
                        <td>{payment[3]}</td>
                    </tr>
                """

            table_html += """
                </table>
                </body>
                </html>
            """

            # Display the HTML table in the QTextBrowser
            self.ui.textBrowser_2.setHtml(table_html)

        except sqlite3.Error as e:
            print(f"Error: {e}")

        finally:
            # Close the connection
            if db_connection:
                db_connection.close()

    # STUDENT MODULE****************************************************************

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
    create_school_database()
    school_manager_app = SchoolManagerApp()
    school_manager_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
