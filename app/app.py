import streamlit as st

from visualisation import *
from read_data import *


path_csv_1 = "data/input_csv/tweets_users_chatgpt.csv"
path_csv_2 = "data/output_csv/tweets_preprocess.csv"

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
        st.session_state.data_loaded = True
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {str(e)}")
        st.stop()

df = st.session_state.df
df2 = st.session_state.df2

#Filtrer chaque metrique des utilisateurs
user_metrics = (
    df2.groupby("User")
    .agg(
        total_likes=("Likes", "sum"),
        total_retweets=("Retweets", "sum"),
        total_tweets=("Tweet", "count"),
        total_followers=("UserFollowers", "max"),
        total_friends=("UserFriends","max"),
        unique_words=("processed_tweet", lambda x: sum(count_unique_words(tweet) for tweet in x)),
    )
    .reset_index()
)

# Application principale
st.title("Analyse des Tweets pour des utilisateurs lors de la sortie de ChatGPT")
st.markdown("**Calcul des métriques** : likes, retweets, tweets, followers, amis et nombre de mots différents")

# Métriques globales
st.markdown("### Métriques globales :")
col7, col8, col9, col10 = st.columns(4)
col7.metric("Total global des tweets", len(df2["processed_tweet"]))
col8.metric("Total global des utilisateurs", len(user_metrics["User"]))
col9.metric("Total global des likes", int(df2["Likes"].sum()))
col10.metric("Total global des retweets", int(df2["Retweets"].sum()))


# Filtrer par utilisateur
selected_user = st.selectbox("Choisissez un utilisateur :", user_metrics["User"].unique(),index=None,placeholder="Select user...")
if selected_user:
    user_data = user_metrics[user_metrics["User"] == selected_user].iloc[0]
    user_tweets = df2[df2["User"] == selected_user]
    user_urls = user_tweets["Url"].tolist()  

    st.markdown(f"### Métriques pour l'utilisateur : **{selected_user}**")
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre de Likes", int(user_data["total_likes"]))
    col2.metric("Nombre de Retweets", int(user_data["total_retweets"]))
    col3.metric("Total de Tweets postés", user_data["total_tweets"])

    col4, col5, col6 = st.columns(3)
    col4.metric("Nombre de Followers", int(user_data["total_followers"]))
    col5.metric("Nombre d'amis", int(user_data["total_friends"]))
    col6.metric("Total de mots uniques", user_data["unique_words"])

    st.markdown("Liste des URLs associées :")
    user_tweets_table = user_tweets[["Date", "processed_tweet", "Url"]].rename(
        columns={
            "Date": "Date",
            "processed_tweet": "Cleaning Tweet",
            "Url": "Associated URL"
        }
    )

    #Mettre une balise HTML pour accéder au lien directement sur Streamlit
    user_tweets_table["Associated URL"] = user_tweets_table["Associated URL"].apply(
        lambda url: f'<a href="{url}" target="_blank">{url}</a>')

    # Convertir le DataFrame en HTML
    table_html = user_tweets_table.to_html(escape=False, index=False)
    # Afficher le tableau HTML dans Streamlit
    st.markdown(table_html, unsafe_allow_html=True)



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



page = st.sidebar.radio("Select a page", ["Description global du dataset", "Visualisations globales"])
# Display selected page
if page == "Description global du dataset":
    page1(df,df2)
elif page == "Visualisations globales":
    tab1, tab2, tab3, tab4, tab5 = page2(df2)

    
