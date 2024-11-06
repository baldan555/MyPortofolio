import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score

def main():

    st.title('Lung Cancer Prediction')

    st.info("""
        **Information**:
        - To try, Please insert data using the sidebar.
        - The dataset used in this application is the Lung Cancer Dataset from (https://www.kaggle.com/datasets/mysarahmadbhat/lung-cancer).
        - You can choose and compare the algorithm model used in this app by the side bar).
        - See the modelling at (https://www.kaggle.com/code/nissbaldanullah/lungcancerprediction/notebook)**.
        
        """)

    @st.cache_data
    def load_data():
        return pd.read_csv('binarylung_no_outliers.csv')

    df = load_data()

    st.write("Data Preview:", df.head())

    X = df.drop('LUNG_CANCER', axis=1)
    y = df['LUNG_CANCER']

    label_encoder = LabelEncoder()
    X['GENDER'] = label_encoder.fit_transform(X['GENDER'])
    y = label_encoder.fit_transform(y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    models = {
        'Random Forest': RandomForestClassifier(max_depth=None, min_samples_split=2, n_estimators=100, random_state=42),
        'Logistic Regression': LogisticRegression(C=1, solver='liblinear'),
        'Support Vector Machine': SVC(C=1, kernel='linear', probability=True),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5, weights='distance')
    }

    results = []
    for model_name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        results.append({
            'Model': model_name,
            'Accuracy': accuracy,
            'Precision': report['1']['precision'], 
            'Recall': report['1']['recall'],       
            'F1-Score': report['1']['f1-score']     
        })

    results_df = pd.DataFrame(results)
    st.write("Model Comparison Results:")
    st.dataframe(results_df)

    st.sidebar.header("Input Features")

    gender_mapping = {'Male': 0, 'Female': 1}
    gender = st.sidebar.selectbox("Gender", list(gender_mapping.keys()))


    yes_no_mapping = {'YES': 1, 'NO': 0}

    age = st.sidebar.number_input("Age", min_value=0)
    smoking = st.sidebar.selectbox("Smoking", list(yes_no_mapping.keys()))
    yellow_fingers = st.sidebar.selectbox("Yellow Fingers", list(yes_no_mapping.keys()))
    anxiety = st.sidebar.selectbox("Anxiety", list(yes_no_mapping.keys()))
    peer_pressure = st.sidebar.selectbox("Peer Pressure", list(yes_no_mapping.keys()))
    chronic_disease = st.sidebar.selectbox("Chronic Disease", list(yes_no_mapping.keys()))
    fatigue = st.sidebar.selectbox("Fatigue", list(yes_no_mapping.keys()))
    allergy = st.sidebar.selectbox("Allergy", list(yes_no_mapping.keys()))
    wheezing = st.sidebar.selectbox("Wheezing", list(yes_no_mapping.keys()))
    alcohol_consuming = st.sidebar.selectbox("Alcohol Consuming", list(yes_no_mapping.keys()))
    coughing = st.sidebar.selectbox("Coughing", list(yes_no_mapping.keys()))
    shortness_of_breath = st.sidebar.selectbox("Shortness of Breath", list(yes_no_mapping.keys()))
    swallowing_difficulty = st.sidebar.selectbox("Swallowing Difficulty", list(yes_no_mapping.keys()))
    chest_pain = st.sidebar.selectbox("Chest Pain", list(yes_no_mapping.keys()))

    model_choice = st.sidebar.selectbox("Choose Model", list(models.keys()))

    if st.sidebar.button('Predict'):
    
        input_data = pd.DataFrame([[gender_mapping[gender], age, yes_no_mapping[smoking], yes_no_mapping[yellow_fingers], 
                                    yes_no_mapping[anxiety], yes_no_mapping[peer_pressure], yes_no_mapping[chronic_disease], 
                                    yes_no_mapping[fatigue], yes_no_mapping[allergy], yes_no_mapping[wheezing], 
                                    yes_no_mapping[alcohol_consuming], yes_no_mapping[coughing], 
                                    yes_no_mapping[shortness_of_breath], yes_no_mapping[swallowing_difficulty], 
                                    yes_no_mapping[chest_pain]]],
                                columns=['GENDER', 'AGE', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY',
                                        'PEER_PRESSURE', 'CHRONIC DISEASE', 'FATIGUE', 'ALLERGY',
                                        'WHEEZING', 'ALCOHOL CONSUMING', 'COUGHING', 'SHORTNESS OF BREATH',
                                        'SWALLOWING DIFFICULTY', 'CHEST PAIN'])

    
        input_data_scaled = scaler.transform(input_data)

        selected_model = models[model_choice]
        prediction = selected_model.predict(input_data_scaled)
        prediction_proba = selected_model.predict_proba(input_data_scaled)

    
        st.write("### Prediction Result")
        if prediction[0] == 1:
            st.markdown("<h3 style='color: red;'>**Prediction: POSITIVE**</h3>", unsafe_allow_html=True)
            st.write("Based on the input features, there is a high likelihood of lung cancer. Please consult a healthcare provider for further evaluation.")
        else:
            st.markdown("<h3 style='color: green;'>**Prediction: NEGATIVE**</h3>", unsafe_allow_html=True)
            st.write("The prediction indicates a lower likelihood of lung cancer. However, consider regular check-ups and maintaining a healthy lifestyle.")

        st.write("### Prediction Probability")
        st.write(f"The probability of having lung cancer is: **{prediction_proba[0][1]*100:.2f}%**")
        st.write(f"The probability of not having lung cancer is: **{prediction_proba[0][0]*100:.2f}%**")

        st.write("### Input Data")
        st.write(input_data)
if __name__ == "__main__":
    main()