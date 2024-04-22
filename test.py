import streamlit as st
import pandas as pd
import os

# Fonction pour charger les données à partir d'un fichier CSV
def load_data(file):
    file_path = f"Datas/{file}.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()

# Fonction pour enregistrer les données dans un fichier CSV
def save_data(file, data):
    file_path = f"Datas/{file}.csv"
    data.to_csv(file_path, index=False)


def main():
    st.sidebar.title("Navigation")

    # Afficher les boutons pour chaque page
    page = st.sidebar.radio("Aller à :", ("Accueil", "Créer une convention", "Modifier une convention", "Enregistrer une opération"))

    # Afficher la page sélectionnée
    if page == "Accueil":
        accueil_page()
    elif page == "Créer une convention":
        creer_convention_page()
    elif page == "Modifier une convention":
        modifier_convention_page()
    elif page == "Enregistrer une opération":
        enregistrer_operation_page()

# Fonction pour afficher la page "Accueil"
def accueil_page():
    st.title("Page d'Accueil")
    convention_df = load_data("convention")
    st.subheader("Contenu du fichier convention :")
    st.write(convention_df)

# Fonction pour afficher la page "Créer une convention"
def creer_convention_page():
    st.title("Créer une convention")
    st.write("Veuillez remplir les informations suivantes :")

    # Obtenir les noms de colonnes du DataFrame
    convention_df = load_data("convention")
    column_names = convention_df.columns.tolist()
    user_inputs = {}

    # Afficher les champs de saisie pour chaque colonne
    for column in column_names:
        user_input = st.text_input(f"Saisir {column}", "")
        user_inputs[column] = user_input

    # Bouton pour enregistrer la convention
    if st.button("Enregistrer"):
        # Créer un DataFrame avec les nouvelles données
        new_data = pd.DataFrame([user_inputs])
        save_data("convention", pd.concat([convention_df, new_data], ignore_index=True))
        st.success("Convention enregistrée avec succès !")

# Fonction pour afficher la page "Enregistrer une opération"
def enregistrer_operation_page():
    st.title("Enregistrer une opération sur une convention")
    st.write("Veuillez remplir les informations suivantes :")

    # Obtenir les noms de colonnes du DataFrame
    convention_df = load_data("logs")
    column_names = convention_df.columns.tolist()
    user_inputs = {}

    # Afficher les champs de saisie pour chaque colonne
    for column in column_names:
        user_input = st.text_input(f"Saisir {column}", "")
        user_inputs[column] = user_input

    # Bouton pour enregistrer l'opération sur la convention
    if st.button("Enregistrer"):
        # Créer un DataFrame avec les nouvelles données
        new_data = pd.DataFrame([user_inputs])
        save_data("logs", pd.concat([convention_df, new_data], ignore_index=True))
        st.success("Opération sur la convention enregistrée avec succès !")

# Fonction pour afficher la page "Modifier une convention"
def modifier_convention_page():
    st.title("Modifier une convention")

    # Charger les données des conventions
    convention_df = load_data("convention")

    # Afficher les conventions actuelles dans un tableau
    st.subheader("Conventions actuelles :")
    st.write(convention_df)

    # Sélectionner une ligne à modifier
    selected_index = st.number_input("Entrez l'index de la ligne à modifier :", min_value=0, max_value=len(convention_df)-1, value=0, step=1)

    
    if 'Btn_affiche_clicked' not in st.session_state:
        st.session_state.Btn_affiche_clicked = False
    
    def click_button():
        st.session_state.Btn_affiche_clicked = True
        
    st.button("Afficher la ligne sélectionnée",on_click=click_button)

    if st.session_state.Btn_affiche_clicked:
        
        # Afficher les détails de la ligne sélectionnée
        selected_row = convention_df.iloc[selected_index]
        st.write("Détails de la ligne sélectionnée :")
        st.write(selected_row)

        # Afficher les champs de saisie pour modifier la ligne
        st.subheader("Modifier les informations :")
        new_values = {}
        for column in convention_df.columns:
            new_value = st.text_input(f"Modifier {column} :", value=selected_row[column], key=f"{column}_{selected_index}")
            new_values[column] = new_value

        # Bouton pour enregistrer les modifications
        if st.button("Enregistrer les modifications", key="enregistrer_modifs"):
            # Mettre à jour la ligne sélectionnée dans le DataFrame
            convention_df.loc[selected_index] = pd.Series(new_values)

            # Enregistrer les modifications dans le fichier convention.csv
            save_data("convention", convention_df)

            st.success("Modification enregistrée avec succès !")
            #Refresh the page
            st.rerun() 


# Appeler la fonction principale
if __name__ == "__main__":
    main()
