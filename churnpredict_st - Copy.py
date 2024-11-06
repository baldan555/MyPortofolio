import streamlit as st
import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from sklearn.preprocessing import StandardScaler

def main():
    # Maintenance Notification
    st.warning("This app is under maintenance due to accuracy improvement. Please check back later.")
    
    # Stop further execution
    st.stop()

    model = CatBoostClassifier()
    model.load_model('catboost_model2.cbm')

    scaler = StandardScaler()

    numeric_features = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary']
    categorical_features = ['Geography', 'Gender']

    st.title("Bank Customer Churn Prediction")
    st.write("""
    This app predicts whether a customer will exit based on various features.
    Input the data manually or upload a CSV file.
    """)

    # Sidebar inputs
    st.sidebar.header("Input Data")

    CreditScore = st.sidebar.number_input("Credit Score", min_value=0, max_value=1000, value=500)
    Geography = st.sidebar.selectbox("Geography", ['France', 'Spain', 'Germany'])
    Gender = st.sidebar.selectbox("Gender", ['Male', 'Female'])
    Age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=30)
    Tenure = st.sidebar.number_input("Tenure", min_value=0, max_value=10, value=5)
    Balance = st.sidebar.number_input("Balance", min_value=0.0, value=1000.0)
    NumOfProducts = st.sidebar.number_input("Number of Products", min_value=1, max_value=4, value=1)
    HasCrCard = st.sidebar.selectbox("Has Credit Card", [0, 1])
    IsActiveMember = st.sidebar.selectbox("Is Active Member", [0, 1])
    EstimatedSalary = st.sidebar.number_input("Estimated Salary", min_value=0.0, value=50000.0)

    # Initialize session state to store the input data
    if 'data' not in st.session_state:
        st.session_state['data'] = pd.DataFrame(columns=[
            'CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 
            'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary'
        ])
        st.write("Initialized empty DataFrame in session state.")

    # Insert data when button is clicked
    if st.sidebar.button("Insert Data"):
        new_data = pd.DataFrame({
            'CreditScore': [CreditScore],
            'Geography': [Geography],
            'Gender': [Gender],
            'Age': [Age],
            'Tenure': [Tenure],
            'Balance': [Balance],
            'NumOfProducts': [NumOfProducts],
            'HasCrCard': [HasCrCard],
            'IsActiveMember': [IsActiveMember],
            'EstimatedSalary': [EstimatedSalary]
        })
        st.session_state['data'] = pd.concat([st.session_state['data'], new_data], ignore_index=True)
        st.write("Data after insertion:")
        st.write(st.session_state['data'])

    # Display inserted data in a table
    st.write("### Inserted Data")
    st.dataframe(st.session_state['data'])

    # Prediction button and result display
    if st.button("Predict"):
        input_data = st.session_state['data'].copy()
        if input_data.empty:
            st.write("Please insert data to predict.")
        else:
            input_data = pd.get_dummies(input_data, columns=categorical_features, drop_first=True)

            expected_columns = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 
                                'Geography_Germany', 'Geography_Spain', 'Gender_Male']
            for col in expected_columns:
                if col not in input_data.columns:
                    input_data[col] = 0

            input_data = input_data[expected_columns]

            scaled_input_data = input_data.copy()
            scaled_input_data[numeric_features] = scaler.fit_transform(input_data[numeric_features])

            predictions = model.predict(scaled_input_data)
            st.session_state['data']['Prediction'] = predictions

            # Display results in a card format
            st.write("### Prediction Results")
            for index, row in st.session_state['data'].iterrows():
                st.write(f"#### Customer {index + 1}")
                st.write(f"**Credit Score:** {row['CreditScore']}")
                st.write(f"**Geography:** {row['Geography']}")
                st.write(f"**Gender:** {row['Gender']}")
                st.write(f"**Prediction:** {'Exit' if row['Prediction'] == 1 else 'Stay'}")
                st.markdown("---")

    # CSV file upload for batch prediction
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        original_df = df.copy()
        
        df = pd.get_dummies(df, columns=categorical_features, drop_first=True)
        
        expected_columns = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 
                            'Geography_Germany', 'Geography_Spain', 'Gender_Male']
        for col in expected_columns:
            if col not in df.columns:
                df[col] = 0

        df = df[expected_columns]

        scaled_df = df.copy()
        scaled_df[numeric_features] = scaler.fit_transform(df[numeric_features])
        
        predictions = model.predict(scaled_df)
        
        df['Prediction'] = predictions
        
        st.write("Predictions for the uploaded file:")
        st.dataframe(pd.concat([original_df, df[['Prediction']]], axis=1))

if __name__ == "__main__":
    main()
