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
    selected_course_type = st.sidebar.text_input("Enter Course Type:")
    
    # Enter button to trigger filtering
    if st.sidebar.button("Enter"):
        filtered_users = filter_users(user_data_list, selected_cohort, selected_course_type)
        display_users(filtered_users)

def filter_users(user_data_list, selected_cohort, selected_course_type):
    filtered_users = []
    
    # Filter user data based on input criteria
    for user_data in user_data_list:
        if (not selected_cohort or selected_cohort.lower() in user_data.get("cohort", "").lower()) and \
           (not selected_course_type or selected_course_type.lower() in user_data.get("course_type", "").lower()):
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
        if "file_name" in user_data and "file_url" in user_data:
            st.write("Linked File:", user_data["file_name"])
            st.write("File URL:", user_data["file_url"])

            # Download and display the linked file
            file_name = user_data["file_name"]
            file = user_drive.get(file_name)
            st.write("File Content:")
            st.download_button(
                label=f"Download {file_name}",
                data=file.read(),
                file_name=file_name
            )

        st.write("---")  # Divider between user entries

if __name__ == "__main__":
    main()
