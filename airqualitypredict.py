import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load and process the dataset

def main():
    st.markdown("<h1 style='text-align: center;'>Air Quality Health Impact Score Predict</h1>", unsafe_allow_html=True)

    st.info("""
        **Information**:
        - To try, Please insert data using the sidebar.
        - The dataset used in this application is the Air Quality and Health Impact Dataset from (https://www.kaggle.com/datasets/rabieelkharoua/air-quality-and-health-impact-dataset/data).
        - The algorithm model used in this app is Histogram Gradient Boosting based on the best accuracy modelling you can see at (https://www.kaggle.com/code/nissbaldanullah/airqualityhelathimpactscorepredict)**.
        
        """)

    @st.cache_data
    def load_and_process_data():
        data = pd.read_csv('airquality.csv')
        data = data.drop(columns=['HealthImpactClass', 'RecordID'])
        X = data.drop(columns=['HealthImpactScore'])
        y = data['HealthImpactScore']
        return X, y

    # Load and preprocess data
    X, y = load_and_process_data()

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train HistGradientBoostingRegressor with specified hyperparameters
    model = HistGradientBoostingRegressor(
        learning_rate=0.1, 
        max_iter=300, 
        max_depth=7, 
        l2_regularization=10
    )
    model.fit(X_train_scaled, y_train)

    # Streamlit app
    st.sidebar.title("Input Data")
    st.sidebar.write("Please enter the following environmental and health data:")

    AQI = st.sidebar.number_input('AQI', value=187.27, help="Air Quality Index (AQI) value, indicating the level of air pollution.")
    PM10 = st.sidebar.number_input('PM10', value=295.85, help="Particulate Matter (PM10) in µg/m³, representing particles with a diameter of 10 micrometers or less.")
    PM2_5 = st.sidebar.number_input('PM2_5', value=13.04, help="Particulate Matter (PM2.5) in µg/m³, representing fine particles with a diameter of 2.5 micrometers or less.")
    NO2 = st.sidebar.number_input('NO2', value=6.64, help="Nitrogen Dioxide (NO2) concentration in µg/m³.")
    SO2 = st.sidebar.number_input('SO2', value=66.16, help="Sulfur Dioxide (SO2) concentration in µg/m³.")
    O3 = st.sidebar.number_input('O3', value=54.62, help="Ozone (O3) concentration in µg/m³.")
    Temperature = st.sidebar.number_input('Temperature', value=5.15, help="Ambient temperature in °C.")
    Humidity = st.sidebar.number_input('Humidity', value=84.42, help="Relative humidity in percentage (%).")
    WindSpeed = st.sidebar.number_input('WindSpeed', value=6.14, help="Wind speed in km/h.")
    RespiratoryCases = st.sidebar.number_input('RespiratoryCases', value=7, help="Number of reported respiratory cases.")
    CardiovascularCases = st.sidebar.number_input('CardiovascularCases', value=5, help="Number of reported cardiovascular cases.")
    HospitalAdmissions = st.sidebar.number_input('HospitalAdmissions', value=1, help="Number of hospital admissions.")

    # Button to add data
    if st.sidebar.button('Insert Data'):
        if 'data_entries' not in st.session_state:
            st.session_state.data_entries = []
        
        st.session_state.data_entries.append({
            'AQI': AQI,
            'PM10': PM10,
            'PM2_5': PM2_5,
            'NO2': NO2,
            'SO2': SO2,
            'O3': O3,
            'Temperature': Temperature,
            'Humidity': Humidity,
            'WindSpeed': WindSpeed,
            'RespiratoryCases': RespiratoryCases,
            'CardiovascularCases': CardiovascularCases,
            'HospitalAdmissions': HospitalAdmissions
        })

    # Display inserted data
    if 'data_entries' in st.session_state and st.session_state.data_entries:
        df_entries = pd.DataFrame(st.session_state.data_entries)
        st.subheader("Inserted Data")
        st.write(df_entries)

        # Button to make predictions
        if st.button('Submit for Prediction'):
            input_data_scaled = scaler.transform(df_entries)
            predictions = model.predict(input_data_scaled)
            
            # Display predictions
            st.subheader("Prediction Results")
            results = pd.DataFrame({
                'AQI': df_entries['AQI'],
                'PM10': df_entries['PM10'],
                'PM2_5': df_entries['PM2_5'],
                'NO2': df_entries['NO2'],
                'SO2': df_entries['SO2'],
                'O3': df_entries['O3'],
                'Temperature': df_entries['Temperature'],
                'Humidity': df_entries['Humidity'],
                'WindSpeed': df_entries['WindSpeed'],
                'RespiratoryCases': df_entries['RespiratoryCases'],
                'CardiovascularCases': df_entries['CardiovascularCases'],
                'HospitalAdmissions': df_entries['HospitalAdmissions'],
                'Predicted Health Impact Score': predictions
            })
            
            st.write(results)

            # Visualize results in a more engaging format
            for _, row in results.iterrows():
                st.markdown(f"""
                    <div style="border: 2px solid #007bff; border-radius: 12px; padding: 15px; margin-bottom: 20px; background-color: #e9f7ff;">
                        <h3 style="color: #007bff;">Prediction Summary</h3>
                        <p style="font-size: 16px; font-weight: bold;">Based on the provided data, here is the detailed prediction:</p>
                        <ul style="font-size: 16px; line-height: 1.5;">
                            <li><strong>AQI:</strong> {row['AQI']} - Air Quality Index value.</li>
                            <li><strong>PM10:</strong> {row['PM10']} µg/m³ - Particulate Matter (10 micrometers or less).</li>
                            <li><strong>PM2_5:</strong> {row['PM2_5']} µg/m³ - Fine Particulate Matter (2.5 micrometers or less).</li>
                            <li><strong>NO2:</strong> {row['NO2']} µg/m³ - Nitrogen Dioxide concentration.</li>
                            <li><strong>SO2:</strong> {row['SO2']} µg/m³ - Sulfur Dioxide concentration.</li>
                            <li><strong>O3:</strong> {row['O3']} µg/m³ - Ozone concentration.</li>
                            <li><strong>Temperature:</strong> {row['Temperature']} °C - Ambient temperature.</li>
                            <li><strong>Humidity:</strong> {row['Humidity']}% - Relative humidity.</li>
                            <li><strong>WindSpeed:</strong> {row['WindSpeed']} km/h - Wind speed.</li>
                            <li><strong>Respiratory Cases:</strong> {row['RespiratoryCases']} - Number of respiratory cases reported.</li>
                            <li><strong>Cardiovascular Cases:</strong> {row['CardiovascularCases']} - Number of cardiovascular cases reported.</li>
                            <li><strong>Hospital Admissions:</strong> {row['HospitalAdmissions']} - Number of hospital admissions.</li>
                        </ul>
                        <h4 style="color: #007bff;">Predicted Health Impact Score:</h4>
                        <p style="font-size: 18px; font-weight: bold; color: #ff5733;">{row['Predicted Health Impact Score']:.2f}</p>
                        <p style="font-size: 16px;">This score reflects the estimated impact of the environmental and health factors provided. A higher score suggests a greater potential health impact.</p>
                    </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()        
