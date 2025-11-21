import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import copy
import openpyxl
import mysql.connector
import bcrypt

st.set_page_config(page_title='DaVis', page_icon='📊', layout='centered')

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='kabir123@',
        database='davis'
)
def hash_pw(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_pw(password,hashed):
    return bcrypt.checkpw(password.encode(),hashed)

def signup_user(username,password):
    db = get_db()
    cur = db.cursor()

    hashed = hash_pw(password)

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)",(username,hashed))
        db.commit()

        return True
    except:
        return False
    
def login_user(username,password):
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT password FROM users WHERE username=%s",(username,))
    result = cur.fetchone()

    if result is None:
        return False
    
    stored_hash = result[0]
    return verify_pw(password,stored_hash)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("One step away....")

    mode = st.selectbox("Choose:",['Login','Sign Up'])
    user = st.text_input("Username")
    pwd = st.text_input("Password",type='password')

    if mode == 'Sign Up':
        if st.button("Create Account"):
            if signup_user(user,pwd):
                st.success("Account Created! You can log in.")
            else:
                st.error("Username already taken!")

    if mode == 'Login':
        if st.button("Log In"):
            if login_user(user,pwd):
                st.session_state.logged_in = True
                st.session_state.current_user = user
                st.rerun()
            else:
                st.error("Invalid login!")
    st.stop()

st.success(f"Welcome {st.session_state.current_user}.....")


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

type_of = st.selectbox("Select the type of your file",['csv','xls','xlsx'])
loaded_file = st.file_uploader("Upload your file",type=([type_of]))

if loaded_file is not None:
    try:
        #dataframe reading
        if type_of == 'csv':
            df = pd.read_csv(loaded_file)
        else:
            df = pd.read_excel(loaded_file)
        if st.button("Click here to see tabular preview"):
            st.dataframe(df)

        #data visualisation part
        st.write("Visualizing Options")
        column = st.selectbox("Choose a column:",[col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])])
        graph_type = st.radio("Plot type",['Plot','Bar','Scatter'])
        plt.style.use('ggplot')  
        fig, axs = plt.subplots()  
        plot_func = getattr(axs, graph_type.lower())
        plot_func(df.index,df[column])
        axs.set_title(f'Visualizing {column}')
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
    
    except Exception as e:
        print(f"The problem is {e}")
        st.error(f"Maybe the file is causing problem...")


st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 8px;
        color: #6c6c6c;
        font-size: 14px;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    </style>

    <div class="footer">
        Built with curiosity and passion @SaadKabir
    </div>
    """,
    unsafe_allow_html=True
)



    

