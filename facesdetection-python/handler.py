import cv2
import numpy as np
import urllib.request
import base64
import json

class Response:
    def __init__(self, faces):
        self.Faces = faces

def detect_faces(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return faces

def handle(req):
    data = req.strip()
    
    # Fetch the image from the URL
    try:
        response = urllib.request.urlopen(data)
        img_data = response.read()
    except Exception as e:
        return f"Error fetching image from URL: {str(e)}"
    
    # Decode the image
    nparr = np.frombuffer(img_data, dtype=np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Detect faces in the image
    faces = detect_faces(image)
    
    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # Encode the image back to base64
    _, encoded_img = cv2.imencode('.jpg', image)
    encoded_image = base64.b64encode(encoded_img).decode('utf-8')
    
    # Convert the faces array to a list
    faces_list = faces.tolist()
    
    # Create a response object
    response = Response(faces_list)
    response.ImageBase64 = "data:image/jpeg;base64," + encoded_image  # Add 'data:image/jpeg;base64,' prefix

    
    # Convert the response to JSON
    response_json = json.dumps(response.__dict__)
    
    return response_json





