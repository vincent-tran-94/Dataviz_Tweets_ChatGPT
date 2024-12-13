#Librairies pour la visualisation de données 
import plotly.express as px
import streamlit as st
from read_data import *

def page1(df,df2,df3):
    st.header("Description du jeu de données analysé sur Hugging Face")
    st.subheader("Aperçu des données")
    st.write(f"**Nombre total d'observations dans le jeu de données : {len(df)}**")
    st.write(f"**Nombre total de variables : {len(df.columns)}**")
    st.dataframe(df.head())
    significations = {
        "Date": "Date de création du tweet",
        "Tweet": "Texte brut du tweet",
        "Url": "Lien associé au tweet",
        "User": "Nom d'utilisateur ayant publié le tweet",
        "UserCreated": "Date de création du compte utilisateur",
        "UserVerified": "Indique si l'utilisateur est vérifié",
        "UserFollowers": "Nombre de followers de l'utilisateur",
        "UserFriends": "Nombre d'amis de l'utilisateur",
        "Retweets": "Nombre de retweets pour le tweet",
        "Likes": "Nombre de likes pour le tweet",
        "Location": "Localisation mentionnée par l'utilisateur",
        "UserDescription": "Description utilisateur dans son profil",
    }
    
    # Extraire les informations et ajouter la description
    info_data = {
        "Colonne": df.columns,
        "Non-Null Count": df.notnull().sum().values,
        "Type": [str(df[col].dtype) for col in df.columns],
        "Description": [significations.get(col, "Description non disponible") for col in df.columns],
    }
    info_df = pd.DataFrame(info_data)  # Convertir en DataFrame
    st.dataframe(info_df)  # Afficher le tableau dans Streamlit

    st.subheader("Nombre de valeurs manquantes pour chaque variable")
    # Créer un DataFrame avec le nombre de valeurs manquantes et les noms des colonnes
    missing_values = pd.DataFrame({
        "Colonnes": df.columns,
        "Valeurs manquantes": df.isnull().sum()
    }).reset_index(drop=True)

    st.dataframe(missing_values)
    st.subheader("Analyse descriptive globale")
    st.dataframe(df2.describe())
    st.subheader("Aperçu des tweets et description utilisateur")
    st.dataframe(df[['Tweet', 'UserDescription']].head())
    st.subheader("Aperçu des données après le nettoyage")
    st.dataframe(df2[['processed_tweet', 'processed_userdescription']].head())
    st.header("Comparaison d'un autre jeu de données analysé sur Kaggle")
    st.subheader("Aperçu des données")
    st.write(f"**Nombre total d'observations dans le jeu de données : {len(df3)}**")
    st.write(f"**Nombre total de variables : {len(df3.columns)}**")
    st.dataframe(df3.head())

    significations_df3 = {
        "date": "Date de création du tweet",
        "id": "id Uitilisateur",
        "content": "Texte brut du tweet",
        "username": "Nom d'utilisateur ayant publié le tweet",
        "retweet_count": "Nombre de retweets pour le tweet",
        "like_count": "Nombre de likes pour le tweet",
    }

    # Extraire les informations et ajouter la description
    info_data_df3 = {
        "Colonne": df3.columns,
        "Non-Null Count": df3.notnull().sum().values,
        "Type": [str(df3[col].dtype) for col in df3.columns],
        "Description": [significations_df3.get(col, "Description non disponible") for col in df3.columns],
    }
    info_df3 = pd.DataFrame(info_data_df3)  # Convertir en DataFrame
    st.dataframe(info_df3)  # Afficher le tableau dans Streamlit
    st.subheader("Nombre de valeurs manquantes pour chaque variable")
    # Créer un DataFrame avec le nombre de valeurs manquantes et les noms des colonnes
    missing_values_df3 = pd.DataFrame({
        "Colonnes": df3.columns,
        "Valeurs manquantes": df3.isnull().sum()
    }).reset_index(drop=True)
    st.dataframe(missing_values_df3)
    st.subheader("Analyse descriptive globale")
    st.dataframe(df3.describe())

    


