import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf

def main():
    # Fungsi untuk memuat model
    @st.cache_data
    def load_model():
        model = tf.keras.models.load_model('rhizomes_model.h5')  # Ganti dengan path model Anda
        return model

    model = load_model()

    # Fungsi untuk melakukan prediksi
    def predict(image):
        image = image.resize((224, 224))  # Sesuaikan dengan ukuran input model Anda
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)
        
        predictions = model.predict(image)
        classes = ['Jahe', 'Kunyit', 'Lengkuas']
        return classes[np.argmax(predictions)]

    # Judul aplikasi
    st.title('Prediksi Jenis Rimpang')

    # Unggah gambar
    uploaded_file = st.file_uploader("Unggah gambar", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Gambar yang diunggah.', use_column_width=True)
        
        st.write("")
        st.write("Memprediksi...")
        
        label = predict(image)
        st.write(f'Ini adalah: {label}')

if __name__ == "__main__":
    main()
