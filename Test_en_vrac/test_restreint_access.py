import streamlit as st 

users_info = {
    "Batman": {"password": "Robin", "access_level": 1},
    "Sherlock": {"password": "Watson", "access_level": 1},
    "DoctorWho": {"password": "Tardis", "access_level": 2},
    "Shane": {"password": "Carmen", "access_level": 2}
}
 
def login_page():
    st.title("Authentification")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se Connecter"):
        if username in users_info and password == users_info[username]["password"]:
            st.success("Connexion réussie !")
            st.session_state.user_id = username
            st.session_state.access_level = users_info[username]["access_level"]
            st.session_state.logged_in = True  # Marquer l'utilisateur comme connecté
            st.rerun()
        else:
            st.error("Identifiants invalides.")

def main():
    if not st.session_state.get("logged_in"):
        login_page()
        return

    st.sidebar.title("Navigation")

    if st.session_state.access_level == 1:
        page = st.sidebar.radio("Aller à :", ["Page Accessible par tous","Page Accessible par Niveau 1"])
        if page == "Page Accessible par Niveau 1":
            page_accessible_by_level_1()
        elif page == "Page Accessible par tous":
            page_accessible_by_all()
    elif st.session_state.access_level == 2:
        page = st.sidebar.radio("Aller à :", ["Page Accessible par tous","Page Accessible par Niveau 2"])
        if page == "Page Accessible par Niveau 2":
            page_accessible_by_level_2()
        elif page == "Page Accessible par tous":
            page_accessible_by_all()

def page_accessible_by_all():
    st.title("Hello World!") 
    # Ajoutez le contenu de la page accessible par niveau 1 ici

def page_accessible_by_level_1():
    st.title("Page Accessible par Niveau 1")
    st.write("Bienvenue sur la page accessible par les utilisateurs de niveau 1.")
    # Ajoutez le contenu de la page accessible par niveau 1 ici

def page_accessible_by_level_2():
    st.title("Page Accessible par Niveau 2")
    st.write("Bienvenue sur la page accessible par les utilisateurs de niveau 2.")
    # Ajoutez le contenu de la page accessible par niveau 2 ici

if __name__ == "__main__":
    main()