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

def merge_convention_logs(convention_file_path, logs_file_path):
    # Charger les données des fichiers convention et logs
    convention_df = pd.read_csv(convention_file_path)
    logs_df = pd.read_csv(logs_file_path)

    # Fusionner les données en utilisant une jointure gauche sur la colonne 'Libellé'
    merged_df = pd.merge(convention_df, logs_df, on='Libellé', how='left')

    # Calculer le bilan des dépenses pour chaque convention
    # balance_df = merged_df.groupby('Libellé')['Montant de la dépense (HTR)'].sum().reset_index()
    # balance_df.rename(columns={'Montant': 'Total_Depenses'}, inplace=True)

    # Fusionner le bilan des dépenses avec les données de convention
    # final_df = pd.merge(merged_df, balance_df, on='Libellé', how='left')

    return merged_df # final_df

def export_to_excel(data_frame, output_file_path):
    # Écrire les données dans un fichier Excel
    with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
        data_frame.to_excel(writer, sheet_name='Conventions_Logs', index=False)

########################################        
### Menu principal et fonctionnalité ###
########################################

def main():
    st.sidebar.title("Navigation")

    # Afficher les boutons pour chaque page
    page = st.sidebar.radio("Aller à :", ("Accueil", "Créer une convention", "Modifier une convention", "Enregistrer une opération", "Modifier une opération sur une convention", "Fusionner dans un excel"))

    # Afficher la page sélectionnée
    if page == "Accueil":
        accueil_page()
    elif page == "Créer une convention":
        creer_convention_page()
    elif page == "Modifier une convention":
        modifier_convention_page()
    elif page == "Enregistrer une opération":
        enregistrer_operation_page()
    elif page == "Modifier une opération sur une convention":
        modifier_logs_page()
    elif page == "Fusionner dans un excel":
        merge_convention_logs_page()

#####################################        
### Contenu des différentes pages ###
#####################################

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
        # Vérifier que tous les champs sont remplis
        if all(user_inputs.values()):
            # Créer un DataFrame avec les nouvelles données
            new_data = pd.DataFrame([user_inputs])
            save_data("convention", pd.concat([convention_df, new_data], ignore_index=True))
            st.success("Convention enregistrée avec succès !")
        else:
            st.warning("Veuillez remplir tous les champs avant d'enregistrer la convention.")

# Fonction pour afficher la page "Enregistrer une opération"
def enregistrer_operation_page():
    st.title("Enregistrer une opération sur une convention")
    st.write("Veuillez remplir les informations suivantes :")

    # Obtenir les noms de colonnes du DataFrame
    logs_df = load_data("logs")
    column_names = logs_df.columns.tolist()
    user_inputs = {}

    # Afficher les champs de saisie pour chaque colonne
    for column in column_names:
        user_input = st.text_input(f"Saisir {column}", "")
        user_inputs[column] = user_input

    # Bouton pour enregistrer l'opération
    if st.button("Enregistrer"):
        # Vérifier que tous les champs sont remplis
        if all(user_inputs.values()):
            # Créer un DataFrame avec les nouvelles données
            new_data = pd.DataFrame([user_inputs])
            save_data("logs", pd.concat([logs_df, new_data], ignore_index=True))
            st.success("Opération sur la convention enregistrée avec succès !")
        else:
            st.warning("Veuillez remplir tous les champs avant d'enregistrer l'opération.") 

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

    # Définir une variable de session pour suivre l'état du bouton "Afficher la ligne sélectionnée"
    if 'Btn_affiche_clicked' not in st.session_state:
        st.session_state.Btn_affiche_clicked = False

    # Fonction pour gérer le clic sur le bouton "Afficher la ligne sélectionnée"
    def click_button():
        st.session_state.Btn_affiche_clicked = True

    # Afficher les boutons dans une colonne Bootstrap
    col1, col2 = st.columns(2)

    # Bouton "Afficher la ligne sélectionnée"
    with col1:
        if st.button("Modifier la ligne sélectionnée", on_click=click_button):
            st.session_state.Btn_affiche_clicked = True

    # Bouton "Supprimer la ligne sélectionnée"
    with col2:
        if st.button("Supprimer la ligne sélectionnée", key="supprimer_ligne"):
            # Supprimer la ligne sélectionnée du DataFrame
            convention_df.drop(selected_index, inplace=True)
            # Réinitialiser les index du DataFrame
            convention_df.reset_index(drop=True, inplace=True)
            # Enregistrer les modifications dans le fichier convention.csv
            save_data("convention", convention_df)
            st.success("Ligne supprimée avec succès !")
            st.rerun()

    # Vérifier si le bouton a été cliqué
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
            # Rafraîchir la page
            st.experimental_rerun()


