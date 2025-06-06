from database import create_tables
import tkinter as tk
import webbrowser
from user_registration import UserRegistrationApp
from attendance import AttendanceApp
from report import ReportApp
from PIL import Image, ImageTk
import os
import tkinter as tk
from user_registration import UserRegistrationApp
from attendance import AttendanceApp
from report import ReportApp
from database import get_all_users, delete_user

class AdministrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Administration")
        self.root.geometry("300x150")

        self.show_button = tk.Button(root, text="Show Attendance", width=20, command=self.show_attendance)
        self.show_button.pack(pady=10)

        self.delete_button = tk.Button(root, text="Delete User", width=20, command=self.delete_user)
        self.delete_button.pack(pady=10)

    def show_attendance(self):
        self.new_window = tk.Toplevel(self.root)
        ReportApp(self.new_window)

    def delete_user(self):
        self.new_window = tk.Toplevel(self.root)
        UserDeletionApp(self.new_window)

class ContactUsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Us")
        self.root.geometry("300x150")

        self.email_button = tk.Button(root, text="Email: support@example.com", width=30, command=self.open_email)
        self.email_button.pack(pady=10)

        self.phone_button = tk.Button(root, text="Phone: +1-234-567-890", width=30, command=self.show_phone)
        self.phone_button.pack(pady=10)

    def open_email(self):
        import webbrowser
        webbrowser.open("mailto:support@example.com")

    def show_phone(self):
        tk.messagebox.showinfo("Phone", "Call us at +1-234-567-890")

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("600x250")

        # Frame to hold buttons horizontally
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        # Load logos for buttons
        logo_paths = [
            "C:/Users/shres/OneDrive/Desktop/logo/1.jpg",
            "C:/Users/shres/OneDrive/Desktop/logo/2.png",
            "C:/Users/shres/OneDrive/Desktop/logo/3.png",
            "C:/Users/shres/OneDrive/Desktop/logo/4.jpeg",
            "C:/Users/shres/OneDrive/Desktop/logo/5.jpg"
        ]
        self.logos = []
        for path in logo_paths:
            img = Image.open(path)
            img = img.resize((50, 50), Image.LANCZOS)
            self.logos.append(ImageTk.PhotoImage(img))

        # Create buttons with logos and labels below
        self.register_button = tk.Button(self.button_frame, image=self.logos[0], command=self.open_registration)
        self.register_button.grid(row=0, column=0, padx=10)
        self.register_label = tk.Label(self.button_frame, text="Register New User")
        self.register_label.grid(row=1, column=0)

        self.attendance_button = tk.Button(self.button_frame, image=self.logos[1], command=self.open_attendance)
        self.attendance_button.grid(row=0, column=1, padx=10)
        self.attendance_label = tk.Label(self.button_frame, text="Mark Attendance")
        self.attendance_label.grid(row=1, column=1)

        self.report_button = tk.Button(self.button_frame, image=self.logos[2], command=self.open_reports)
        self.report_button.grid(row=0, column=2, padx=10)
        self.report_label = tk.Label(self.button_frame, text="View Attendance Reports")
        self.report_label.grid(row=1, column=2)

        self.admin_button = tk.Button(self.button_frame, image=self.logos[3], command=self.open_administration)
        self.admin_button.grid(row=0, column=3, padx=10)
        self.admin_label = tk.Label(self.button_frame, text="Administration")
        self.admin_label.grid(row=1, column=3)

        self.contact_button = tk.Button(self.button_frame, image=self.logos[4], command=self.open_contact_us)
        self.contact_button.grid(row=0, column=4, padx=10)
        self.contact_label = tk.Label(self.button_frame, text="Contact Us")
        self.contact_label.grid(row=1, column=4)

    def open_registration(self):
        self.new_window = tk.Toplevel(self.root)
        UserRegistrationApp(self.new_window)

    def open_attendance(self):
        self.new_window = tk.Toplevel(self.root)
        AttendanceApp(self.new_window)

    def open_reports(self):
        self.new_window = tk.Toplevel(self.root)
        ReportApp(self.new_window)

    def open_administration(self):
        self.new_window = tk.Toplevel(self.root)
        AdministrationApp(self.new_window)

    def open_contact_us(self):
        self.new_window = tk.Toplevel(self.root)
        ContactUsApp(self.new_window)

    def open_registration(self):
        self.new_window = tk.Toplevel(self.root)
        UserRegistrationApp(self.new_window)

    def open_contact_us(self):
        self.new_window = tk.Toplevel(self.root)
        ContactUsApp(self.new_window)

    def open_attendance(self):
        self.new_window = tk.Toplevel(self.root)
        AttendanceApp(self.new_window)

    def open_reports(self):
        self.new_window = tk.Toplevel(self.root)
        ReportApp(self.new_window)

    def open_administration(self):
        self.new_window = tk.Toplevel(self.root)
        AdministrationApp(self.new_window)

class UserDeletionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Delete User")
        self.root.geometry("400x300")

        self.user_listbox = tk.Listbox(root, width=50)
        self.user_listbox.pack(pady=10)

        self.delete_button = tk.Button(root, text="Delete Selected User", command=self.delete_selected_user)
        self.delete_button.pack(pady=10)

        self.load_users()

    def load_users(self):
        self.user_listbox.delete(0, tk.END)
        users = get_all_users()
        for user in users:
            self.user_listbox.insert(tk.END, f"{user[0]}: {user[1]}")

    def delete_selected_user(self):
        selected = self.user_listbox.curselection()
        if not selected:
            tk.messagebox.showerror("Error", "No user selected")
            return
        user_info = self.user_listbox.get(selected[0])
        user_id = int(user_info.split(":")[0])
        delete_user(user_id)
        tk.messagebox.showinfo("Success", "User deleted successfully")
        self.load_users()

if __name__ == "__main__":
    create_tables()
    root = tk.Tk()
    from landing_page import LandingPage
    app = LandingPage(root)
    root.mainloop()
