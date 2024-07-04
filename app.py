import streamlit as st
import pickle
import numpy as np

# Load the model
model = pickle.load(open('models/loan_prediction.sav', 'rb'))

st.set_page_config(page_title="Loan Prediction App", layout="centered")


# Custom CSS
def local_css(file_name):
    with open(file_name, 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    # Apply custom CSS
    local_css("templates/style.css")

    # Page configuration

    # Header
    st.markdown("<h1 class='title'>Loan Prediction App</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Fill in the details below to predict loan approval</p>", unsafe_allow_html=True)

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox('Gender', ['Male', 'Female'])
        married = st.selectbox('Married', ['Yes', 'No'])
        dependents = st.number_input('Dependents', min_value=0, max_value=10, value=0, step=1)
        education = st.selectbox('Education', ['Graduate', 'Not Graduate'])
        self_employed = st.selectbox('Self Employed', ['Yes', 'No'])

    with col2:
        applicant_income = st.number_input('Applicant Income', min_value=0, value=0)
        coapplicant_income = st.number_input('Coapplicant Income', min_value=0, value=0)
        loan_amount = st.number_input('Loan Amount', min_value=0, value=0)
        loan_amount_term = st.number_input('Loan Amount Term (months)', min_value=0, value=0)
        credit_history = st.selectbox('Credit History', ['1', '0'])
        property_area = st.selectbox('Property Area', ['Rural', 'Semiurban', 'Urban'])

    # Predict button
    if st.button('Predict Loan Approval', key='predict_button'):
        features = [
            1 if gender == 'Male' else 0,
            1 if married == 'Yes' else 0,
            int(dependents),
            1 if education == 'Graduate' else 0,
            1 if self_employed == 'Yes' else 0,
            float(applicant_income),
            float(coapplicant_income),
            float(loan_amount),
            float(loan_amount_term),
            int(credit_history),
            2 if property_area == 'Urban' else (1 if property_area == 'Semiurban' else 0)
        ]

        features = np.array(features).reshape(1, -1)
        prediction = model.predict(features)
        prediction_text = 'Approved' if prediction[0] == 1 else 'Rejected'

        st.markdown(f"<div class='prediction-box'><h2>Loan Approval Prediction:</h2><p class='prediction-text {prediction_text.lower()}'>{prediction_text}</p></div>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()