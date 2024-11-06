import streamlit as st
import cv2
from tensorflow.keras.models import load_model
import numpy as np
import tensorflow as tf

def main():
    # Load model
    model = load_model('model_resnet.h5')

    # Label ekspresi
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    # Fungsi untuk deteksi wajah dan prediksi ekspresi
    def detect_emotions(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48))
            roi_gray = np.stack([roi_gray] * 3, axis=-1)  # Convert grayscale to RGB
            roi_gray = roi_gray.astype('float32') / 255
            roi_gray = np.expand_dims(roi_gray, axis=0)

            prediction = model.predict(roi_gray)
            maxindex = int(np.argmax(prediction))
            emotion = emotion_labels[maxindex]

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

        return frame

    # Tampilan judul di tengah
    st.markdown("<h1 style='text-align: center;'>Real-time Emotion Detection</h1>", unsafe_allow_html=True)

    st.info("""
        **Information**:
        - To try, Please click the Start Camera Button.
        - To see the perform of the model you can see the code at (https://www.kaggle.com/code/nissbaldanullah/emotionfacemodel/notebook) 
        - when you stop the camera and there some error appear, just ignore and refresh it or you can just click another App an get back again.
        """)      

    # Tombol Start dan Stop
    start_button = st.button('Start Camera')
    stop_button = st.button('Stop Camera')

    # Ruang untuk menampilkan video
    FRAME_WINDOW = st.image([])

    # Status kamera
    camera_active = False

    if start_button:
        camera_active = True
        camera = cv2.VideoCapture(0)

    if stop_button:
        camera_active = False
        if 'camera' in locals():
            camera.release()
            FRAME_WINDOW.image([])  # Bersihkan tampilan gambar
            st.write('Camera stopped')

    while camera_active:
        ret, frame = camera.read()
        if not ret:
            st.write("Camera not detected")
            break
        frame = detect_emotions(frame)
        FRAME_WINDOW.image(frame)

    # Reset session after stopping the camera
    if not camera_active:
        tf.keras.backend.clear_session()

if __name__ == "__main__":
    main()
