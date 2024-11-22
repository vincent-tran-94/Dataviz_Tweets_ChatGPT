#Librairies pour la visualisation de données 
import plotly.express as px
import streamlit as st
from data_preprocessing import *
from PIL import Image


def page1(df,df2):
    st.subheader("Aperçu des données")
    st.dataframe(df.head())
    st.subheader("Aperçu des tweets et description utilisateur")
    st.dataframe(df[['Tweet', 'UserDescription']].head())
    st.subheader("Aperçu des données après le nettoyage")
    st.dataframe(df2[['processed_tweet', 'processed_userdescription']].head())
    st.subheader("Analyse descriptive des likes et des retweets")
    st.dataframe(df2[['Likes', 'Retweets']].describe())

def page2(df2):
    tab1, tab2, tab3, tab4, tab5= st.tabs([
        "👍 Relation Likes et Retweets",
        "📶 Periode d'analyse de données en jour, semaine et mois",
        "📊 Top utilisateurs les plus actifs sur Twitter",
        "🔠 Wordcloud de mots des tweets ",
        "🎯 Analyse des hashtags et des mentions d’utilisateurs"
    ])
    
    with tab1:
        max_like_count = 1500
        max_retweet_count = 300
        min_like_count = 150
        min_retweet_count = 50

        # Convertir les colonnes en numérique avec gestion des erreurs
        df2['Likes'] = pd.to_numeric(df2['Likes'], errors='coerce')
        df2['Retweets'] = pd.to_numeric(df2['Retweets'], errors='coerce')


        # Filtrer les données
        df2_filtered = df2[
            (df2['Likes'] <= max_like_count) & 
            (df2['Likes'] >= min_like_count) & 
            (df2['Retweets'] <= max_retweet_count) & 
            (df2['Retweets'] >= min_retweet_count)
        ]

        # Créer un graphique de dispersion
        fig = px.scatter(
            df2_filtered,
            x='Likes',
            y='Retweets',
            color='Likes',
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
        # Compter la fréquence des tweets par date
        date_distribution = df2["Date"].value_counts().reset_index()
        date_distribution.columns = ["Date", "TweetCount"]
        date_distribution = date_distribution.sort_values("Date")  # Trier par date
        
                # Créer un graphique à barres
        fig = px.bar(
            date_distribution,
            x="Date",
            y="TweetCount",
            color='TweetCount',  # Remplacez par une colonne pertinente si disponible
            title="Distribution des tweets par période",
            color_continuous_scale=[ (0, "#ADD8E6"),  # Couleur pour les faibles densités
                (0.5,"#0047AB" ),  # Couleur pour les densités moyennes
                (1, "#FFD700")]
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
        st.image("data/twitter_wordcloud.png", caption="Représentation d'un Wordcloud en fonction d'occurrence de mots des tweets ")

    with tab5:
        top_hashtags = pd.read_csv("data/top_hashtags.csv")
        top_mentions = pd.read_csv("data/top_mentions.csv")
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

