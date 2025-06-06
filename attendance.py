import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime
from database import get_face_encodings, mark_attendance, get_all_users
from face_recognition_module import detect_faces, get_face_encodings as get_encodings, compare_faces, deserialize_encoding

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance - Face Recognition System")
        self.root.geometry("900x700")

        self.start_button = tk.Button(root, text="Start Recognition", command=self.start_camera)
        self.error_label = tk.Label(root, text="", fg="red")
        self.error_label.pack()
        self.start_button.pack()

        self.video_label = tk.Label(root)
        self.video_label.pack()

        self.attendance_listbox = tk.Listbox(root, width=50, height=15)
        self.attendance_listbox.pack()

        self.cap = None
        self.current_frame = None
        self.known_encodings = []
        self.known_user_ids = []
        self.users = {}
        self.recognized_users = set()
        self.running = False

        self.load_known_faces()

    def load_known_faces(self):
        encodings_data = get_face_encodings()
        self.known_encodings = []
        self.known_user_ids = []
        for user_id, encoding_blob in encodings_data:
            encoding = deserialize_encoding(encoding_blob)
            self.known_encodings.append(encoding)
            self.known_user_ids.append(user_id)
        users = get_all_users()
        self.users = {user_id: name for user_id, name in users}

    def start_camera(self):
        # Try multiple webcam indices to improve reliability
        for index in range(3):
            self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if self.cap.isOpened():
                self.error_label.config(text=f"Webcam opened at index {index}")
                break
            else:
                self.cap.release()
                self.cap = None
        if not self.cap or not self.cap.isOpened():
            self.error_label.config(text="Cannot open webcam")
            return
        self.running = True
        self.update_frame()

    def update_frame(self):
        if not self.running:
            return
        ret, frame = self.cap.read()
        if not ret:
            self.error_label.config(text="Failed to grab frame from webcam, retrying...")
            # Retry after short delay instead of stopping camera
            self.root.after(100, self.update_frame)
            return
        self.current_frame = frame.copy()
        faces = detect_faces(frame)
        encodings = get_encodings(frame, faces)
        for i, encoding in enumerate(encodings):
            if len(self.known_encodings) == 0:
                # No known encodings to compare with, skip recognition
                continue
            match, index, distance = compare_faces(np.array(self.known_encodings), encoding)
            if match:
                user_id = self.known_user_ids[index]
                name = self.users.get(user_id, "Unknown")
                x1, y1, x2, y2 = faces[i].left(), faces[i].top(), faces[i].right(), faces[i].bottom()
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                if user_id not in self.recognized_users:
                    mark_attendance(user_id)
                    self.recognized_users.add(user_id)
                    self.attendance_listbox.insert(tk.END, f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {name}")
                    # Show message box after marking attendance
                    messagebox.showinfo("Attendance", "Attendance is marked")
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        self.root.after(30, self.update_frame)

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None

    def on_closing(self):
        self.stop_camera()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
