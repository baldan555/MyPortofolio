import streamlit as st
import pandas as pd
import joblib
from streamlit_option_menu import option_menu

def main():

    st.markdown("<h1 style='text-align: center;'>Telco Customer Churn Predict</h1>", unsafe_allow_html=True)

    st.info("""
        **Information**:
        - To try, Please insert data using the sidebar.
        - The dataset used in this application is the Telco Customer Dataset from (https://www.kaggle.com/datasets/blastchar/telco-customer-churn).
        - The algorithm model used in this app is Logistic Regression based on the best accuracy modelling you can see at (https://www.kaggle.com/code/nissbaldanullah/telcocustomerchurpredict/notebook)**.
        
        """)

    model = joblib.load('Logistic Regression_model.pkl')
    le = joblib.load('label_encoder.pkl')
    feature_columns = joblib.load('feature_columns.pkl')

    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Input Data", "Upload CSV"],
            icons=["input", "upload"],
            menu_icon="cast",
            default_index=0,
        )

    def user_input_features():
        st.sidebar.header('Input Data Pelanggan')
        
        customerID = st.sidebar.text_input('customerID', '7590-VHVEG')
        gender = st.sidebar.selectbox('Gender', ['Female', 'Male'])
        SeniorCitizen = st.sidebar.selectbox('SeniorCitizen', [0, 1])
        Partner = st.sidebar.selectbox('Partner', ['Yes', 'No'])
        Dependents = st.sidebar.selectbox('Dependents', ['Yes', 'No'])
        tenure = st.sidebar.number_input('Tenure', min_value=0, max_value=100, value=1)
        PhoneService = st.sidebar.selectbox('PhoneService', ['Yes', 'No'])
        MultipleLines = st.sidebar.selectbox('MultipleLines', ['No', 'Yes', 'No phone service'])
        InternetService = st.sidebar.selectbox('InternetService', ['DSL', 'Fiber optic', 'No'])
        OnlineSecurity = st.sidebar.selectbox('OnlineSecurity', ['No', 'Yes', 'No internet service'])
        OnlineBackup = st.sidebar.selectbox('OnlineBackup', ['No', 'Yes', 'No internet service'])
        DeviceProtection = st.sidebar.selectbox('DeviceProtection', ['No', 'Yes', 'No internet service'])
        TechSupport = st.sidebar.selectbox('TechSupport', ['No', 'Yes', 'No internet service'])
        StreamingTV = st.sidebar.selectbox('StreamingTV', ['No', 'Yes', 'No internet service'])
        StreamingMovies = st.sidebar.selectbox('StreamingMovies', ['No', 'Yes', 'No internet service'])
        Contract = st.sidebar.selectbox('Contract', ['Month-to-month', 'One year', 'Two year'])
        PaperlessBilling = st.sidebar.selectbox('PaperlessBilling', ['Yes', 'No'])
        PaymentMethod = st.sidebar.selectbox('PaymentMethod', ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])
        MonthlyCharges = st.sidebar.number_input('MonthlyCharges', min_value=0.0, value=29.85)
        TotalCharges = st.sidebar.number_input('TotalCharges', min_value=0.0, value=29.85)

        data = {
            'customerID': customerID,
            'gender': gender,
            'SeniorCitizen': SeniorCitizen,
            'Partner': Partner,
            'Dependents': Dependents,
            'tenure': tenure,
            'PhoneService': PhoneService,
            'MultipleLines': MultipleLines,
            'InternetService': InternetService,
            'OnlineSecurity': OnlineSecurity,
            'OnlineBackup': OnlineBackup,
            'DeviceProtection': DeviceProtection,
            'TechSupport': TechSupport,
            'StreamingTV': StreamingTV,
            'StreamingMovies': StreamingMovies,
            'Contract': Contract,
            'PaperlessBilling': PaperlessBilling,
            'PaymentMethod': PaymentMethod,
            'MonthlyCharges': MonthlyCharges,
            'TotalCharges': TotalCharges
        }

        # Buat DataFrame
        features = pd.DataFrame([data])
        return features

    # Fungsi untuk upload CSV
    def upload_csv():
        st.sidebar.header('Upload CSV')
        uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            st.write(data.head())
            return data
        return None

    # Fungsi untuk menampilkan hasil prediksi dalam card
    def display_prediction(input_df):
        # Mengonversi input data
        for column in input_df.columns:
            if input_df[column].dtype == object:
                input_df[column] = input_df[column].apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)

        # Prediksi
        prediction = model.predict(input_df.drop('customerID', axis=1))
        prediction_proba = model.predict_proba(input_df.drop('customerID', axis=1))

        # Desain card dengan CSS
        st.markdown(
            """
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
                <h3 style="color: #333;">Hasil Prediksi</h3>
                <p style="font-size: 24px; color: {color};"><b>{prediction}</b></p>
                <h4 style="color: #333;">Probabilitas Prediksi</h4>
                <p style="font-size: 20px;">Tidak Churn: {prob_no_churn:.2f}%</p>
                <p style="font-size: 20px;">Churn: {prob_churn:.2f}%</p>
            </div>
            """.format(
                prediction="Churn" if prediction[0] else "Tidak Churn",
                color="#ff4b4b" if prediction[0] else "#2ecc71",
                prob_no_churn=prediction_proba[0][0] * 100,
                prob_churn=prediction_proba[0][1] * 100
            ),
            unsafe_allow_html=True
        )

    # Navigasi berdasarkan menu yang dipilih
    if selected == "Input Data":
        input_df = user_input_features()

        # Menampilkan card untuk input data
        st.markdown(
            """
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
                <h3 style="color: #333;">Keterangan Data Input</h3>
                <ul>
                    {details}
                </ul>
            </div>
            """.format(
                details='\n'.join(f"<li><b>{col}:</b> {val}</li>" for col, val in input_df.iloc[0].items())
            ),
            unsafe_allow_html=True
        )

        # Prediksi jika tombol ditekan
        if st.sidebar.button('Predict'):
            display_prediction(input_df)

    elif selected == "Upload CSV":
        csv_data = upload_csv()
        if csv_data is not None:
            # Menyiapkan data untuk prediksi
            csv_data_processed = csv_data.copy()
            for column in csv_data_processed.columns:
                if csv_data_processed[column].dtype == object:
                    csv_data_processed[column] = csv_data_processed[column].apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)

            # Prediksi
            predictions = model.predict(csv_data_processed.drop('customerID', axis=1))
            prediction_probas = model.predict_proba(csv_data_processed.drop('customerID', axis=1))

            # Menampilkan hasil prediksi
            st.write("Hasil Prediksi:")
            st.dataframe(pd.DataFrame({
                'customerID': csv_data['customerID'],
                'Prediction': ["Churn" if pred else "Tidak Churn" for pred in predictions],
                'Probabilitas Tidak Churn (%)': prediction_probas[:, 0] * 100,
                'Probabilitas Churn (%)': prediction_probas[:, 1] * 100
            }))

if __name__ == "__main__":
    main()