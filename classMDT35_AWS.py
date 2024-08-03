import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
from sqlalchemy import create_engine
import pymysql
import time
from datetime import datetime, timedelta
import pickle
from xgboost import XGBClassifier
#from sklearn.tree import DecisionTreeClassifier



# Sidebar radio button for navigation
selcetRadioVar = st.sidebar.radio("Main Menu",["Diabets Checkup"])

# Home page

# Search Buses page    
if selcetRadioVar =="Diabets Checkup":
    
    tab2,tab3 = st.tabs(["xgboost","Project Info"])  
        
    # Content for the second tab
    with tab2:
        tab2.info("Free Diabetes CheckUp based on xgboost model Machine learning, It have 97% of accuracy rate")
        form = st.form(key="diabetesCheckupXgboost")
        # Initialize variables for form inputs   
        float_age = 0.0
        float_bmi = 0.0
        float_HbA1clevel = 0.0
        float_glucoseLevel = 0.0

        gender_int = 0
        bp_int = 0 
        heartDisease_int = 0
        smokingHistory_int = 0

        # Create columns for form inputs
        col1, col2, col3, col4 = form.columns(4)  

        # First column: Gender and smoking history
        with col1:
            gender = col1.selectbox("Select Your Gender", ["Female","Male"])
            smokingHistory = col1.selectbox("Smoking history",["No Info", "current", "ever", "former", "never", "not current"]) 
        # Second column: Age and BMI inputs
        with col2:
            age = col2.text_input("Enter your Age in Number")
            if not age=="":
                float_age = float(age)            
            bmi = col2.text_input("Enter your BMI")
            if not bmi=="":
                float_bmi = float(bmi)  
        # Third column: BP and HbA1c level inputs
        with col3:
            bp = col3.selectbox("Do you have BP",["No","Yes"])
            HbA1clevel = col3.text_input("Enter your HbA1c level")
            if not HbA1clevel=="":
                float_HbA1clevel = float(HbA1clevel)     
        # Fourth column: Heart disease and glucose level inputs
        with col4:
            heartDisease = col4.selectbox("Do you have Heart Disease",["No","Yes"])
            glucoseLevel = col4.text_input("Blood glucose level")    
            if not glucoseLevel=="":
                float_glucoseLevel = float(glucoseLevel)               
            
        # Form submission button
        clickToFind = form.form_submit_button("Click Here")
        # Form validation and model prediction
        if clickToFind:
            if float_age == "" or float_age == " " or float_age == 0.0:
                st.error("Please Enter Age")
            elif float_bmi == "" or float_bmi == " " or float_bmi == 0.0:
                st.error("Please Enter BMI")
            elif float_HbA1clevel == "" or float_HbA1clevel == " " or float_HbA1clevel == 0.0:
                st.error("Please Enter 'HbA1c' Level")            
            elif float_glucoseLevel == "" or float_glucoseLevel == " " or float_glucoseLevel == 0.0:
                st.error("Please Enter Glucose Level")
            else :
                # Convert gender to integer
                if gender =="Female":
                    gender_int = 0
                elif gender =="Male":
                    gender_int = 1
                # Convert BP to integer
                if bp =="No":
                    bp_int = 0
                elif bp =="Yes":
                    bp_int = 1    
                # Convert heart disease to integer
                if heartDisease =="No":
                    heartDisease_int = 0
                elif heartDisease =="Yes":
                    heartDisease_int = 1

                # Convert smoking history to integer
                if smokingHistory =="No Info":
                    smokingHistory_int = 0
                elif smokingHistory =="current":
                    smokingHistory_int = 1
                elif smokingHistory =="ever":
                    smokingHistory_int = 2
                elif smokingHistory =="former":
                    smokingHistory_int = 3
                elif smokingHistory =="never":
                    smokingHistory_int = 4
                elif smokingHistory =="not current":
                    smokingHistory_int = 5

                # Use Pickle to get Trained model file
                with open("XGB.pkl","rb") as trainedFile:
                    sugerCheckup_model = pickle.load(trainedFile) 

                # Prepare the input for prediction
                sugerTestPersonInput = np.array([[gender_int,float_age,bp_int,heartDisease_int,smokingHistory_int,float_bmi,float_HbA1clevel,float_glucoseLevel]])
                checkResult = sugerCheckup_model.predict(sugerTestPersonInput)
                
                # final result position of Diabetes
                if checkResult[0] == 0:
                    st.write("Diabetes Negative")
                    st.success("Congragulation You not have Diabetes, Still make one time medical check to become 100% confident about you medical condition")
                elif checkResult[0] == 1:
                    st.write("Diabetes Positive")
                    st.warning("Sorry You have Diabetes, still this method 97% only accurate, Better make one medical checkup to identify you have diabetes or not, Here their is a change you not have diabetes please make sure viz diabetes medical checkup")

    with tab3:
        st.info("Site Under Development")            

