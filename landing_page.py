 #test save
import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import os
from user_registration import UserRegistrationApp
from attendance import AttendanceApp
from report import ReportApp
from database import create_tables
from database import get_all_users, delete_user
from main import UserDeletionApp

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

        self.email_button = tk.Button(root, text="Email: shrestspalaz123456@gmail.com", width=30, command=self.open_email)
        self.email_button.pack(pady=10)

        self.phone_button = tk.Button(root, text="Phone: +1-234-567-890", width=30, command=self.show_phone)
        self.phone_button.pack(pady=10)

    def open_email(self):
        import webbrowser
        webbrowser.open("mailto:shrestspalaz123456@gmail.com")

    def show_phone(self):
        tk.messagebox.showinfo("Phone", "Call us at +1-234-567-890")

class LandingPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Landing Page")
        self.root.geometry("600x400") 
        bg_path = "C:/Users/shres/OneDrive/Desktop/logo/6.jpg"
        bg_image = Image.open(bg_path).convert("RGBA")
        enhancer = ImageEnhance.Brightness(bg_image)
        bg_image = enhancer.enhance(0.5)  # 30% brightness to simulate 30% visibility
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.background_label = tk.Label(root, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.lower()





        # Load logo image
        logo_path = "C:/Users/shres/OneDrive/Desktop/Face recognization Attendance System/college_images/csjmu-emplem.png"
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((150, 150), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_image)

        # Display logo
        self.logo_label = tk.Label(root, image=self.logo_photo)
        self.logo_label.pack(pady=20)

        # Display title text
        self.title_label = tk.Label(root, text="Automated Attendance Management System\nusing Face Recognition", font=("Arial", 16), justify="center")
        self.title_label.pack(pady=10)

        # Frame to hold buttons horizontally at bottom
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.BOTTOM, pady=20)

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
            img = img.resize((140, 140), Image.LANCZOS)
            self.logos.append(ImageTk.PhotoImage(img))

        # Create buttons with logos and labels below with bold font for labels
        self.register_button = tk.Button(self.button_frame, image=self.logos[0], command=self.open_registration, width=140, height=140, borderwidth=0, highlightthickness=0)
        self.register_button.grid(row=0, column=0, padx=10)
        self.register_label = tk.Label(self.button_frame, text="Register New User", font=("Arial", 10, "bold"))
        self.register_label.grid(row=1, column=0)

        self.attendance_button = tk.Button(self.button_frame, image=self.logos[1], command=self.open_attendance, width=140, height=140)
        self.attendance_button.grid(row=0, column=1, padx=10)
        self.attendance_label = tk.Label(self.button_frame, text="Mark Attendance", font=("Arial", 10, "bold"))
        self.attendance_label.grid(row=1, column=1)

        self.report_button = tk.Button(self.button_frame, image=self.logos[2], command=self.open_reports, width=140, height=140)
        self.report_button.grid(row=0, column=2, padx=10)
        self.report_label = tk.Label(self.button_frame, text="View Attendance Reports", font=("Arial", 10, "bold"))
        self.report_label.grid(row=1, column=2)

        self.admin_button = tk.Button(self.button_frame, image=self.logos[3], command=self.open_administration, width=140, height=140)
        self.admin_button.grid(row=0, column=3, padx=10)
        self.admin_label = tk.Label(self.button_frame, text="Administration", font=("Arial", 10, "bold"))
        self.admin_label.grid(row=1, column=3)

        self.contact_button = tk.Button(self.button_frame, image=self.logos[4], command=self.open_contact_us, width=140, height=140)
        self.contact_button.grid(row=0, column=4, padx=10)
        self.contact_label = tk.Label(self.button_frame, text="Contact Us", font=("Arial", 10, "bold"))
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

if __name__ == "__main__":
    create_tables()
    root = tk.Tk()
    app = LandingPage(root)
    root.mainloop()
