import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk

# Function to record attendance in CSV
def record_attendance(name):
    if name in students:
        students.remove(name)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        with open(f"{current_date}.csv", "a", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([name, current_time])
        recorded_names.append(name)
        update_display(f"{name} is present.")

# Function to update GUI display
def update_display(message):
    display_label.config(text=message)

# Function to start and stop face recognition
def toggle_recognition():
    global recognition_active
    if recognition_active:
        # Stop recognition
        recognition_active = False
        start_stop_button.config(text="Start Recognition", bg="#4CAF50")  # Green color
    else:
        # Start recognition
        recognition_active = True
        start_stop_button.config(text="Stop Recognition", bg="#f44336")  # Red color
        check_attendance()

# Correct the typo in cv2.VideoCapture
video_capture = cv2.VideoCapture(0)

abhay_image = face_recognition.load_image_file("faces/abhay.JPG")
abhay_encoding = face_recognition.face_encodings(abhay_image)[0]

aman_image = face_recognition.load_image_file("faces/aman.jpg")
aman_encoding = face_recognition.face_encodings(aman_image)[0]

amit_virmani_image = face_recognition.load_image_file("faces/Amit-Virmani.jpg")
amit_virmani_encoding = face_recognition.face_encodings(amit_virmani_image)[0]

dr_rabins_porwal_image = face_recognition.load_image_file("faces/Dr_Rabins_Porwal.jpg")
dr_rabins_porwal_encoding = face_recognition.face_encodings(dr_rabins_porwal_image)[0]

mamta_mayee_panda_image = face_recognition.load_image_file("faces/Mamta-Mayee-Panda.jpg")
mamta_mayee_panda_encoding = face_recognition.face_encodings(mamta_mayee_panda_image)[0]

mamta_tiwari_image = face_recognition.load_image_file("faces/Mamta-Tiwari.jpg")
mamta_tiwari_encoding = face_recognition.face_encodings(mamta_tiwari_image)[0]

prashant_srivastava_image = face_recognition.load_image_file("faces/Prashant-Srivastava.jpg")
prashant_srivastava_encoding = face_recognition.face_encodings(prashant_srivastava_image)[0]

pushpa_mamoria_image = face_recognition.load_image_file("faces/Pushpa-Mamoria.jpg")
pushpa_mamoria_encoding = face_recognition.face_encodings(pushpa_mamoria_image)[0]

abhay_pratap_image = face_recognition.load_image_file("faces/abhay_pratap.jpg")
abhay_pratap_encoding = face_recognition.face_encodings(abhay_pratap_image)[0]



known_face_encoding = [
    abhay_encoding, aman_encoding, amit_virmani_encoding, dr_rabins_porwal_encoding,
    mamta_mayee_panda_encoding, mamta_tiwari_encoding, prashant_srivastava_encoding,
    pushpa_mamoria_encoding, abhay_pratap_encoding ]
known_face_names = [
    "abhay", "aman", "amit_virmani", "dr_rabins_porwal", "mamta_mayee_panda",
    "mamta_tiwari", "prashant_srivastava", "pushpa_mamoria", "abhay_pratap"
]
students = known_face_names.copy()

face_locations = []
face_encodings = []
recorded_names = []  # Keep track of recorded names

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

# Correct the file writing mode and add a header to the CSV file
with open(f"{current_date}.csv", "w", newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["Name", "Time"])

# Create the tkinter GUI window
root = tk.Tk()
root.title("Continuous Attendance Tracking")

# Load background image
background_image = Image.open("faces/wallpaperflare.com_wallpaper (7).jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Create a label to hold the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Set window background color
root.configure(bg="#f0f0f0")  # Light gray background

# Determine screen size and set GUI size to 1/4 of the screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
gui_width = screen_width
gui_height = screen_height
root.geometry(f"{gui_width}x{gui_height}")

# Create a label for displaying attendance status
display_label = tk.Label(root, text="Attendance status will be displayed here.", bg="#f0f0f0", fg="#333", font=("Helvetica", 14))
display_label.pack(pady=20)

# Create a button to start/stop recognition
recognition_active = False
start_stop_button = tk.Button(root, text="Start Recognition", bg="#4CAF50", fg="white", font=("Helvetica", 14), command=toggle_recognition)
start_stop_button.pack(pady=10)

# Function to continuously check attendance
def check_attendance():
    if recognition_active:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Initialize name variable outside the loop
        name = ""

        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                if name not in recorded_names:
                    record_attendance(name)

                # Draw green rectangle around the face
                cv2.rectangle(frame, (left * 4, top * 4), (right * 4, bottom * 4), (0, 255, 0), 2)

        cv2.imshow("Attendance", frame)

        if name in known_face_names:
            font = cv2.FONT_ITALIC
            bottomLeftCornerOfText = (10, 100)
            fontScale = 1.5
            fontColor = (30, 30, 30)
            thickness = 3
            lineType = 2
            cv2.putText(frame, name + " Present", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)
            if name in students:
                record_attendance(name)

        cv2.imshow("Attendance", frame)
        root.after(100, check_attendance)  # Schedule the function to run again after 100 milliseconds

# Run the tkinter main loop
root.mainloop()
