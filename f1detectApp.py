import streamlit as st
import torch
import cv2
import time
from ultralytics import YOLO
import contextlib
import sys
import os


# Context manager to suppress stdout and stderr
@contextlib.contextmanager
def suppress_stdout_stderr():
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


def main():

    st.cache_data.clear()
    # Load the trained model
    model = YOLO('best.pt')

    # Streamlit UI
    st.markdown("<h1 style='text-align: center;'>YOLO V8 F1 Max Verstappen Object Detection</h1>", unsafe_allow_html=True)
    st.write('Detecting objects in a pre-loaded video.')
    st.info("""
        **Information**:
        - Detecting objects in a pre-loaded video.
        - I used yolov8 from ultralytics for the model perform with manual data annotation using roboflow
        - you can see the code at(https://github.com/baldan555/f1MaxVerstappenYOLOv8ObjectDetection)
        """)
    # Path ke video yang sudah ada
    video_path = 'videomv.mp4'

    # Membuka video file
    cap = cv2.VideoCapture(video_path)

    # Button to stop the process
    stop_button = st.button("Stop Video Processing")
    stop_flag = False

    # Memastikan video berhasil dibuka
    if not cap.isOpened():
        st.error(f"Error: Could not open video {video_path}.")
    else:
        # Membuat output video writer
        output_video = 'output_video.mp4'
        out = None

        stframe = st.empty()
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = int(1000 / fps)  # Menghitung delay untuk setiap frame agar sesuai dengan FPS asli video

        while cap.isOpened() and not stop_flag:
            ret, frame = cap.read()
            if not ret or stop_button:
                stop_flag = True
                break

            with suppress_stdout_stderr():  # Suppress output during model inference
                # Deteksi objek pada frame
                results = model(frame)

            # Menggambar bounding boxes pada frame
            annotated_frame = results[0].plot()

            # Menulis frame ke output video
            if out is None:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_video, fourcc, fps, (frame.shape[1], frame.shape[0]))

            out.write(annotated_frame)

            # Menampilkan frame
            stframe.image(annotated_frame, channels="BGR")

            # Delay untuk menjaga FPS
            time.sleep(delay / 1000)

        cap.release()
        if out is not None:
            out.release()

        st.success(f"Video processed successfully! You can download the output video [here](output_video.mp4).")


if __name__ == "__main__":
    main()
