# DeepFace-Based Face Authentication System

This Python project uses the [DeepFace](https://github.com/serengil/deepface) library to grant or deny access to a specific Windows application (e.g. Notepad) based on facial recognition. It includes a live webcam interface built with Tkinter.

# Features
-  Face Authentication using images stored in an `auth/` folder  
- Live webcam feed in a GUI with a "Verify Face" button  
- Realtime face embedding and comparison using the **FaceNet** model  
- Access granted by launching a Windows app if a match is found  
- Retrains authorized embeddings every time the app is launched  

## Project Structure
face-auth-app/
│
├── auth/ # Folder with authorized user face images
│ ├── 1.jpg
│ └── 2.jpg
│
├── main.py # Main face authentication script
├── requirements.txt # Python dependencies
└── README.md # This file

##  How It Works
1. Add one or more clear images of authorized users in the `auth/` folder.  
2. Run the app using:
   ```bash
   python main.py
The GUI will launch with a live webcam feed.

Click "Verify Face" to scan the live frame and compare it with authorized embeddings.

If a match is found (within a certain distance threshold), Notepad (notepad.exe) will be launched.

If no match is found, access is denied.

## Install dependencies using:

bash
Copy
Edit
pip install -r requirements.txt
requirements.txt:

Copy
Edit
opencv-python
deepface
numpy
Pillow


---

Let me know if you want the file generated for download or want to turn this into a GitHub template project.
