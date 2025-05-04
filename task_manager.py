import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import json
import os
from datetime import datetime

class DailyTaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Task Manager")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f5f5")
        
        # Data structure
        self.tasks = []
        self.completed_tasks = []
        self.incomplete_tasks = []
        
        # Data file
        self.data_file = "task_data.json"
        self.load_data()
        
        # Create frames
        self.create_header_frame()
        self.create_task_frame()
        self.create_completed_frame()
        self.create_incomplete_frame()
        self.create_control_frame()
        
        # Update displays
        self.update_all_displays()
    
    def create_header_frame(self):
        header_frame = tk.Frame(self.root, bg="#4a6fa5", pady=10)
        header_frame.pack(fill=tk.X)
        
        today = datetime.now().strftime("%A, %B %d, %Y")
        title_label = tk.Label(
            header_frame, 
            text=f"Daily Task Manager - {today}",
            font=("Arial", 16, "bold"),
            bg="#4a6fa5",
            fg="white"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Organize your day and track your progress",
            font=("Arial", 10),
            bg="#4a6fa5",
            fg="white"
        )
        subtitle_label.pack()
    
    def create_task_frame(self):
        # Task list frame
        task_outer_frame = tk.LabelFrame(self.root, text="Today's Tasks", font=("Arial", 12), bg="#f5f5f5", padx=10, pady=10)
        task_outer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add button
        add_button = tk.Button(task_outer_frame, text="Add Task", command=self.add_task, bg="#4a6fa5", fg="white", padx=10)
        add_button.pack(anchor=tk.W, pady=(0, 10))
        
        # Task listbox with scrollbar
        task_frame = tk.Frame(task_outer_frame)
        task_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tasks_listbox = tk.Listbox(
            task_frame,
            selectmode=tk.SINGLE,
            bg="white",
            font=("Arial", 10),
            height=15
        )
        self.tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tasks_scrollbar = tk.Scrollbar(task_frame)
        tasks_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tasks_listbox.config(yscrollcommand=tasks_scrollbar.set)
        tasks_scrollbar.config(command=self.tasks_listbox.yview)
        
        # Action buttons
        action_frame = tk.Frame(task_outer_frame, bg="#f5f5f5")
        action_frame.pack(fill=tk.X, pady=10)
        
        complete_button = tk.Button(
            action_frame,
            text="Mark Complete",
            command=self.mark_complete,
            bg="#2e8b57",
            fg="white",
            padx=10
        )
        complete_button.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_button = tk.Button(
            action_frame,
            text="Delete Task",
            command=self.delete_task,
            bg="#808080",
            fg="white",
            padx=10
        )
        delete_button.pack(side=tk.LEFT, padx=5)
    
    def create_completed_frame(self):
        # Completed tasks frame
        completed_outer_frame = tk.LabelFrame(self.root, text="Completed Tasks", font=("Arial", 12), bg="#f5f5f5", padx=10, pady=10)
        completed_outer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        # Completed listbox with scrollbar
        completed_frame = tk.Frame(completed_outer_frame)
        completed_frame.pack(fill=tk.BOTH, expand=True)
        
        self.completed_listbox = tk.Listbox(
            completed_frame,
            selectmode=tk.SINGLE,
            bg="#efffef",
            font=("Arial", 10),
            height=7
        )
        self.completed_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        completed_scrollbar = tk.Scrollbar(completed_frame)
        completed_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.completed_listbox.config(yscrollcommand=completed_scrollbar.set)
        completed_scrollbar.config(command=self.completed_listbox.yview)
    
    def create_incomplete_frame(self):
        # Incomplete tasks frame
        incomplete_outer_frame = tk.LabelFrame(self.root, text="Incomplete Tasks", font=("Arial", 12), bg="#f5f5f5", padx=10, pady=10)
        incomplete_outer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        # Incomplete listbox with scrollbar
        incomplete_frame = tk.Frame(incomplete_outer_frame)
        incomplete_frame.pack(fill=tk.BOTH, expand=True)
        
        self.incomplete_listbox = tk.Listbox(
            incomplete_frame,
            selectmode=tk.SINGLE,
            bg="#ffefef",
            font=("Arial", 10),
            height=7
        )
        self.incomplete_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        incomplete_scrollbar = tk.Scrollbar(incomplete_frame)
        incomplete_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.incomplete_listbox.config(yscrollcommand=incomplete_scrollbar.set)
        incomplete_scrollbar.config(command=self.incomplete_listbox.yview)
        
        # Add "Move back to today's tasks" button
        move_back_button = tk.Button(
            incomplete_outer_frame,
            text="Move Back to Today's Tasks",
            command=self.move_back_to_tasks,
            bg="#ff7f50",
            fg="white",
            padx=10
        )
        move_back_button.pack(pady=(5, 0))
    
    def create_control_frame(self):
        # Control frame
        control_frame = tk.Frame(self.root, bg="#f5f5f5", pady=10)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10)
        
        save_button = tk.Button(
            control_frame,
            text="Save All",
            command=self.save_data,
            bg="#4a6fa5",
            fg="white",
            padx=20,
            pady=5
        )
        save_button.pack(side=tk.RIGHT, padx=5)
        
        reset_button = tk.Button(
            control_frame,
            text="Start New Day",
            command=self.start_new_day,
            bg="#ff7f50",
            fg="white",
            padx=20,
            pady=5
        )
        reset_button.pack(side=tk.RIGHT, padx=5)
        
        # Add button to manually move incomplete tasks
        check_incomplete_button = tk.Button(
            control_frame,
            text="Move Incomplete Tasks",
            command=self.move_incomplete_tasks,
            bg="#cd5c5c",
            fg="white",
            padx=20,
            pady=5
        )
        check_incomplete_button.pack(side=tk.RIGHT, padx=5)
        
        # Add button to view archives
        archives_button = tk.Button(
            control_frame,
            text="View Archives",
            command=self.open_archives_viewer,
            bg="#9370db",
            fg="white",
            padx=20,
            pady=5
        )
        archives_button.pack(side=tk.LEFT, padx=5)
    
    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter a new task:")
        if task and task.strip():
            self.tasks.append(task.strip())
            self.update_task_display()
            self.save_data()
    
    def delete_task(self):
        try:
            selected_idx = self.tasks_listbox.curselection()[0]
            task = self.tasks[selected_idx]
            if messagebox.askyesno("Confirm Delete", f"Delete task: {task}?"):
                del self.tasks[selected_idx]
                self.update_task_display()
                self.save_data()
        except IndexError:
            messagebox.showinfo("No Selection", "Please select a task to delete.")
    
    def mark_complete(self):
        try:
            selected_idx = self.tasks_listbox.curselection()[0]
            task = self.tasks[selected_idx]
            self.completed_tasks.append(task)
            del self.tasks[selected_idx]
            self.update_all_displays()
            self.save_data()
        except IndexError:
            messagebox.showinfo("No Selection", "Please select a task to mark as complete.")
    
    def move_incomplete_tasks(self):
        """Automatically move tasks to incomplete section"""
        if not self.tasks:  # No tasks to move
            return
            
        # Ask for confirmation
        if messagebox.askyesno("Move Incomplete Tasks", 
                              f"Move {len(self.tasks)} tasks to the incomplete section?"):
            # Move all current tasks to incomplete
            self.incomplete_tasks.extend(self.tasks)
            self.tasks = []
            self.update_all_displays()
            self.save_data()
            messagebox.showinfo("Tasks Moved", "All tasks have been moved to incomplete section.")
    
    def move_back_to_tasks(self):
        """Move a task from incomplete back to today's tasks"""
        try:
            selected_idx = self.incomplete_listbox.curselection()[0]
            task = self.incomplete_tasks[selected_idx]
            self.tasks.append(task)
            del self.incomplete_tasks[selected_idx]
            self.update_all_displays()
            self.save_data()
        except IndexError:
            messagebox.showinfo("No Selection", "Please select a task to move back.")
    
    def update_task_display(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.tasks_listbox.insert(tk.END, task)
    
    def update_completed_display(self):
        self.completed_listbox.delete(0, tk.END)
        for task in self.completed_tasks:
            self.completed_listbox.insert(tk.END, task)
    
    def update_incomplete_display(self):
        self.incomplete_listbox.delete(0, tk.END)
        for task in self.incomplete_tasks:
            self.incomplete_listbox.insert(tk.END, task)
    
    def update_all_displays(self):
        self.update_task_display()
        self.update_completed_display()
        self.update_incomplete_display()
    
    def save_data(self):
        data = {
            "tasks": self.tasks,
            "completed_tasks": self.completed_tasks,
            "incomplete_tasks": self.incomplete_tasks,
            "last_saved": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(self.data_file, "w") as file:
            json.dump(data, file, indent=4)
        
        messagebox.showinfo("Success", "Tasks saved successfully!")
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as file:
                    data = json.load(file)
                    
                self.tasks = data.get("tasks", [])
                self.completed_tasks = data.get("completed_tasks", [])
                self.incomplete_tasks = data.get("incomplete_tasks", [])
            except:
                messagebox.showwarning("Error", "Failed to load previous data.")
    
    def start_new_day(self):
        """Start a new day by clearing all lists and saving archive"""
        if messagebox.askyesno("Start New Day", "This will archive current tasks and start fresh. Continue?"):
            # First move all uncompleted tasks to the incomplete section
            if self.tasks:
                self.incomplete_tasks.extend(self.tasks)
                self.tasks = []
            
            # Archive current day if needed
            self.archive_current_day()
            
            # Clear completed tasks but keep the incomplete ones
            previously_incomplete = self.incomplete_tasks.copy()
            self.completed_tasks = []
            self.incomplete_tasks = []
            
            # Ask if user wants to bring back incomplete tasks
            if previously_incomplete and messagebox.askyesno("Incomplete Tasks", 
                                                           f"You have {len(previously_incomplete)} incomplete tasks. Would you like to add them to today's tasks?"):
                self.tasks = previously_incomplete
            
            self.update_all_displays()
            self.save_data()
            messagebox.showinfo("New Day", "Ready for a new day! Add your tasks.")
    
    def archive_current_day(self):
        """Archive the current day's data"""
        if not (self.tasks or self.completed_tasks or self.incomplete_tasks):
            return  # Nothing to archive
            
        today = datetime.now().strftime("%Y-%m-%d")
        archive_dir = "task_archives"
        
        # Create archives directory if it doesn't exist
        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)
        
        # Create archive data
        archive_data = {
            "date": today,
            "tasks": self.tasks,
            "completed_tasks": self.completed_tasks,
            "incomplete_tasks": self.incomplete_tasks,
            "summary": {
                "total": len(self.tasks) + len(self.completed_tasks) + len(self.incomplete_tasks),
                "completed": len(self.completed_tasks),
                "incomplete": len(self.incomplete_tasks) + len(self.tasks)
            }
        }
        
        # Save archive
        archive_file = os.path.join(archive_dir, f"tasks_{today}.json")
        with open(archive_file, "w") as file:
            json.dump(archive_data, file, indent=4)


    def open_archives_viewer(self):
        """Open a window to view archived tasks"""
        archive_dir = "task_archives"
        
        # Check if archive directory exists
        if not os.path.exists(archive_dir):
            messagebox.showinfo("No Archives", "No archived tasks found.")
            return
            
        # Get list of archive files
        archive_files = []
        for file in os.listdir(archive_dir):
            if file.endswith(".json") and file.startswith("tasks_"):
                archive_files.append(file)
                
        if not archive_files:
            messagebox.showinfo("No Archives", "No archived tasks found.")
            return
            
        # Sort archives by date (newest first)
        archive_files.sort(reverse=True)
        
        # Create archive viewer window
        archive_window = tk.Toplevel(self.root)
        archive_window.title("Task Archives")
        archive_window.geometry("800x600")
        archive_window.configure(bg="#f5f5f5")
        
        # Create header
        header_frame = tk.Frame(archive_window, bg="#4a6fa5", pady=10)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame, 
            text="Task Archives",
            font=("Arial", 16, "bold"),
            bg="#4a6fa5",
            fg="white"
        )
        title_label.pack()
        
        # Create main content frame
        content_frame = tk.Frame(archive_window, bg="#f5f5f5", padx=10, pady=10)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create left panel with dates
        left_frame = tk.Frame(content_frame, bg="#f5f5f5", width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        date_label = tk.Label(left_frame, text="Select Date:", font=("Arial", 12), bg="#f5f5f5")
        date_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Create listbox with dates
        date_frame = tk.Frame(left_frame)
        date_frame.pack(fill=tk.BOTH, expand=True)
        
        dates_listbox = tk.Listbox(
            date_frame,
            selectmode=tk.SINGLE,
            bg="white",
            font=("Arial", 10),
            width=25
        )
        dates_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        dates_scrollbar = tk.Scrollbar(date_frame)
        dates_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        dates_listbox.config(yscrollcommand=dates_scrollbar.set)
        dates_scrollbar.config(command=dates_listbox.yview)
        
        # Create right panel with task details
        right_frame = tk.Frame(content_frame, bg="#f5f5f5")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create notebook for task categories
        task_notebook = ttk.Notebook(right_frame)
        task_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs for different task categories
        pending_tab = tk.Frame(task_notebook, bg="#f5f5f5")
        completed_tab = tk.Frame(task_notebook, bg="#efffef")
        incomplete_tab = tk.Frame(task_notebook, bg="#ffefef")
        
        task_notebook.add(pending_tab, text="Pending Tasks")
        task_notebook.add(completed_tab, text="Completed Tasks")
        task_notebook.add(incomplete_tab, text="Incomplete Tasks")
        
        # Create listboxes for each category
        pending_listbox = tk.Listbox(pending_tab, bg="white", font=("Arial", 10))
        pending_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        completed_listbox = tk.Listbox(completed_tab, bg="#efffef", font=("Arial", 10))
        completed_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        incomplete_listbox = tk.Listbox(incomplete_tab, bg="#ffefef", font=("Arial", 10))
        incomplete_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add summary frame at the bottom
        summary_frame = tk.LabelFrame(right_frame, text="Summary", font=("Arial", 12), bg="#f5f5f5", padx=10, pady=10)
        summary_frame.pack(fill=tk.X, pady=(10, 0))
        
        summary_label = tk.Label(summary_frame, text="", font=("Arial", 10), bg="#f5f5f5")
        summary_label.pack(fill=tk.X)
        
        # Populate the dates listbox
        for file in archive_files:
            # Extract date from filename (tasks_YYYY-MM-DD.json)
            date_str = file[6:-5]
            try:
                # Format date for display (e.g., "Monday, January 1, 2024")
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                display_date = date_obj.strftime("%A, %B %d, %Y")
                dates_listbox.insert(tk.END, display_date)
            except:
                # If date parsing fails, just show the raw date string
                dates_listbox.insert(tk.END, date_str)
        
        # Function to load archive data when a date is selected
        def load_archive_data(event):
            selection = dates_listbox.curselection()
            if not selection:
                return
                
            index = selection[0]
            file_name = archive_files[index]
            file_path = os.path.join(archive_dir, file_name)
            
            try:
                with open(file_path, "r") as file:
                    archive_data = json.load(file)
                    
                # Clear existing data in listboxes
                pending_listbox.delete(0, tk.END)
                completed_listbox.delete(0, tk.END)
                incomplete_listbox.delete(0, tk.END)
                
                # Populate listboxes with archive data
                for task in archive_data.get("tasks", []):
                    pending_listbox.insert(tk.END, task)
                    
                for task in archive_data.get("completed_tasks", []):
                    completed_listbox.insert(tk.END, task)
                    
                for task in archive_data.get("incomplete_tasks", []):
                    incomplete_listbox.insert(tk.END, task)
                
                # Update summary
                summary_dict = archive_data.get("summary", {})
                if summary_dict:
                    total = summary_dict.get("total", 0)
                    completed = summary_dict.get("completed", 0)
                    incomplete = summary_dict.get("incomplete", 0)
                    completion_rate = (completed / total * 100) if total > 0 else 0
                    
                    summary_text = f"Total Tasks: {total}  |  Completed: {completed}  |  " \
                                   f"Incomplete: {incomplete}  |  Completion Rate: {completion_rate:.1f}%"
                else:
                    # Calculate summary if not available in archive
                    total = len(archive_data.get("tasks", [])) + \
                           len(archive_data.get("completed_tasks", [])) + \
                           len(archive_data.get("incomplete_tasks", []))
                    completed = len(archive_data.get("completed_tasks", []))
                    incomplete = len(archive_data.get("tasks", [])) + \
                                len(archive_data.get("incomplete_tasks", []))
                    completion_rate = (completed / total * 100) if total > 0 else 0
                    
                    summary_text = f"Total Tasks: {total}  |  Completed: {completed}  |  " \
                                   f"Incomplete: {incomplete}  |  Completion Rate: {completion_rate:.1f}%"
                
                summary_label.config(text=summary_text)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load archive: {e}")
        
        # Bind selection event
        dates_listbox.bind("<<ListboxSelect>>", load_archive_data)
        
        # Add export button
        export_button = tk.Button(
            left_frame,
            text="Export Selected Archive",
            command=lambda: self.export_archive(archive_dir, archive_files, dates_listbox.curselection()),
            bg="#4a6fa5",
            fg="white",
            padx=10
        )
        export_button.pack(pady=10)
        
        # Select the first date by default if available
        if archive_files:
            dates_listbox.select_set(0)
            dates_listbox.event_generate("<<ListboxSelect>>")
    
    def export_archive(self, archive_dir, archive_files, selection):
        """Export selected archive to a user-selected location"""
        if not selection:
            messagebox.showinfo("No Selection", "Please select an archive to export.")
            return
            
        index = selection[0]
        file_name = archive_files[index]
        file_path = os.path.join(archive_dir, file_name)
        
        # Get destination file path
        dest_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=file_name
        )
        
        if not dest_path:
            return  # User cancelled
            
        try:
            # Copy file to destination
            with open(file_path, "r") as src_file:
                archive_data = json.load(src_file)
                
            with open(dest_path, "w") as dest_file:
                json.dump(archive_data, dest_file, indent=4)
                
            messagebox.showinfo("Export Successful", f"Archive exported to {dest_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export archive: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DailyTaskManager(root)
    root.mainloop()