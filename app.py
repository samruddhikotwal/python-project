import streamlit as st
import pickle
import numpy as np
# with open('lrmodel_sustainable.pkl','rb') as file:
with open(r"C:\Users\DELL\OneDrive\Desktop\my.py\lrmodel_sustainable.pkl", "rb") as file:
    model = pickle.load(file)
    model=pickle.load(file)
    st.title("sustainability checker!!")
    carbon_emmision=st.number_input("carbon emmision amount:",min_value=0.0,format="%f")
    energy_output=st.number_input("enter the energy output generated:",min_value=0.0,format="%f")
    renewability_index=st.number_input("enter the renewability index values:  ",min_value=0.0,format="%f")
    cost_efficiency=st.number_input("enter the cost efficiency values: ",min_value=0.0,format="%f")

    if st.button("predict"):
        input_data=np.array([[carbon_emmision,energy_output,renewability_index,cost_efficiency]])
        prediction=model.predict(input_data)
        if prediction[0]==1:
           st.success("congre,it is sustainable")
        else:
            st.info("it is not sustainable need")

'''stremlist
numpy
pandas
scikit-learn
matplotlib
seaborn '''