# Fonction pour afficher la page "Modifier une opération sur les conventions"
def modifier_logs_page():
    st.title("Modifier une opération sur les conventions")

    # Charger les données des opérations sur les conventions
    logs_df = load_data("logs")

    # Afficher les Opérations sur les conventions dans un tableau
    st.subheader("Opérations sur les conventions :")
    st.write(logs_df)

    # Sélectionner une ligne à modifier
    selected_index = st.number_input("Entrez l'index de la ligne à modifier :", min_value=0, max_value=len(logs_df)-1, value=0, step=1)

    
    if 'Btn_affiche_clicked' not in st.session_state:
        st.session_state.Btn_affiche_clicked = False
    
    def click_button():
        st.session_state.Btn_affiche_clicked = True
        
    # Afficher les boutons dans une colonne Bootstrap
    col1, col2 = st.columns(2)

    # Bouton "Afficher la ligne sélectionnée"
    with col1:
        if st.button("Modifier la ligne sélectionnée", on_click=click_button):
            st.session_state.Btn_affiche_clicked = True

    # Bouton "Supprimer la ligne sélectionnée"
    with col2:
        if st.button("Supprimer la ligne sélectionnée", key="supprimer_ligne"):
            # Supprimer la ligne sélectionnée du DataFrame
            logs_df.drop(selected_index, inplace=True)
            # Réinitialiser les index du DataFrame
            logs_df.reset_index(drop=True, inplace=True)
            # Enregistrer les modifications dans le fichier logs.csv
            save_data("logs", logs_df)
            st.success("Opération supprimée avec succès !")

    if st.session_state.Btn_affiche_clicked:
        
        # Afficher les détails de la ligne sélectionnée
        selected_row = logs_df.iloc[selected_index]
        st.write("Détails de la ligne sélectionnée :")
        st.write(selected_row)

        # Afficher les champs de saisie pour modifier la ligne
        st.subheader("Modifier les informations :")
        new_values = {}
        for column in logs_df.columns:
            new_value = st.text_input(f"Modifier {column} :", value=selected_row[column], key=f"{column}_{selected_index}")
            new_values[column] = new_value

        # Bouton pour enregistrer les modifications
        if st.button("Enregistrer les modifications", key="enregistrer_modifs"):
            # Mettre à jour la ligne sélectionnée dans le DataFrame
            logs_df.loc[selected_index] = pd.Series(new_values)

            # Enregistrer les modifications dans le fichier logs.csv
            save_data("logs", logs_df)

            st.success("Modification enregistrée avec succès !")
            #Refresh the page
            st.rerun() 

# Fonction pour afficher la page "Modifier une opération sur les conventions"
def merge_convention_logs_page():
    st.title("Fusion des données Convention et Logs")

    # Afficher les champs de téléchargement des fichiers
    convention_file = st.file_uploader("Sélectionner le fichier convention.csv", type=['csv'])
    logs_file = st.file_uploader("Sélectionner le fichier logs.csv", type=['csv'])

    if convention_file is not None and logs_file is not None:
        # Enregistrer les fichiers téléchargés temporairement
        convention_temp_path = "convention_temp.csv"
        logs_temp_path = "logs_temp.csv"
        with open(convention_temp_path, 'wb') as f:
            f.write(convention_file.getvalue())
        with open(logs_temp_path, 'wb') as f:
            f.write(logs_file.getvalue())

        # Fusionner les fichiers et calculer le bilan des dépenses
        merged_data = merge_convention_logs(convention_temp_path, logs_temp_path)

        # Sélectionner le chemin de sortie pour le fichier Excel
        output_file_path = st.text_input("Nom du fichier Excel de sortie :", "conventions_logs_output.xlsx")

        # Bouton pour exporter les données fusionnées vers un fichier Excel
        if st.button("Exporter vers Excel"):
            export_to_excel(merged_data, "Datas/"+output_file_path)
            st.success(f"Données exportées avec succès vers {output_file_path}")

        # Afficher les données fusionnées dans Streamlit
        st.subheader("Données fusionnées Convention et Logs :")
        st.write(merged_data)

        # Supprimer les fichiers temporaires
        os.remove(convention_temp_path)
        os.remove(logs_temp_path)

# Appeler la fonction principale
if __name__ == "__main__":
    main()
