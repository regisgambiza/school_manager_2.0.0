import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


class SchoolStatisticsDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("School Statistics Dashboard")
        self.root.geometry("1000x800")

        self.create_widgets()

    def create_widgets(self):
        # Header Label
        header_label = tk.Label(self.root, text="School Statistics Dashboard", font=("Helvetica", 16, "bold"))
        header_label.pack(pady=10)

        # Statistics Frame
        statistics_frame = ttk.Frame(self.root, borderwidth=2, relief="solid")
        statistics_frame.pack(pady=20, padx=10, fill="both", expand=True)

        # Placeholder Statistics
        total_students_label = tk.Label(statistics_frame, text="Total Students:")
        total_students_value = tk.Label(statistics_frame, text=str(random.randint(500, 1000)))

        total_teachers_label = tk.Label(statistics_frame, text="Total Teachers:")
        total_teachers_value = tk.Label(statistics_frame, text=str(random.randint(50, 100)))

        total_income_label = tk.Label(statistics_frame, text="Total Income:")
        total_income_value = tk.Label(statistics_frame, text=f"${random.randint(100000, 500000)}")

        # Grid Layout
        total_students_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        total_students_value.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        total_teachers_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        total_teachers_value.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        total_income_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        total_income_value.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Chart Frame
        chart_frame = ttk.Frame(self.root, borderwidth=2, relief="solid")
        chart_frame.pack(pady=20, padx=10, fill="both", expand=True)

        # Matplotlib Chart
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        self.plot_chart(ax)
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Exit Button
        exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
        exit_button.pack(pady=10)

    def plot_chart(self, ax):
        # Placeholder Chart (replace with actual data)
        categories = ['Math', 'English', 'Science', 'History', 'Art']
        values = [random.randint(60, 100) for _ in range(len(categories))]

        ax.bar(categories, values, color='skyblue')
        ax.set_title('Subject Performance')
        ax.set_xlabel('Subjects')
        ax.set_ylabel('Scores')


if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolStatisticsDashboard(root)
    root.mainloop()
