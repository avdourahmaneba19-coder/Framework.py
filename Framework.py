import streamlit as st
import pandas as pd # Utile pour structurer les données du graphique
import plotly.express as px # La bibliothèque pour le diagramme

# 1. Configuration de la page
st.set_page_config(page_title="Objectif Diplôme v4", page_icon="🎓", layout="wide") # Passage en layout large pour le graphique

st.title("🎓 Objectif Diplôme")
st.write("Personnalisez vos matières, visualisez vos résultats et atteignez vos objectifs.")

st.divider()

# 2. Gestion du nombre de matières (Session State)
if "nb_matieres" not in st.session_state:
    st.session_state.nb_matieres = 3 # On commence direct avec 3 pour le test

col_btn1, col_btn2, _ = st.columns([1, 1, 2]) # Un peu d'espace à droite
with col_btn1:
    if st.button("➕ Ajouter", use_container_width=True):
        st.session_state.nb_matieres += 1
with col_btn2:
    if st.button("➖ Retirer", use_container_width=True) and st.session_state.nb_matieres > 1:
        st.session_state.nb_matieres -= 1

st.divider()

# 3. La Boucle avec le Nom des Matières
st.header("1. Vos Matières actuelles")

list_noms = []
list_notes = []
list_coefficients = []

for i in range(st.session_state.nb_matieres):
    # On crée une ligne propre avec 3 colonnes : Nom, Note, Coefficient
    c1, c2, c3 = st.columns([3, 1, 1])
    
    with c1:
        # Valeurs par défaut différentes pour s'amuser
        noms_defaut = ["Maths", "Python", "Géographie", "Droit", "Anglais"]
        val_nom = noms_defaut[i] if i < len(noms_defaut) else f"Matière {i+1}"
        nom_matiere = st.text_input(f"Matière {i+1} :", value=val_nom, key=f"nom_{i}")
    with c2:
        val_note = 12.0 + (i % 3) # Notes fictives pour le test
        note = st.number_input(f"Note / 20 :", min_value=0.0, max_value=20.0, value=val_note, step=0.5, key=f"note_{i}")
    with c3:
        val_coef = 2 + (i % 2)
        coef = st.number_input(f"Coef :", min_value=1, max_value=10, value=val_coef, key=f"coef_{i}")
        
    list_noms.append(nom_matiere)
    list_notes.append(note)
    list_coefficients.append(coef)

st.divider()

# 4. L'examen final et l'objectif
st.header("2. Votre Objectif")
c_target1, c_target2 = st.columns(2)
with c_target1:
    coef_final = st.number_input("Coefficient de l'examen final :", min_value=1, max_value=10, value=4)
with c_target2:
    note_cible = st.slider("Moyenne générale visée :", min_value=10.0, max_value=20.0, value=12.0, step=0.5)

st.divider()

# 5. Calculs, Verdict et Diagramme
st.header("3. Analyse et Résultats")

# On structure tout dans deux colonnes : Gauche pour le texte, Droite pour le graphique
col_result, col_chart = st.columns([1, 1])

with col_result:
    # Calculs mathématiques
    points_acquis = sum(n * c for n, c in zip(list_notes, list_coefficients))
    somme_coef_actuels = sum(list_coefficients)
    
    total_coefficients = somme_coef_actuels + coef_final
    points_totaux_necessaires = note_cible * total_coefficients
    points_restants = points_totaux_necessaires - points_acquis
    
    note_requise = points_restants / coef_final
    moyenne_actuelle = points_acquis / somme_coef_actuels
    
    st.metric(label="Votre moyenne actuelle", value=f"{moyenne_actuelle:.2f} / 20")
    
    if note_requise <= 0:
        st.success(f"🎉 Objectif déjà atteint ! Moyenne finale > {note_cible}/20 peu importe la note finale.")
    elif note_requise > 20:
        st.error(f"⚠️ Impossible d'atteindre {note_cible}/20. Il faudrait {note_requise:.2f}/20 à l'examen final.")
    else:
        st.info(f"🎯 Pour obtenir {note_cible}/20 de moyenne générale, il vous faut **{note_requise:.2f}/20** à l'examen final.")

with col_chart:
    st.subheader("Visualisation de vos Notes")
    
    # Étape A : On prépare les données dans un DataFrame Pandas
    # C'est le format que Plotly préfère
    df = pd.DataFrame({
        'Matière': list_noms,
        'Note': list_notes,
        'Coefficient': list_coefficients
    })
    
    # Étape B : On crée le graphique à barres interactif
    fig = px.bar(
        df, 
        x='Matière', 
        y='Note', 
        color='Note', # La couleur change selon la note (plus c'est haut, plus c'est vert)
        color_continuous_scale='RdYlGn', # Échelle Rouge -> Jaune -> Vert
        range_y=[0, 20], # On force l'axe Y de 0 à 20
        title="Répartition des Notes Actuelles",
        text='Note' # Affiche la note au-dessus de chaque barre
    )
    
    # Améliorations esthétiques du graphique
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside') # Formate le texte
    fig.update_layout(xaxis_tickangle=-45) # Incline les noms des matières si trop longs
    
    # Étape C : On affiche le graphique Plotly dans Streamlit
    st.plotly_chart(fig, use_container_width=True)