def page2(df2):
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
        user_description = user_tweets["UserDescription"].iloc[0]  # Récupère la description de l'utilisateur

        st.markdown(f"### Métriques pour l'utilisateur : **{selected_user}**")
        st.markdown(f"**Description de l'utilisateur :** {user_description}")  # Affiche la description

        col1, col2, col3 = st.columns(3)
        col1.metric("Nombre de Likes", int(user_data["total_likes"]))
        col2.metric("Nombre de Retweets", int(user_data["total_retweets"]))
        col3.metric("Total de Tweets postés", user_data["total_tweets"])

        col4, col5, col6 = st.columns(3)
        col4.metric("Nombre de Followers", int(user_data["total_followers"]))
        col5.metric("Nombre d'amis", int(user_data["total_friends"]))
        col6.metric("Total de mots uniques", user_data["unique_words"])

        st.markdown("Liste des URLs associées :")
        user_tweets_table = user_tweets[["Date", "Tweet", "Url"]].rename(
            columns={
                "Date": "Date",
                "Tweet": "Tweet posté",
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


def page3(df2):
    tab1, tab2 = st.tabs([
        "👍 Relation Likes et Retweets",
        "📶 Periode d'analyse de données en jour, semaine et mois",
    ])

    tab3,tab4, tab5 = st.tabs([
        "📊 Top utilisateurs les plus actifs sur Twitter",
        "🔠 Wordcloud de mots",
        "🎯 Analyse des hashtags et des mentions d’utilisateurs"
    ])

    with tab1:
        st.subheader("Filtrage dynamique des Likes et Retweets")
        
        # Création de colonnes pour aligner les sliders à droite de la figure
        col1, col2 = st.columns([2, 1])  # Largeur relative : figure (3 parts), sliders (1 part)

        # Colonne droite : sliders
        with col2:
            st.markdown("### Ajustez les filtres :")
            
            # Widgets pour définir les plages de Likes et Retweets
            min_like_count, max_like_count = st.slider(
                "Plage des Likes",
                min_value=int(df2['Likes'].min()),
                max_value=int(df2['Likes'].max()),
                value=(150, 1500)
            )
            min_retweet_count, max_retweet_count = st.slider(
                "Plage des Retweets",
                min_value=int(df2['Retweets'].min()),
                max_value=int(df2['Retweets'].max()),
                value=(50, 300)
            )
            

            # Convertir les colonnes en numérique avec gestion des erreurs
            df2['Likes'] = pd.to_numeric(df2['Likes'], errors='coerce')
            df2['Retweets'] = pd.to_numeric(df2['Retweets'], errors='coerce')

            # Filtrer les données selon les plages sélectionnées
            df2_filtered = df2[
                (df2['Likes'] <= max_like_count) & 
                (df2['Likes'] >= min_like_count) & 
                (df2['Retweets'] <= max_retweet_count) & 
                (df2['Retweets'] >= min_retweet_count)
            ]
        
        # Colonne gauche : graphique de dispersion
        with col1:
            # Créer un graphique de dispersion
            fig = px.scatter(
                df2_filtered,
                x='Likes',
                y='Retweets',
                color='Likes',
                hover_data=['User'],
                color_continuous_scale=[
                    (0, "#ff7f00"),  # Couleur pour les faibles densités
                    (0.5, "#e5e619"),                   
                    (1, "#16bb26")  # Couleur pour les densités élevées
                ]
            )

            # Personnaliser la mise en page
            fig.update_layout(
                title={
                    'text': "Relation entre Likes et Retweets",
                    'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'
                },
                xaxis=dict(
                    title='Nombre de Likes',
                    showgrid=True, gridcolor='lightgrey', gridwidth=0.5,
                    zeroline=True, zerolinecolor='black'
                ),
                yaxis=dict(
                    title='Nombre de Retweets',
                    showgrid=True, gridcolor='lightgrey', gridwidth=0.5,
                    zeroline=True, zerolinecolor='black'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                height=600,
                width=800
            )

            # Afficher le graphique
            st.plotly_chart(fig)


    with tab2:
        st.subheader("Distribution des Tweets par Date")

        # Convertir la colonne "Date" en datetime si ce n'est pas déjà fait
        df2['Date'] = pd.to_datetime(df2['Date'])
        df2['Date'] = df2['Date'].dt.date

        # Définir la date minimale et maximale des tweets
        min_date = df2['Date'].min()
        max_date = df2['Date'].max()

        # Créer deux colonnes pour la disposition du graphique et des sliders
        col1, col2 = st.columns([2, 1]) 

        # Colonne droite : sliders de date
        with col2:
            st.markdown("### Ajustez la période des tweets")
            # Utiliser un slider pour sélectionner la plage de dates
            selected_start_date, selected_end_date = st.slider(
                "Sélectionnez la période des tweets",
                min_value=min_date,
                max_value=max_date,
                value=(min_date, max_date),
                format="YYYY-MM-DD"
            )
        # Colonne gauche : graphique de distribution des tweets
        with col1:
            # Filtrer les données en fonction de la plage de dates sélectionnée
            df_filtered_by_date = df2[(df2['Date'] >= selected_start_date) & (df2['Date'] <= selected_end_date)]

            # Compter la fréquence des tweets par date
            date_distribution = df_filtered_by_date["Date"].value_counts().reset_index()
            date_distribution.columns = ["Date", "TweetCount"]
            date_distribution = date_distribution.sort_values("Date")  # Trier par date

            # Créer un graphique à barres
            fig = px.bar(
                date_distribution,
                x="Date",
                y="TweetCount",
                color='TweetCount',  # Remplacez par une colonne pertinente si disponible
                title="Distribution des tweets par période",
                color_continuous_scale=[ 
                    (0, "#ADD8E6"),  # Couleur pour les faibles densités
                    (0.5, "#0047AB"),  # Couleur pour les densités moyennes
                    (1, "#FFD700")  # Couleur pour les densités élevées
                ]
            )

            # Personnalisation du graphique
            fig.update_traces(textposition="outside")
            fig.update_layout(
                width=800,
                height=500,
                coloraxis_colorbar=dict(
                    title="Quantité de Tweets",  # Titre de la barre de couleur
                    ticks="outside",
                ),
                xaxis=dict(
                    title='Date de publication',
                    showgrid=True, gridcolor='lightgrey', gridwidth=0.5,
                ),
                yaxis=dict(
                    title='Nombre de tweets',
                    showgrid=True, gridcolor='lightgrey', gridwidth=0.5,
                ),
            )

            # Afficher le graphique
            st.plotly_chart(fig)


    with tab3:
        tweets_by_user = df2.groupby('User').size().sort_values(ascending=False)
        # Créer le graphique avec une échelle de couleurs basée sur le nombre de tweets
        fig_users = px.bar(
            y=tweets_by_user.index[:20][::-1],  # Inverser pour avoir l'ordre décroissant de haut en bas
            x=tweets_by_user[:20][::-1],       # Correspondance des valeurs
            title='Top 20 des utilisateurs actifs entre novembre 2022 à février 2023',
            orientation='h',
            color=tweets_by_user[:20][::-1],   # Utiliser le nombre de tweets pour la couleur
            color_continuous_scale=[(0, "#ADD8E6"), (1, "#0047AB")] # Choisir une échelle de couleur (exemple : 'Viridis', 'Plasma', 'Cividis', etc.)
        )

        # Ajuster les options de la mise en page
        fig_users.update_layout(
            width=800,
            height=500,
            coloraxis_colorbar=dict(
                title="Quantité de Tweets",  # Titre de la barre de couleur
                ticks="outside",
            ),
            xaxis=dict(
                title='Total de Tweets',
                showgrid=True, gridcolor='lightgrey', gridwidth=0.5,
            ),
            yaxis=dict(
                title='Nom des utilisateurs',
                showgrid=True, gridcolor='lightgrey', gridwidth=0.5,
            ),
        )

        st.plotly_chart(fig_users)

    with tab4:
        col1, col2 = st.columns(2) 
        with col1: 
            st.image("data/output_png/twitter_wordcloud.png")
            st.markdown("""
            <div style="font-size: 25px; font-weight: bold;">
                Meilleurs mots (De novembre 2022 à février 2023)
            </div>
            """,
            unsafe_allow_html=True)
            st.image("data/output_png/twitter_wordcloud_2.png")
            st.markdown("""
            <div style="font-size: 25px; font-weight: bold;">
                Meilleurs mots (De janvier à mars 2023)
            </div>
            """,
            unsafe_allow_html=True)
            st.image("data/output_png/twitter_wordcloud_3.png")
            st.markdown("""
            <div style="font-size: 25px; font-weight: bold;">
                Analyse des Mots fréquents dans les descriptions utilisateurs
            </div>
            """,
            unsafe_allow_html=True)
        with col2: 
            top_words_first = pd.read_csv("data/output_csv/word_counts.csv")
            top_words_second = pd.read_csv("data/output_csv/word_counts_2.csv")
            top_words_third = pd.read_csv("data/output_csv/word_counts_3.csv")
        
            top_number_words = 20
           
            # Premier graphique interactif
            st.subheader("Top 20 des Mots Clés les Plus Populaires dans Environ 200 000 Tweets (Novembre 2022 à Février 2023)")
            fig1 = px.bar(
                top_words_first.head(top_number_words),
                x="Count",
                y="Word",
                orientation='h',
                labels={"Count": "Total", "Word": "Mot"},
                color="Count",  # Ajoute une couleur basée sur le nombre d'occurrences
                color_continuous_scale="Magma"  # Palette de couleurs
            )
            fig1.update_layout(xaxis=dict(showgrid=True, gridcolor='lightgrey', gridwidth=0.5),yaxis=dict(categoryorder="total ascending",showgrid=True, gridcolor='lightgrey', gridwidth=0.5))  # Trie par ordre croissant
            st.plotly_chart(fig1)

            # Deuxième graphique interactif
            st.subheader("Top 20 des Mots Clés les Plus Populaires basé sur un article de 500 000 Tweets (Janvier à Mars 2023)")
            fig2 = px.bar(
                top_words_second.head(top_number_words),
                x="Count",
                y="Word",
                orientation='h',
                labels={"Count": "Total", "Word": "Mot"},
                color="Count",  # Ajoute une couleur basée sur le nombre d'occurrences
                color_continuous_scale="Magma"  # Palette de couleurs différente
            )
            fig2.update_layout(xaxis=dict(showgrid=True, gridcolor='lightgrey', gridwidth=0.5),yaxis=dict(categoryorder="total ascending",showgrid=True, gridcolor='lightgrey', gridwidth=0.5))  # Trie par ordre croissant
            st.plotly_chart(fig2)

            # Troisième graphique interactif
            st.subheader("Top 20 des Mots Clés les Plus Pertinents dans les Descriptions Utilisateurs")
            fig3 = px.bar(
                top_words_third.head(top_number_words),
                x="Count",
                y="Word",
                orientation='h',
                labels={"Count": "Total", "Word": "Mot"},
                color="Count",  # Ajoute une couleur basée sur le nombre d'occurrences
                color_continuous_scale="Cividis"  # Palette de couleurs différente
            )
            fig3.update_layout(xaxis=dict(showgrid=True, gridcolor='lightgrey', gridwidth=0.5),yaxis=dict(categoryorder="total ascending",showgrid=True, gridcolor='lightgrey', gridwidth=0.5))  # Trie par ordre croissant
            st.plotly_chart(fig3)


    with tab5:
        top_hashtags = pd.read_csv("data/output_csv/top_hashtags.csv")
        top_mentions = pd.read_csv("data/output_csv/top_mentions.csv")
        top_number_hashtags = 10 
        top_number_mentions = 10 

        # Diagramme circulaire interactif pour les hashtags
        fig_hashtags = px.pie(top_hashtags.head(top_number_hashtags), 
                            width=600,
                            height=500,
                            values='Count', 
                            names='Hashtag', 
                            title='Top 10 Hashtags',
                            color_discrete_sequence=px.colors.sequential.RdBu)

        # Diagramme circulaire interactif pour les mentions d’utilisateurs
        fig_mentions = px.pie(top_mentions.head(top_number_mentions), 
                            width=600,
                            height=500,
                            values='Count', 
                            names='Mention', 
                            title='Top 10 Mentions',
                            color_discrete_sequence=px.colors.sequential.Blues_r)

        # Création de deux colonnes pour afficher les graphiques côte à côte
        col1, col2 = st.columns(2)  # Divise la page en 2 colonnes égales

        with col1:
            st.plotly_chart(fig_hashtags)  # Affiche le premier graphique dans la première colonne

        with col2:
            st.plotly_chart(fig_mentions)  # Affiche le deuxième graphique dans la deuxième colonne

    return tab1, tab2, tab3, tab4, tab5
