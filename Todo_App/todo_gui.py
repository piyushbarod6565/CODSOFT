import tkinter as tk
import customtkinter as ctk
import json
import os


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List 📋")
        self.geometry("450x700+700+50")
        self.configure(fg_color=("#F9F9F9", "#121212"))
        self.tasks = self.load_tasks()
        self.create_widgets()
        self.render_tasks()
        self.update_stats()


    def load_tasks(self):
        try:
            if os.path.exists("tasks.json"):
                with open("tasks.json", "r") as file:
                    return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return []


    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file, indent=4)


    def create_widgets(self):
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(fill="x", pady=(30, 20), padx=30)

        self.header_label = ctk.CTkLabel(
            self.top_bar, text="To-Do List 📋", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#1A365D", "#FFFFFF")
        )
        self.header_label.pack(side="left")


        self.is_dark = False
        self.theme_btn = ctk.CTkButton(
            self.top_bar, text="☀️", width=40, height=40, corner_radius=20,
            fg_color=("#ECECEC", "#2A2A2A"), text_color=("#333333", "#FFFFFF"),
            hover_color=("#D1D1D1", "#3A3A3A"),
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="right")


        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=30, pady=(0, 20))

        self.task_entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Add your task",
            height=50,
            corner_radius=25,
            border_width=0,
            fg_color=("#ECECEC", "#2A2A2A"),
            text_color=("#333333", "#FFFFFF")
        )
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())


        self.add_button = ctk.CTkButton(
            self.input_frame, 
            text="ADD", width=100, height=50, corner_radius=25,
            fg_color="#3358FF", hover_color="#2A19E6",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.add_task
        )
        self.add_button.pack(side="right")


        self.tasks_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent"
        )
        self.tasks_frame.pack(fill="both", expand=True, padx=20, pady=10)


        self.tracker_frame = ctk.CTkFrame(
            self, corner_radius=15, 
            fg_color=("#F4F4F4", "#1E1E1E"),
            border_width=1,
            border_color=("#E0E0E0", "#333333")
        )
        self.tracker_frame.pack(fill="x", padx=25, pady=(10, 30))


        tracker_inner = ctk.CTkFrame(self.tracker_frame, fg_color="transparent")
        tracker_inner.pack(padx=15, pady=15, fill="x")


        ctk.CTkLabel(
            tracker_inner, text="TASK TRACKER", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#1A365D", "#FFFFFF")
        ).pack(anchor="nw", pady=(0, 10))


        self.stats_container = ctk.CTkFrame(tracker_inner, fg_color="transparent")
        self.stats_container.pack(fill="x")


        self.create_stat_item(self.stats_container, "Total Tasks", "0", "#1E88E5", 0)
        self.create_stat_item(self.stats_container, "Completed Tasks", "0", "#1E88E5", 1)
        self.create_stat_item(self.stats_container, "Pending Tasks", "0", "#1E88E5", 2)


    def create_stat_item(self, parent, label_text, value_text, color, column):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=0, column=column * 2, sticky="nsew")
        parent.grid_columnconfigure(column * 2, weight=1)

        if column > 0:
            divider = ctk.CTkFrame(parent, width=1, height=30, fg_color=("#E0E0E0", "#444444"))
            divider.grid(row=0, column=column * 2 - 1, sticky="ns", pady=5)

        ctk.CTkLabel(
            container, text=label_text, font=ctk.CTkFont(size=11), text_color="gray"
            ).pack()

        value_label = ctk.CTkLabel(
            container, text=value_text, font=ctk.CTkFont(size=22, weight="bold"), text_color=color
            )
        value_label.pack()


        if "Total" in label_text:
            self.total_label = value_label

        elif "Completed" in label_text:
            self.completed_label = value_label
            
        elif "Pending" in label_text:
            self.pending_label = value_label


    def toggle_theme(self):
        if not self.is_dark:
            ctk.set_appearance_mode("light")
            self.theme_btn.configure(text="🌙")
            self.is_dark = True
        else:
            ctk.set_appearance_mode("dark")
            self.theme_btn.configure(text="☀️")
            self.is_dark = False


    def add_task(self, event=None):
        task_text = self.task_entry.get().strip()
        if task_text:
            self.tasks.append({"task": task_text, "Completed": False})
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
            self.render_tasks()
            self.update_stats()


    def toggle_task(self, index):
        self.tasks[index]["Completed"] = not self.tasks[index]["Completed"]
        self.save_tasks()
        self.render_tasks()
        self.update_stats()


    def delete_task(self, index):
        self.tasks.pop(index)
        self.save_tasks()
        self.render_tasks()
        self.update_stats()


    def edit_task(self, index):
        dialog = ctk.CTkInputDialog(text="Edit Task:", title="Update Task")
        new_text = dialog.get_input()
        if new_text and new_text.strip():
            self.tasks[index]["task"] = new_text.strip()
            self.save_tasks()
            self.render_tasks()


    def render_tasks(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        for i, task in enumerate(self.tasks):
            task_row = ctk.CTkFrame(self.tasks_frame, fg_color="transparent")
            task_row.pack(fill="x", pady=(5, 0))

            is_done = task["Completed"]
            status_color = "#333DFF" if is_done else "transparent"
            border_color = "#3D33FF" if is_done else ("#D1D1D1", "#444444")
            

            check_btn = ctk.CTkButton(
                task_row, 
                text="✓" if is_done else "", 
                width=26, 
                height=26, 
                corner_radius=13,
                fg_color=status_color, 
                border_width=2, 
                border_color=border_color,
                hover_color="#4643FF", 
                text_color="white", 
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda idx=i: self.toggle_task(idx)
            )
            check_btn.pack(side="left", padx=(10, 15), pady=10)


            task_label = ctk.CTkLabel(
                task_row, 
                text=task["task"], 
                text_color=("#A0A0A0", "#777777") if is_done else ("#333333", "#EEEEEE"), 
                font=ctk.CTkFont(size=15, overstrike=is_done),
                anchor="w", 
                wraplength=250, 
                justify="left"
            )
            task_label.pack(side="left", fill="x", expand=True, pady=10)


            ctk.CTkButton(
                task_row, 
                text="✎", 
                width=35, 
                height=35, 
                fg_color="transparent",
                text_color=("#666666", "#AAAAAA"), 
                hover_color=("#F0F0F0", "#2A2A2A"), 
                font=ctk.CTkFont(size=20),
                command=lambda idx=i: self.edit_task(idx)
            ).pack(side="left", padx=2)


            ctk.CTkButton(
                task_row, 
                text="✕", 
                width=35, 
                height=35, 
                fg_color="transparent",
                text_color=("#666666", "#AAAAAA"), 
                hover_color=("#F0F0F0", "#2A2A2A"),
                font=ctk.CTkFont(size=18),
                command=lambda idx=i: self.delete_task(idx)
            ).pack(side="left", padx=(2, 10))
            
            ctk.CTkFrame(self.tasks_frame, height=1, fg_color=("#EEEEEE", "#222222")).pack(fill="x", padx=10)


    def update_stats(self):
        total = len(self.tasks)
        completed = 0

        for task in self.tasks:
            if task["Completed"] == True:
                completed = completed + 1
        self.total_label.configure(text=str(total))
        self.completed_label.configure(text=str(completed))
        self.pending_label.configure(text=str(total - completed))


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
