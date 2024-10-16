
import os
import face_recognition

def recognize_faces():
    known_face_encodings = []
    known_face_names = []

    # Load known faces and names
    known_faces_dir = '/home/pi/known_faces'
    for person_name in os.listdir(known_faces_dir):
        person_dir = os.path.join(known_faces_dir, person_name)
        if os.path.isdir(person_dir):
            for filename in os.listdir(person_dir):
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    image_path = os.path.join(person_dir, filename)
                    image = face_recognition.load_image_file(image_path)
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        encoding = encodings[0]
                        known_face_encodings.append(encoding)
                        known_face_names.append(person_name)
                        print(f"Loaded encoding for {person_name} from {filename}")

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []

    # Process each captured image
    for i in range(1, 6):
        filename = f"/home/pi/Pictures/RaspPhotos/image_{i}.jpg"
        if os.path.exists(filename):
            image = face_recognition.load_image_file(filename)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                print(f"Recognized {name} in {filename}")

            if face_names:
                return face_names[0]  # Return the first recognized name

    return None

# if __name__ == "__main__":
    # recognized_name = recognize_faces()
    # if recognized_name:
        # print(f"Recognized: {recognized_name}")
    # else:
        # print("No faces recognized.")
