import streamlit as st
import pandas as pd
import numpy as np
import pickle
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

st.title("Heart Disease Risk Assessment")
tab1,tab2 = st.tabs(["Individual Prediction", "Batch Prediction"])

with tab1:
    age = st.number_input("Age (years)", min_value=0, max_value=150)
    sex = st.selectbox("Sex", ["Male", "Female"])
    cp = st.selectbox("Chest Pain Type", ["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"])
    trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=0, max_value=300)
    chol = st.number_input("Serum Cholesterol (mg/dl)", min_value=0)
    fbs = st.selectbox("Fasting Blood Sugar", ["<= 120 mg/dl", "> 120 mg/dl"])
    restecg = st.selectbox("Resting ECG Results", ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"])
    thalach = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=220)
    exang = st.selectbox("Exercise-Induced Angina", ["Yes", "No"])
    oldpeak = st.number_input("Oldpeak (ST Depression)", min_value=0.0, max_value=10.0, step=0.1)
    slope = st.selectbox("Slope of Peak Exercise ST Segment", ["Upsloping", "Flat", "Downsloping"])
    ca = st.selectbox("Number of Major Vessels Colored by Fluoroscopy (0–3)", [0, 1, 2, 3])
    thal = st.selectbox("Thalassemia", ["Normal", "Fixed Defect", "Reversible Defect"])

    # Convert categorical inputs to numeric
    sex = 1 if sex == "Male" else 0
    cp = ["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"].index(cp)
    fbs = 1 if fbs == "> 120 mg/dl" else 0
    restecg = ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"].index(restecg)
    exang = 1 if exang == "Yes" else 0
    slope = ["Upsloping", "Flat", "Downsloping"].index(slope)
    thal = ["Normal", "Fixed Defect", "Reversible Defect"].index(thal)

    # Create a DataFrame with user inputs
    input_data = pd.DataFrame({
        'age': [age],
        'sex': [sex],
        'cp': [cp],
        'trestbps': [trestbps],
        'chol': [chol],
        'fbs': [fbs],
        'restecg': [restecg],
        'thalach': [thalach],
        'exang': [exang],
        'oldpeak': [oldpeak],
        'slope': [slope],
        'ca': [ca],
        'thal': [thal]
    })


    # Load the model
    with open('model.pkl', 'rb') as f:
        logistic_model = pickle.load(f)

    # Submit button and prediction logic
    if st.button("Submit"):
        st.subheader('🩺 Result')
        st.markdown('-----------------------------')

        prediction = logistic_model.predict(input_data)

        result_text = "No heart disease detected." if prediction[0] == 0 else "Heart disease detected."
        if prediction[0] == 0:
            st.success(result_text)
        else:
            st.error(result_text)
        st.markdown('-----------------------------')


        # Generate Report________________
        import datetime

        st.markdown("### Generated Report")

        # Create PDF in memory
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        y = height - 50

        # Title
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2, y, "Heart Risk Assessment Report")
        y -= 30

        # Subtitle
        c.setFont("Helvetica", 12)
        today = datetime.date.today().strftime("%B %d, %Y")
        c.drawCentredString(width / 2, y, f"Date: {today}")
        y -= 40

        # Section: Patient Inputs
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Patient Information & Risk Factors")
        y -= 20
        c.setFont("Helvetica", 12)

        data_dict = {
            "Age": age,
            "Sex": sex,
            "Chest Pain Type": cp,
            "Resting BP (mm Hg)": trestbps,
            "Cholesterol (mg/dl)": chol,
            "Fasting Blood Sugar": fbs,
            "Resting ECG": restecg,
            "Max Heart Rate": thalach,
            "Exercise-Induced Angina": exang,
            "Oldpeak": oldpeak,
            "Slope": slope,
            "Major Vessels": ca,
            "Thalassemia": thal
        }

        for key, val in data_dict.items():
            c.drawString(60, y, f"{key}:")
            c.drawString(250, y, str(val))
            y -= 20
            if y < 80:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 12)

        # Section: Prediction Result
        y -= 10
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Prediction Result")
        y -= 25
        c.setFont("Helvetica", 12)

        result_color = (0, 0.6, 0) if "No" in result_text else (0.8, 0, 0)
        c.setFillColorRGB(*result_color)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y, result_text)
        c.setFillColorRGB(0, 0, 0)

        y -= 60
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(width / 2, y, "This report is generated using a predictive model for educational purposes only.")

        # Finalize
        c.save()
        buffer.seek(0)

        # Download button
        st.download_button(
            label="📄 Download Report as PDF",
            data=buffer,
            file_name="heart_risk_report.pdf",
            mime="application/pdf"
        )



# Function to create a download link for a DataFrame as a CSV file
def get_binary_file_downloader_html(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="predictions.csv">Download Predictions CSV</a>'
    return href


with tab2:
    st.subheader("📤 Upload CSV for Batch Prediction")

    st.subheader('📌 Note Before Uploading:')
    st.info("""
        - Dataset must have exactly **13 columns** in this order: 
        age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
        - No missing (`NaN`) values
        - All features must follow proper encoding.
    """)


    # Create a file uploader in the sidebar
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read CSV file
        input_data = pd.read_csv(uploaded_file)

        expected_columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 
                            'fbs', 'restecg', 'thalach', 'exang', 
                            'oldpeak', 'slope', 'ca', 'thal']

        if set(expected_columns).issubset(input_data.columns):
            try:
                # Make predictions
                predictions = logistic_model.predict(input_data[expected_columns])
                input_data['Prediction'] = ['No disease' if p == 0 else 'Disease' for p in predictions]

                # Display predictions
                st.success("✅ Predictions successfully generated!")
                st.dataframe(input_data)

                # Download link
                st.markdown(get_binary_file_downloader_html(input_data), unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error making predictions: {e}")
        else:
            st.warning("⚠️ The uploaded file must contain the correct columns in the correct format.")

    else:
        st.info("Upload a CSV file to get heart disease predictions.")



