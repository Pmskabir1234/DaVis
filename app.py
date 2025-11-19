import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import copy

st.set_page_config(page_title='DaVis', page_icon='📊', layout='centered')

st.markdown(
    "<h1>"
    "<span style='color:blue'>Wel</span>"
    "<span style='color:cyan'>Come</span>"
    " to "
    "<span style='color:red'>Da</span>"
    "<span style='color:pink'>Vis</span>"
    "</h1>",
    unsafe_allow_html= True
)
st.header("Your data decoder,visualizer buddy")

st.divider()
st.write("\n")

loaded_file = st.file_uploader("Upload your csv file",type=(['csv']))

if loaded_file is not None:

    #dataframe reading
    df = pd.read_csv(loaded_file)
    if st.button("Click here to see tabular preview"):
        st.dataframe(df)

    #data visualisation part
    st.write("Visualising Options")
    column = st.selectbox("Choose a column:",df.columns.unique())
    fig, axs = plt.subplots()  
    axs.plot(df.index,df[column])
    axs.set_title(f'Visuaizing {column}')
    axs.set_ylabel(f'{column}')
    axs.set_xlabel(f'Index')   
    st.pyplot(fig)

    #sidebar and filter options
    def filter_dataframe(df):
        df = df.copy()
        with st.sidebar:
            st.header("Filters")

            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    min_val, max_val = float(df[col].min()),float(df[col].max())
                    selected_range = st.slider(
                        f"{col} range",
                        min_val,
                        max_val,
                        (min_val,max_val)
                    )
                    df = df[df[col].between(selected_range[0],selected_range[1])]

                elif pd.api.types.is_categorical_dtype(df[col]) or df[col].dtype == object:
                    vals = st.multiselect(
                        f"Select {col}",
                        df[col].unique(),
                        default=df[col].unique()
                    )
                    df = df[df[col].isin(vals)]
        return df
    
    st.divider()
    st.title("Filtered View options:")
    st.dataframe(filter_dataframe(df))





    

