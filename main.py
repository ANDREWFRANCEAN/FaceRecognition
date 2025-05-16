# Import necessary libraries
import cv2                          # For webcam access and image processing
import os                           # For file and folder handling
import numpy as np                  # For numerical operations
from deepface import DeepFace       # Face recognition and embedding extraction
from numpy.linalg import norm       # Used to calculate Euclidean distance
from tkinter import *               # GUI library
from PIL import Image, ImageTk      # For displaying OpenCV frames in Tkinter
import subprocess                   # To open external Windows applications

# Path to authorized face images
AUTHORIZED_FOLDER = "auth"

# Threshold for Euclidean distance comparison — smaller = stricter
THRESHOLD = 10

# Global list to store authorized face embeddings
known_faces = []

# Calculate the Euclidean distance between two face embeddings
def euclidean_distance(emb1, emb2):
    return norm(np.array(emb1) - np.array(emb2))  # Smaller distance = more similar faces

# Load all authorized faces from the 'auth' folder and extract their embeddings
def load_authorized_faces():
    global known_faces
    known_faces = []

    for file in os.listdir(AUTHORIZED_FOLDER):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(AUTHORIZED_FOLDER, file)
            try:
                # Get 128D embedding using FaceNet
                embedding = DeepFace.represent(
                    img_path=path,
                    model_name="Facenet", #model name to train the auth pics
                    detector_backend="opencv",
                    enforce_detection=True
                )[0]["embedding"]

                known_faces.append({
                    "name": file,
                    "embedding": embedding
                })
                print(f"Embedded: {file}")  # Log loaded face
            except Exception as e:
                print(f"Failed to process {file}: {e}")

# Function to launch a Windows app (here: Notepad)
def unlock_windows_app():
    subprocess.Popen(["notepad.exe"])  # Replace with any app path you want to unlock

# Check if the face from the webcam matches any authorized face
def is_face_recognized(frame):
    try:
        # Generate embedding from the live webcam frame
        rep = DeepFace.represent(
            img_path=frame,
            model_name="Facenet",
            detector_backend="opencv",
            enforce_detection=True
        )

        if len(rep) == 0:
            return "No face detected"

        target_embedding = rep[0]["embedding"]

        # Compare current embedding with each authorized face
        for face in known_faces:
            distance = euclidean_distance(target_embedding, face["embedding"])
            print(f"🔍 Comparing to {face['name']} | Distance: {distance:.4f}")

            if distance < THRESHOLD:
                unlock_windows_app()  # Launch the app if match found
                return f"Access granted to: {face['name']}"

        return "Access denied (no match)"  # No face matched

    except Exception as e:
        print("Verification error:", e)
        return "Error verifying face"

# Start webcam
cap = cv2.VideoCapture(0)

# Create GUI window
root = Tk()
root.title("Face Recognition App")
root.geometry("800x600")
root.configure(bg="#1c1c1c")

# Title label
label = Label(root, text="Face Recognition System", font=("Helvetica", 24), fg="white", bg="#1c1")
label.pack(pady=10)

# Live video frame
video_label = Label(root)
video_label.pack()

# Label to display result messages
result_label = Label(root, text="", font=("Helvetica", 18), fg="white", bg="#1c1c1c")
result_label.pack(pady=20)

# Function to update live webcam feed in the GUI
def update_frame():
    ret, frame = cap.read()
    if ret:
        # Convert frame to RGB and display it
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    video_label.after(10, update_frame)  # Repeat every 10ms

# Run face recognition when the button is clicked
def verify_from_webcam():
    ret, frame = cap.read()
    if ret:
        result_label.config(text="Verifying...")
        root.update()
        msg = is_face_recognized(frame)
        result_label.config(text=msg)

# Create and place the Verify button
verify_button = Button(
    root,
    text="Verify Face",
    command=verify_from_webcam,
    font=("Helvetica", 16, "bold"),
    bg="#444",
    fg="white",
    width=22,
    height=2,
    padx=20,
    pady=10
)
verify_button.pack(pady=(10, 1), anchor="n")

# Load known faces and start video stream
load_authorized_faces()
update_frame()

# Start the GUI event loop
root.mainloop()

# Release camera and close any OpenCV windows on exit
cap.release()
cv2.destroyAllWindows()
