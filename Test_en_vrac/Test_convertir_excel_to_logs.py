import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


def Convert_excel_to_convention_logs(excel_file_path,output_file_path):
    # Lire le fichier Excel
    xls = pd.ExcelFile(excel_file_path)

    # Lire chaque feuille de l'Excel et les convertir en DataFrames
    first_row_convention =["Libellé","Dates_d","Dates_f","nPEP","Bénéficiaire","Partenaire","Montant alloué","M_Fonctionnement","M_Investissement","M_Personnel"]
    first_row_log =["Date_ajout","Libellé","nPEP","Nature de la dépense","Année d'imputation","Type de dépense","Bénéficiaire","Libellé","Numéro OM","Numéro EJ",
                    "Numéro Ligne","Montant de la dépense (HTR)","Solde"]
    
    # Transposer les listes pour créer les DataFrames
    convention_df = pd.DataFrame([], columns=first_row_convention)
    logs_df = pd.DataFrame([], columns=first_row_log)

    for sheet_name in xls.sheet_names:
        if sheet_name != "BILAN" and sheet_name != "DATA":
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

            date=df.iloc[6,2] 
            date_parts = date.split(' - ') 

            #Remplir la ligne suivante avec toutes les informations            
            convention_row=[df.iloc[4,2],date_parts[0].strip(),date_parts[1].strip(),df.iloc[4,5],df.iloc[7,2],df.iloc[6,5],df.iloc[8,2],df.iloc[9,2],df.iloc[10,2],df.iloc[11,2]]
            conv_row_df=pd.DataFrame([convention_row],columns=first_row_convention) 
            i=18
            logs_row_df=pd.DataFrame([], columns=first_row_log) 
            while not pd.isnull(df.iloc[i, 0]) : 
                logs_row=["",df.iloc[4,2],df.iloc[4,5],df.iloc[i,0],df.iloc[i,1],df.iloc[i,2],df.iloc[i,3],str(df.iloc[i,4]).replace('\n', ' '),df.iloc[i,5],df.iloc[i,6],
                    df.iloc[i,7],df.iloc[i,8],df.iloc[i,9]] 
                new_logs_row_df=pd.DataFrame([logs_row], columns=first_row_log)
                logs_row_df=pd.concat([logs_row_df,new_logs_row_df], ignore_index=True)
                i=i+1

            convention_df=pd.concat([convention_df, conv_row_df], ignore_index=True) 
            logs_df=pd.concat([logs_df, logs_row_df], ignore_index=True)  

    # Enregistrer les DataFrames en fichiers CSV
    convention_df.to_csv(output_file_path[0], index=False)
    logs_df.to_csv(output_file_path[1], index=False)

    return "Fichiers CSV pour conventions et logs créés avec succès !"




# Appeler la fonction principale
if __name__ == "__main__":
    st.title("Fusion des données Convention et Logs")

    # Afficher les champs de téléchargement des fichiers
    convention_file = st.file_uploader("Sélectionner le fichier convention.excel", type=['xlsx'])

    # Sélectionner le chemin de sortie pour le fichier Excel
    output_conv_file_path = st.text_input("Nom du fichier des conventions csv de sortie :", "conventions1.csv")
    output_log_file_path = st.text_input("Nom du fichier des opérations csv de sortie :", "logs1.csv")

    if st.button("Exporter vers Excel"):        
        first_page_df = pd.read_excel(convention_file, sheet_name='SUBVENTION')
        st.write(first_page_df) 
        Convert_excel_to_convention_logs("Datas/Conventions 2024(1).xlsx",["Datas/"+output_conv_file_path,"Datas/"+output_log_file_path])



