import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from pyt import detect

def browsefunc(ent):
    filename = askopenfilename(filetypes=[
        ("image files", "*.jpeg;*.png;*.jpg"),
        ("all files", "*.*")
    ])
    if filename:
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)

def capture_image_from_cam_into_temp():
    cam = cv2.VideoCapture(0, cv2.CAP_ANY)
    cv2.namedWindow("Capturing Image")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow("Capturing Image", frame)

        k = cv2.waitKey(1)
        if k == 27:  # ESC key
            print("Escape hit, closing...")
            break
        elif k == 32:  # Space key
            if not os.path.isdir('temp'):
                os.mkdir('temp')

            img_name = "./temp/test_img1.png"
            print('imwrite=', cv2.imwrite(img_name, frame))
            print(f"{img_name} written!")
            break
    cam.release()
    cv2.destroyAllWindows()
    return True

def capture_image(ent):
    filename = os.path.join(os.getcwd(), 'temp', 'test_img1.png')
    res = messagebox.askquestion('Click Picture', 'Press Space Bar to click picture and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp()
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
    return True

def check(window, path1):
    if not os.path.isfile(path1):
        messagebox.showerror("File Not Found", "Selected file does not exist.")
        return False

    detected_objects = detect(path1)
    if not detected_objects:
        messagebox.showinfo("No Objects", "No objects detected in the image.")
        return False

    # Load the original image
    original_image = cv2.imread(path1)

    # Resize the image to fit half of the screen width
    target_width = int(window.winfo_screenwidth() / 3)
    aspect_ratio = original_image.shape[1] / original_image.shape[0]
    target_height = int(target_width / aspect_ratio)
    resized_image = cv2.resize(original_image, (target_width, target_height))

    for obj in detected_objects:
        class_id = obj["Object type"]
        cords = obj["Coordinates"]
        conf = obj["Probability"]

        # Resize bounding box coordinates to match the resized image
        cords = [int(c * (target_width / original_image.shape[1])) for c in cords]

        # Draw bounding box and label on the resized image
        cv2.rectangle(resized_image, (cords[0], cords[1]), (cords[2], cords[3]), (0, 255, 0), 2)
        label = f"{class_id}: {conf}"
        cv2.putText(resized_image, label, (cords[0], cords[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the resized image with bounding boxes and labels
    cv2.imshow("Object Detection", resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True


def live_detection():
    GREEN = (0, 255, 0)
    FONT_SCALE = 0.5
    def detect_objects(frame):
        # Perform object detection on the frame
        detected_objects = detect(frame)
        for obj in detected_objects:
            class_id = obj["Object type"]
            cords = obj["Coordinates"]
            conf = obj["Probability"]

            # Draw bounding box and label on the frame
            cv2.rectangle(frame, (cords[0], cords[1]), (cords[2], cords[3]), GREEN, 2)
            label = f"{class_id}: {conf}"
            cv2.putText(frame, label, (cords[0], cords[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, GREEN, 2)

    cam = cv2.VideoCapture(0, cv2.CAP_ANY)

    if not cam.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Detect and display objects
        frame = cv2.flip(frame, 1)
        detect_objects(frame)

        # Display the frame with bounding boxes and labels
        cv2.imshow("Live Detection", frame)

        k = cv2.waitKey(1)
        if k == 27:
            # ESC key
            print("Escape hit, closing...")
            break

    # Release the camera at the end
    cam.release()
    cv2.destroyAllWindows()
    return True


root = tk.Tk()
root.title("Object detection")
root.geometry("500x700")

uname_label = tk.Label(root, text="Object detection:", font=10)
uname_label.place(x=90, y=50)

img1_message = tk.Label(root, text="Insert image", font=10)
img1_message.place(x=10, y=120)

image1_path_entry = tk.Entry(root, font=10)
image1_path_entry.place(x=150, y=120)

img1_capture_button = tk.Button(root, text="Capture", font=10, command=lambda: capture_image(ent=image1_path_entry))
img1_capture_button.place(x=400, y=90)

img1_browse_button = tk.Button(root, text="Browse", font=10, command=lambda: browsefunc(ent=image1_path_entry))
img1_browse_button.place(x=400, y=140)

live_button = tk.Button(root, text="Live", font=10, command=lambda: live_detection())
live_button.place(x=400, y=190)

compare_button = tk.Button(root, text="Recognize", font=10, command=lambda: check(window=root, path1=image1_path_entry.get()))
compare_button.place(x=200, y=320)


root.mainloop()
