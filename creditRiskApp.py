import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib


def main():
    
    pipeline = joblib.load('best_model_pipeline.pkl')


    numerical_features = ['person_age', 'person_income', 'person_emp_length', 
                        'loan_amnt', 'loan_int_rate', 'loan_percent_income', 
                        'cb_person_cred_hist_length']
    categorical_features = ['person_home_ownership', 'loan_intent', 
                            'loan_grade', 'cb_person_default_on_file']


    st.markdown("""
        <style>
        .title {
            text-align: center;
            font-size: 2.5em;
            font-weight: bold;
            color: #00796b;
            margin-bottom: 30px;
            font-family: 'Arial', sans-serif;
        }
        </style>
        <div class="title">
            Credit Risk Prediction
        </div>
        """, unsafe_allow_html=True)

    st.info("""
        **Information**:
        - To try, Please insert data using the sidebar.
        - The dataset used in this application is the creditrisk Dataset from (https://www.kaggle.com/datasets/nissbaldanullah/credit-risk).
        - The algorithm model used in this app is Gradient Boosting Classifier based on the best accuracy modelling you can see at (https://www.kaggle.com/nissbaldanullah/creditrisk)**.
        
        """)

    st.divider()

    st.sidebar.markdown("""
        <style>
        .sidebar .sidebar-content {
            background-color: #f1f8e9; /* Light green for the sidebar background */
            border-radius: 10px;
            padding: 20px;
        }
        .sidebar .sidebar-content .widget {
            margin-bottom: 20px;
        }
        .sidebar .sidebar-content h1 {
            font-size: 1.5em;
            color: #00796b;
        }
        .sidebar .sidebar-content .stButton>button {
            background-color: #00796b;
            color: white;
            font-size: 1em;
            border-radius: 5px;
            padding: 10px;
            border: none;
            cursor: pointer;
            width: 100%;
        }
        .sidebar .sidebar-content .stButton>button:hover {
            background-color: #004d40;
        }
        </style>
        """, unsafe_allow_html=True)


    st.sidebar.header("Input Data")

    person_age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=30)
    person_income = st.sidebar.number_input("Annual Income", min_value=0, value=50000)
    person_home_ownership = st.sidebar.selectbox("Home Ownership", options=['OWN', 'RENT', 'MORTGAGE'])
    person_emp_length = st.sidebar.number_input("Employment Length (in years)", min_value=0, max_value=40, value=5)
    loan_intent = st.sidebar.selectbox("Loan Intent", options=['PERSONAL', 'EDUCATION', 'MEDICAL'])
    loan_grade = st.sidebar.selectbox("Loan Grade", options=['A', 'B', 'C', 'D', 'E'])
    loan_amnt = st.sidebar.number_input("Loan Amount", min_value=0, value=10000)
    loan_int_rate = st.sidebar.number_input("Interest Rate", min_value=0.0, value=10.0)
    loan_percent_income = st.sidebar.number_input("Percent Income", min_value=0.0, value=0.2)
    cb_person_default_on_file = st.sidebar.selectbox("Historical Default", options=['Y', 'N'])
    cb_person_cred_hist_length = st.sidebar.number_input("Credit History Length", min_value=0, value=5)


    st.markdown(f"""
        <style>
        .Detail {{
            background-color: #ffffff; /* White background for the Detail */
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        .Detail-title {{
            font-size: 1.5em;
            font-weight: bold;
            color: #00796b;
            margin-bottom: 15px;
            text-align: center;
        }}
        .Detail-content {{
            font-size: 1.2em;
            color: #004d40;
        }}
        .Detail-item {{
            border-bottom: 1px solid #e0e0e0;
            padding: 10px 0;
        }}
        .Detail-item:last-child {{
            border-bottom: none;
        }}
        </style>
        <div class="Detail">
            <div class="Detail-title">Detail</div>
            <div class="Detail-content">
                <div class="Detail-item">
                    <strong>Age:</strong> {person_age}
                </div>
                <div class="Detail-item">
                    <strong>Annual Income:</strong> ${person_income:,.2f}
                </div>
                <div class="Detail-item">
                    <strong>Home Ownership:</strong> {person_home_ownership}
                </div>
                <div class="Detail-item">
                    <strong>Employment Length:</strong> {person_emp_length} years
                </div>
                <div class="Detail-item">
                    <strong>Loan Intent:</strong> {loan_intent}
                </div>
                <div class="Detail-item">
                    <strong>Loan Grade:</strong> {loan_grade}
                </div>
                <div class="Detail-item">
                    <strong>Loan Amount:</strong> ${loan_amnt:,.2f}
                </div>
                <div class="Detail-item">
                    <strong>Interest Rate:</strong> {loan_int_rate}%
                </div>
                <div class="Detail-item">
                    <strong>Percent Income:</strong> {loan_percent_income:.2%}
                </div>
                <div class="Detail-item">
                    <strong>Historical Default:</strong> {cb_person_default_on_file}
                </div>
                <div class="Detail-item">
                    <strong>Credit History Length:</strong> {cb_person_cred_hist_length} years
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.sidebar.button('Predict'):

        input_data = pd.DataFrame({
            'person_age': [person_age],
            'person_income': [person_income],
            'person_home_ownership': [person_home_ownership],
            'person_emp_length': [person_emp_length],
            'loan_intent': [loan_intent],
            'loan_grade': [loan_grade],
            'loan_amnt': [loan_amnt],
            'loan_int_rate': [loan_int_rate],
            'loan_percent_income': [loan_percent_income],
            'cb_person_default_on_file': [cb_person_default_on_file],
            'cb_person_cred_hist_length': [cb_person_cred_hist_length]
        })


        prediction = pipeline.predict(input_data)
        probability = pipeline.predict_proba(input_data)[0]

        risk_label = 'High Risk' if prediction[0] == 1 else 'Low Risk'
        risk_class = 'risk-high' if prediction[0] == 1 else 'risk-low'

        st.markdown(f"""
            <style>
            .card {{
                background-color: #e0f7fa; /* Light cyan background for the main card */
                border-radius: 12px;
                padding: 30px;
                margin-bottom: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                text-align: center; /* Center text in the main card */
            }}
            .card-title {{
                font-size: 2em;
                font-weight: bold;
                color: #00796b; /* Teal color for the title */
                margin-bottom: 20px;
                font-family: 'Arial', sans-serif; /* Stylish, readable font */
            }}
            .card-content {{
                font-size: 1.5em;
                color: #004d40; /* Darker teal for text */
                font-family: 'Arial', sans-serif; /* Stylish, readable font */
            }}
            .risk-high {{
                color: #d32f2f; /* Red for high risk */
                font-weight: bold;
            }}
            .risk-low {{
                color: #388e3c; /* Green for low risk */
                font-weight: bold;
            }}
            .inner-card {{
                background-color: #ffffff;
                border-radius: 8px;
                padding: 20px;
                margin: 10px 0;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                text-align: left; /* Align text to the left within inner cards */
            }}
            </style>
            <div class="card">
                <div class="card-title">Prediction Result</div>
                <div class="card-content">
                    <div class="inner-card">
                        <p class="{risk_class}">Risk: {risk_label}</p>
                    </div>
                    <div class="inner-card">
                        <p>Probability of High Risk: {probability[1]:.2f}</p>
                    </div>
                    <div class="inner-card">
                        <p>Probability of Low Risk: {probability[0]:.2f}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        fig = go.Figure(data=[
            go.Bar(name='Probability of High Risk', x=['High Risk'], y=[probability[1]]),
            go.Bar(name='Probability of Low Risk', x=['Low Risk'], y=[probability[0]])
        ])
        fig.update_layout(barmode='stack', title='Probability Breakdown')
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()