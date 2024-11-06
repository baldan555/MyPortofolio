import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def main():
    symptom_severity = pd.read_csv('Symptom-severity.csv')
    train = pd.read_csv('Training.csv')
    description = pd.read_csv('description.csv')
    diets = pd.read_csv('diets.csv')
    medications = pd.read_csv('medications.csv')
    precautions = pd.read_csv('precautions_df.csv')
    workout = pd.read_csv('workout_df.csv')

    X = train.drop('prognosis', axis=1)
    y = train['prognosis']

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    st.title('Disease Diagnosis and Recommendation')
    st.info("""
        **Information**:
        - To try, Please insert data using the sidebar.
        - The dataset used in this application is the Sympton Severity Dataset from (https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset/data).
        - The algorithm model used in this app is Random Forest Classifier based on the best accuracy modelling you can see at (https://www.kaggle.com/nissbaldanullah/diseasemedicinerecomendation)**.
        
        """)

    st.sidebar.header('Input Symptoms')
    symptom_inputs = {}
    for symptom in X.columns:
        symptom_inputs[symptom] = st.sidebar.radio(f'{symptom.replace("_", " ").title()}:', ['No', 'Yes'], index=0)

    col1, col2 = st.columns(2)

    with col1:
        st.write('### Symptom Checklist:')
        input_checklist = pd.DataFrame.from_dict(symptom_inputs, orient='index', columns=['Checked'])
        st.dataframe(input_checklist)

    with col2:
        if st.button('Get Diagnosis and Recommendations'):

            user_input = [1 if symptom_inputs[symptom] == 'Yes' else 0 for symptom in X.columns]
            user_input_df = pd.DataFrame([user_input], columns=X.columns)
            
            prognosis = model.predict(user_input_df)[0]

            description_text = description[description['Disease'] == prognosis]['Description'].values
            diet_recommendations = diets[diets['Disease'] == prognosis]['Diet'].values
            medication_recommendations = medications[medications['Disease'] == prognosis]['Medication'].values
            precautions_recommendations = precautions[precautions['Disease'] == prognosis]['Precaution_1'].values
            workout_recommendations = workout[workout['disease'] == prognosis]['workout'].values

            description_text = description_text[0] if len(description_text) > 0 else "No description available."
            diet_recommendations = ', '.join(eval(diet_recommendations[0])) if len(diet_recommendations) > 0 else "No diet recommendations available."
            medication_recommendations = ', '.join(eval(medication_recommendations[0])) if len(medication_recommendations) > 0 else "No medication recommendations available."
            precautions_recommendations = precautions_recommendations[0] if len(precautions_recommendations) > 0 else "No precautions available."
            workout_recommendations = workout_recommendations[0] if len(workout_recommendations) > 0 else "No workout recommendations available."
            
            data = {
                'Category': ['Description', 'Diet', 'Medications', 'Precautions', 'Workout'],
                'Details': [
                    description_text,
                    diet_recommendations,
                    medication_recommendations,
                    precautions_recommendations,
                    workout_recommendations
                ]
            }
            results_df = pd.DataFrame(data)

            st.subheader(f'Diagnosis: {prognosis}')
            st.write('### Details:')
            st.dataframe(results_df)

if __name__ == "__main__":
    main()
