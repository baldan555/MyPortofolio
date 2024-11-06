import streamlit as st
import cv2
import mediapipe as mp
from PIL import Image
import numpy as np

def hand_gesture_recognition():
    st.markdown("<h1 style='text-align: center;'>Number Hand Gesture Recognition</h1>", unsafe_allow_html=True)

    st.info("""
        **Information**:
        - To try, Please click the Start Camera Button.
        - I perform mediapipe and cv2 for the recognition, you can see the code at (https://github.com/baldan555/HandGestureRecognition) 
        """)   

    # Inisialisasi MediaPipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_drawing = mp.solutions.drawing_utils

    def is_finger_up(landmarks, idx_tip, idx_pip):
        return landmarks[idx_tip].y < landmarks[idx_pip].y

    def is_thumb_up(landmarks, is_left_hand):
        if is_left_hand:
            return landmarks[5].x < landmarks[4].x
        else:
            return landmarks[5].x > landmarks[4].x

    def classify_gesture(landmarks, is_left_hand):
        fingers = []
        fingers.append(is_thumb_up(landmarks, is_left_hand))
        fingers.append(is_finger_up(landmarks, 8, 6))
        fingers.append(is_finger_up(landmarks, 12, 10))
        fingers.append(is_finger_up(landmarks, 16, 14))
        fingers.append(is_finger_up(landmarks, 20, 18))

        count = fingers.count(True)
        return count

    def process_frame(frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        total_fingers = 0

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                is_left_hand = handedness.classification[0].label == 'Left'
                landmarks = hand_landmarks.landmark

                wrist = landmarks[0]
                index_finger_tip = landmarks[8]
                angle = np.arctan2(index_finger_tip.y - wrist.y, index_finger_tip.x - wrist.x)
                angle_deg = np.degrees(angle)

                if angle_deg > 90:
                    fingers_count = 5 - classify_gesture(landmarks, is_left_hand)
                else:
                    fingers_count = classify_gesture(landmarks, is_left_hand)

                total_fingers += fingers_count

            cv2.putText(frame, f'Number: {total_fingers}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return frame

    if 'start_camera' not in st.session_state:
        st.session_state.start_camera = False

    if st.button('Start Camera'):
        st.session_state.start_camera = True

    if st.button('Stop Camera'):
        st.session_state.start_camera = False

    if st.session_state.start_camera:
        cap = cv2.VideoCapture(0)
        stframe = st.empty()

        while cap.isOpened() and st.session_state.start_camera:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (640, 480))
            frame = process_frame(frame)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img)

            # Atur lebar gambar
            stframe.image(img_pil, channels="RGB", width=650)  # Ubah lebar sesuai kebutuhan

        cap.release()

# Fungsi ini akan dipanggil dari aplikasi utama saat aplikasi Hand Gesture Recognition dipilih
def main():
    hand_gesture_recognition()
