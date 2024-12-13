import streamlit as st

from visualisation import *
from read_data import *


path_csv_1 = "data/input_csv/tweets_users_chatgpt.csv"
path_csv_2 = "data/output_csv/tweets_preprocess.csv"
path_csv_3 = "data/input_csv/Twitter_article.csv"

st.cache_resource.clear()
st.cache_data.clear()

st.set_page_config(
    page_title="Tweets ChatGPT",
    page_icon="𝕏",
    layout="wide"
)


# Chargement des données avec session_state (Gestion de cookies su)
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if not st.session_state.data_loaded:
    try:
        st.session_state.df = load_data(path_csv_1)
        st.session_state.df2 = load_data(path_csv_2)
        st.session_state.df3 = load_data(path_csv_3)
        st.session_state.data_loaded = True
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {str(e)}")
        st.stop()

df = st.session_state.df
df2 = st.session_state.df2
df3 = st.session_state.df3


# Application principale
st.title("Analyse des Tweets pour des utilisateurs lors de la sortie de ChatGPT")

with st.sidebar:
    st.title("Dashboard sur l'Analyse des Tweets sur ChatGPT")
    st.subheader("Introduction")
    st.markdown("""
    Ce dashboard explore l'impact de ChatGPT sur Twitter en analysant environ 300 000 tweets. 
                        À travers cette étude, nous examinons l'enthousiasme des utilisateurs, 
                        les tendances émergentes et l'évolution de l'outil. L'objectif est de mieux comprendre les perceptions publiques, 
                        les facteurs influençant ChatGPT, et ses applications potentielles. Grâce à des analyses sur le volume de tweets, 
                        le sentiment, l'engagement et les événements clés liés à l'IA, ce dashboard fournit des insights précieux pour 
                        guider les stratégies des entreprises, chercheurs et décideurs.
    """
    )
    st.subheader("Selection de pages")


page = st.sidebar.radio("Select a page", ["Description global du dataset","Recherche par utilisateur","Visualisations globales"])
# Display selected page
if page == "Description global du dataset":
    page1(df,df2,df3)
elif page == "Recherche par utilisateur":
    page2(df2)
elif page == "Visualisations globales":
    tab1, tab2, tab3, tab4, tab5 = page3(df2)


    
