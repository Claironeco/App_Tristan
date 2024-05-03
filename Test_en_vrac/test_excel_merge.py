import streamlit as st
import pandas as pd
import os

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

def main():
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
