import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime

class TaskApp:
    def __init__(self, master):
        self.master = master
        self.tasks = []
        self.create_widgets()

    def create_widgets(self):
        # Sidebar
        sidebar_frame = tk.Frame(self.master, bg="lightgrey", width=200)
        sidebar_frame.pack(fill=tk.Y, side=tk.LEFT)

        sidebar_label = tk.Label(sidebar_frame, text="To Do List", font=("Helvetica", 14), bg="lightgrey")
        sidebar_label.pack(pady=10)

        btn_todo = tk.Button(sidebar_frame, text="To Do List", width=20, highlightbackground="lightgrey", command=self.show_todo_list)
        btn_todo.pack(pady=5)

        btn_calendar = tk.Button(sidebar_frame, text="Calendar", width=20, highlightbackground="lightgrey", command=self.show_calendar)
        btn_calendar.pack(pady=5)

        # Main Content
        self.main_frame = tk.Frame(self.master, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.task_list_frame = tk.Frame(self.main_frame)
        self.calendar_frame = tk.Frame(self.main_frame)

        self.show_todo_list()

    def show_todo_list(self):
        self.clear_main_frame()
        self.task_list_frame.pack(fill=tk.BOTH, expand=True)

        label_title = tk.Label(self.task_list_frame, text="Task", font=("Helvetica", 16))
        label_title.pack(pady=10)

        self.task_list = tk.Frame(self.task_list_frame)
        self.task_list.pack(anchor="w")

        self.task_entry = tk.Entry(self.task_list_frame, width=50)
        self.task_entry.pack()

        self.add_button = tk.Button(self.task_list_frame, text="Add Task", command=self.add_task)
        self.add_button.pack()

    def show_calendar(self):
        self.clear_main_frame()
        self.calendar_frame.pack(fill=tk.BOTH, expand=True)

        header_frame = tk.Frame(self.calendar_frame)
        header_frame.pack(fill=tk.X)

        self.prev_button = tk.Button(header_frame, text="<", command=self.prev_month)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(header_frame, text=">", command=self.next_month)
        self.next_button.pack(side=tk.RIGHT, padx=10)

        self.month_label = tk.Label(header_frame, text="", font=("Helvetica", 16))
        self.month_label.pack(side=tk.LEFT, expand=True)

        self.calendar_content_frame = tk.Frame(self.calendar_frame)
        self.calendar_content_frame.pack(fill=tk.BOTH, expand=True)

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.show_calendar_content(self.current_year, self.current_month)

    def show_calendar_content(self, year, month):
        for widget in self.calendar_content_frame.winfo_children():
            widget.destroy()

        cal = calendar.Calendar()
        month_days = cal.monthdayscalendar(year, month)

        self.month_label.config(text=f"{calendar.month_name[month]} {year}")

        days_header = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for day in days_header:
            day_label = tk.Label(self.calendar_content_frame, text=day, padx=10, pady=5)
            day_label.grid(row=0, column=days_header.index(day))

        for week_index, week in enumerate(month_days):
            for day_index, day in enumerate(week):
                if day == 0:
                    day_label = tk.Label(self.calendar_content_frame, text="", padx=10, pady=5)
                else:
                    day_label = tk.Label(self.calendar_content_frame, text=str(day), padx=10, pady=5)
                day_label.grid(row=week_index + 1, column=day_index)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            task_frame = tk.Frame(self.task_list)
            task_frame.pack(anchor="w", pady=5)

            task_check = tk.Checkbutton(task_frame, command=lambda: self.toggle_task(task_check))
            task_check.pack(side=tk.LEFT)

            task_label = tk.Label(task_frame, text=task_text, width=40, anchor="w")
            task_label.pack(side=tk.LEFT)

            # Three dots symbol for menu
            dots_label = tk.Label(task_frame, text="...", padx=10, cursor="hand2")
            dots_label.pack(side=tk.RIGHT)
            dots_label.bind("<Button-1>", lambda event, frame=task_frame: self.show_popup_menu(event, frame))

            self.tasks.append({"text": task_text, "frame": task_frame, "check": task_check})
            self.task_entry.delete(0, tk.END)

    def toggle_task(self, task_check):
        for task in self.tasks:
            if task["check"] == task_check:
                if task_check.cget("background") == "":
                    task_check.configure(background="cyan")
                else:
                    task_check.configure(background="")
                break

    def show_popup_menu(self, event, task_frame):
        menu = tk.Menu(self.master, tearoff=0)
        menu.add_command(label="Edit", command=lambda frame=task_frame: self.edit_task(frame))
        menu.add_command(label="Delete", command=lambda frame=task_frame: self.delete_task(frame))
        menu.post(event.x_root, event.y_root)

    def edit_task(self, task_frame):
        task_label = task_frame.winfo_children()[1]  # 获取标签组件
        current_text = task_label.cget("text")

        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Task")

        edit_entry = tk.Entry(edit_window, width=40)
        edit_entry.insert(0, current_text)
        edit_entry.pack(padx=10, pady=10)

        save_button = tk.Button(edit_window, text="Save", command=lambda: self.save_task(task_frame, edit_window, edit_entry))
        save_button.pack()

    def save_task(self, task_frame, edit_window, edit_entry):
        new_text = edit_entry.get()
        task_label = task_frame.winfo_children()[1]  # 获取标签组件
        task_label.config(text=new_text)
        edit_window.destroy()  # 保存后关闭编辑窗口

    def delete_task(self, task_frame):
        task_frame.destroy()

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.show_calendar_content(self.current_year, self.current_month)

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.show_calendar_content(self.current_year, self.current_month)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("To Do List & Calendar")
    root.geometry("800x600")

    app = TaskApp(root)

    root.mainloop()