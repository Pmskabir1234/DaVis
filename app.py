import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='DaVis', page_icon='📊', layout='centered')

st.title("Welcome to DaVis")
st.header("Your data decoder,visualizer buddy")

st.divider()
st.write("\n")

loaded_file = st.file_uploader("Upload your csv file",type=['csv'])
if loaded_file is not None:
    df = pd.read_csv(loaded_file)
    if st.button("Click here to see tabular preview"):
        st.dataframe(df)

    st.write("Visualising Options")
    column = st.selectbox("Choose a column:",df.columns.unique())
    fig, axs = plt.subplots()
    axs.bar(df.index,df[column])
    axs.set_title(f'Visuaizing {column}')
    axs.set_ylabel(f'{column}')
    axs.set_xlabel(f'Index')
    st.pyplot(fig)




    

