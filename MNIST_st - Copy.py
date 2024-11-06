import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import tensorflow as tf
from PIL import Image
import os

def load_model():
    model_path = 'mnist_cnn_model.h5'
    if not os.path.exists(model_path):
        st.error(f"Model file not found: {model_path}")
        return None
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def main():
    # Custom CSS for styling
    st.markdown("""
        <style>
            .title {
                text-align: center;
                font-family: 'Helvetica', sans-serif;
                color: #333333;
                margin-bottom: 30px;
            }
            .main-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .canvas-container, .pred-container {
                width: 45%;
            }
            .canvas-wrapper {
                padding: 10px;
            }
            .pred-box {
                background-color: #f0f0f0;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                margin-top: 20px;
            }
            .pred-text {
                font-size: 35px;
                font-weight: bold;
                color: #333333;
                text-align: center;
            }
            .sidebar .sidebar-content {
                background-color: #f7f7f7;
                padding: 20px;
                border-radius: 10px;
            }
            .stButton > button {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                border-radius: 5px;
                padding: 10px 20px;
                margin: 20px auto;
                display: block;
            }
            .stButton > button:hover {
                background-color: #45a049;
            }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("<h1 class='title'>Draw a Number</h1>", unsafe_allow_html=True)

    st.info("""
        **Information**:
        - Try to draw a Number in the box.
        - The dataset used in this application is the MNIST Dataset from keras.dataset.
        - You can see how the model perform the accuracy at (https://www.kaggle.com/nissbaldanullah/mnist-number-predict-using-cnn)**.
        
        """)

    # Sidebar settings
    st.sidebar.header("Setting")

    stroke_color = "#000000"  # Black
    bg_color = "#FFFFFF"  # White
    realtime_update = st.sidebar.checkbox("Update realtime", True)

    # Main container with canvas on the left and prediction on the right
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    # Left: Canvas for drawing
    st.markdown("<div class='canvas-container'>", unsafe_allow_html=True)
    st.markdown("<div class='canvas-wrapper'>", unsafe_allow_html=True)
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",  # canvas background fill color
        stroke_width=15,
        stroke_color=stroke_color,
        background_color=bg_color,
        update_streamlit=realtime_update,
        height=350,
        width=350,
        drawing_mode="freedraw",
        key="canvas",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Right: Prediction result
    st.markdown("<div class='pred-container'>", unsafe_allow_html=True)
    if canvas_result.image_data is not None:
        # Convert the image to grayscale and resize to 28x28 (MNIST model input size)
        image = Image.fromarray(canvas_result.image_data.astype('uint8')).convert('L')
        image = image.resize((28, 28))
        image = np.array(image)

        # Invert colors if the background is black
        image = np.invert(image)

        # Normalize the image
        image = image / 255.0

        # Load model
        model = load_model()
        if model is not None:
            # Make a prediction
            prediction = model.predict(image.reshape(1, 28, 28, 1))
            predicted_digit = np.argmax(prediction)

            # Display the prediction in a styled box
            st.markdown(f"""
                <div class='pred-box'>
                    <p class='pred-text'>You Draw Number: {predicted_digit}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
