import base64
from deta import Deta
import streamlit as st

# Initialize Deta instance
deta = Deta(st.secrets["deta_key"])  # Replace with your Deta project key
user_db = deta.Base('assignment_collection')
user_drive = deta.Drive('assignment')

# Streamlit app
def main():
    st.title("User Information Viewer")

    # Fetch user data from the database
    user_data_list = user_db.fetch().items

    # Text input for filtering by cohort and course type
    selected_cohort = st.sidebar.text_input("Enter Cohort:")
    selected_course_type = st.sidebar.selectbox("Course Type", ["Select Option", "Excel", "Python", "PowerBI", "Tableau", "SQL", "Word File"], key='course_type')
    
    # Enter button to trigger filtering
    if st.sidebar.button("Enter"):
        filtered_users = filter_users(user_data_list, selected_cohort, selected_course_type)
        display_users(filtered_users)

def filter_users(user_data_list, selected_cohort, selected_course_type):
    filtered_users = []
    
    # Filter user data based on input criteria
    for user_data in user_data_list:
        if (not selected_cohort or selected_cohort.lower() in user_data.get("cohort", "").lower()) and \
           (selected_course_type == "Select Option" or selected_course_type.lower() == user_data.get("course_type", "").lower()):
            filtered_users.append(user_data)
    
    return filtered_users

def display_users(users):
    # Display filtered user information
    for user_data in users:
        st.write("Name:", user_data.get("name"))
        st.write("Email:", user_data.get("email"))
        st.write("Cohort:", user_data.get("cohort"))
        st.write("Course Type:", user_data.get("course_type"))

        # Check if the user has a linked file
        if "file_name" in user_data:
            st.write("Linked File:", user_data["file_name"])
            
            # Display a button to trigger the file download
            if st.button("Download " + user_data["file_name"]):
                file_name = user_data["file_name"]
                
                # Get the file data from Deta Drive
                file_data = user_drive.get(file_name)
                
                # Display the file data as a downloadable link
                st.markdown(get_download_link(file_name, file_data), unsafe_allow_html=True)

        st.write("---")  # Divider between user entries

def get_download_link(file_name, file_data):
    # Encode the file data as base64
    file_base64 = base64.b64encode(file_data).decode()
    
    # Create a data URI for the file
    data_uri = f"data:application/octet-stream;base64,{file_base64}"
    
    # Generate a download link using the data URI
    download_link = f'<a href="{data_uri}" download="{file_name}">Click here to download</a>'
    
    return download_link

if __name__ == "__main__":
    main()
