import streamlit as st
import pandas as pd
from utils import scrap_mail_func, email_summary
from PIL import Image

# Define routes
HOME = "Collect Emails"
# SINGLE_EMAIL = "Single Email"
SHOW_DETAILED_SUMMARY = "Detailed Summary Search"

# Define a function toi render the appropriate page based on the route
def render_page(route):
    logo = Image.open('logo.png')
    st.image(logo, width=200)
    if route == HOME:
        scrap_email()
    # elif route == SINGLE_EMAIL:
    #     single_email()
    elif route == SHOW_DETAILED_SUMMARY:
        search_by_mail()


def scrap_email():
    """This Function calls the Email Fetch Function to get the mails"""
    st.title("Summary App - MicronetDB")
    if st.button("Email Fetch"):
        scrap_mail_func()
        st.success("Emails Fetched")
    elif st.button("Generate Summary"):
        render_summary()
        st.success("Summary Created")


#Commented Code below is to display the Emails from the CSV file to the main app according to the senderid or subject of the mail.

# def single_email():
#     st.title("Search")
#     if st.button("Search by Sender"):
#         df = pd.read_csv("scrap_email.csv")
#         # Define a list of items
#         senders = list(df["Sender"])

#         # Create a search bar using the text_input widget
#         search_term = st.text_input("Search for a Sender:")

#         # Filter the list of items based on the search term
#         filtered_items = [
#             sender for sender in senders if search_term.lower() in sender.lower()
#         ]

#         # Display the filtered items in a list
#         st.write("Filtered items:")
#         for sender in filtered_items:
#             st.write("- " + sender)

#     elif st.button("Search by Subject"):
#         df = pd.read_csv("scrap_email.csv")
#         # Define a list of items
#         subjects = list(df["Subject"])

#         # Create a search bar using the text_input widget
#         search_term = st.text_input("Search for a Sender:")

#         # Filter the list of items based on the search term
#         filtered_items = [
#             subject for subject in subjects if search_term.lower() in subject.lower()
#         ]

#         # Display the filtered items in a list
#         st.write("Filtered items:")
#         for subject in filtered_items:
#             st.write("- " + subject)


def render_summary():
    """Reading the mails from the CSV files and Passing it to the OpenAI Function"""
    st.title("summary Creator Of Mails")

    if st.button("Summary Generator"):
        df = pd.read_csv("scrap_email.csv")
        final_summary = []
        mails = list(df["Snippet"])
        senderids = list(df["Sender"])
        subjects = list(df["Subject"])
        for i in range(len(senderids)):

            summary_generated = email_summary(
                mail=mails[i], sender_id=senderids[i], subject=subjects[i]
            )
            final_summary.append(summary_generated)

        df_summary = pd.DataFrame(
            {
                "Sender": senderids,
                "Mail": mails,
                "Summary": final_summary,
                "Subject": subjects,
            }
        )
        df_summary.to_csv("mail_summary.csv", index=False)
    st.success("Summary Generation is Done")


def search_by_mail():
    # Load the CSV file
    df = pd.read_csv("mail_summary.csv")

    # Create a text input for the search term
    search_term = st.text_input("Search by Sender ID")

    if st.button("Search By ID"):
        # Filter the data based on the search term
        filtered_data = df[df["Sender"].str.contains(search_term, case=False)]
        # Display the description of the first matching result
        if not filtered_data.empty:
            st.write("Results by Sender Id")
            st.write(filtered_data[0:2]["Summary"])
        else:
            st.write("No matching results found.")

    elif st.button("Search By Subject"):
        filtered_data_subject = df[df["Subject"].str.contains(search_term, case=False)]

        if not filtered_data_subject.empty:
            st.write("Result by Subject")
            st.write(filtered_data_subject[0:2]["Summary"])
        else:
            st.write("No matching results found.")


nav = st.sidebar.radio(
    "Navigation",
    [HOME,SHOW_DETAILED_SUMMARY],
    index=0,
)

# Render the appropriate page based on the current route
render_page(nav)
