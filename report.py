import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from database import get_attendance_records

class ReportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Reports")
        self.root.geometry("700x500")

        self.records_listbox = tk.Listbox(root, width=80, height=20)
        self.records_listbox.pack()

        self.export_button = tk.Button(root, text="Export to CSV", command=self.export_csv)
        self.export_button.pack()

        self.load_records()

    def load_records(self):
        self.records_listbox.delete(0, tk.END)
        records = get_attendance_records()
        for name, timestamp in records:
            self.records_listbox.insert(tk.END, f"{timestamp} - {name}")

    def export_csv(self):
        records = get_attendance_records()
        if not records:
            messagebox.showinfo("Info", "No attendance records to export.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "User Name"])
                for name, timestamp in records:
                    writer.writerow([timestamp, name])
            messagebox.showinfo("Success", f"Attendance report exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReportApp(root)
    root.mainloop()
