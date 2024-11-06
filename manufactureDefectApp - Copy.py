import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def main():
    # Load the dataset from 'manufacture.csv'
    @st.cache_data
    def load_data():
        df = pd.read_csv('manufacture.csv')
        return df

    # Initialize and prepare the dataset
    df = load_data()
    X = df.drop(columns=['DefectStatus'])
    y = df['DefectStatus']

    # Split the data for model training
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model with the best parameters
    model = RandomForestClassifier(
        max_depth=None,
        min_samples_leaf=1,
        min_samples_split=5,
        n_estimators=100,
        random_state=42
    )
    model.fit(X_train, y_train)

    st.title('Manufacturing Defect Prediction')

    st.info("""
        **Information**:
        - To try, Please insert data using the sidebar.
        - The dataset used in this application is the Manufacturing Defects Dataset from (https://www.kaggle.com/datasets/rabieelkharoua/predicting-manufacturing-defects-dataset/data).
        - The algorithm model used in this app is Random Forest based on the best accuracy modeling you can see at (https://www.kaggle.com/code/nissbaldanullah/manufacturedefectpredict)**.
        """)

    # Initialize session state for storing inserted data
    if 'manufacture_data' not in st.session_state:
        st.session_state.manufacture_data = pd.DataFrame(columns=['Name'] + X.columns.tolist())

    # Sidebar for input and action buttons
    st.sidebar.header('Data Entry')
    default_values = {
        "ProductionVolume": 5647.606037,
        "ProductionCost": 87.335966,
        "SupplierQuality": 5,
        "DeliveryDelay": 0.638524,
        "DefectRate": 67.628690,
        "QualityScore": 8,
        "MaintenanceHours": 4.692476,
        "DowntimePercentage": 3.577616,
        "InventoryTurnover": 0.055331,
        "EquipmentEfficiency": 70.705189,
        "ProcessComplexity": 1,
        "Shift": 1
    }
    
    inputs = {}
    name = st.sidebar.text_input("Name")
    for col in X.columns:
        if df[col].dtype == 'O':  
            unique_values = df[col].unique().tolist()
            inputs[col] = st.sidebar.selectbox(f"{col}", unique_values, index=unique_values.index(default_values.get(col, unique_values[0])))
        else:  
            min_value, max_value = float(df[col].min()), float(df[col].max())
            inputs[col] = st.sidebar.slider(f"{col}", min_value, max_value, float(default_values.get(col, min_value)))

    # Insert data
    if st.sidebar.button('Insert Data'):
        if name:
            new_data = pd.DataFrame([[name] + [inputs[col] for col in X.columns]], columns=['Name'] + X.columns.tolist())
            st.session_state.manufacture_data = pd.concat([st.session_state.manufacture_data, new_data], ignore_index=True)
        else:
            st.error("Please enter a name.")

    # Display the input data
    st.subheader('Input Data')
    st.write(st.session_state.manufacture_data)

    # Perform prediction if there is data in session_state
    if st.button('Predict'):
        if not st.session_state.manufacture_data.empty:
            features = st.session_state.manufacture_data.drop(columns=['Name'])
            predictions = model.predict(features)
            st.session_state.manufacture_data['DefectStatus'] = predictions
            
            st.subheader('Prediction Results')
            st.write(st.session_state.manufacture_data)
        else:
            st.warning("No data to predict.")
            
if __name__ == '__main__':
    main()
