from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
import os
import openai
import dateutil.parser as parser
import csv
import os.path


# This Function is to get the emails from the Gmail Account.
def scrap_mail_func():
    """This function uses the Gmail API to fetch the Mails from the associated Account

    Returns:
        String: "Done"
    """
    # Creating a storage.JSON file with authentication details
    SCOPES = "https://www.googleapis.com/auth/gmail.modify"  # we are using modify and not readonly, as we will be marking the messages Read
    store = file.Storage("storage.json")
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
        creds = tools.run_flow(flow, store)
    GMAIL = discovery.build("gmail", "v1", http=creds.authorize(Http()))

    user_id = "me"
    label_id_one = "INBOX"
    # label_id_two = "SENT"

    # Getting all the unread messages from Inbox
    # labelIds can be changed accordingly
    unread_msgs = (
        GMAIL.users()
        .messages()
        .list(userId="me", labelIds=[label_id_one], maxResults=10)
        .execute()
    )

    # We get a dictonary. Now reading values for the key 'messages'
    mssg_list = unread_msgs["messages"]

    final_list = []

    for mssg in mssg_list:
        temp_dict = {}
        m_id = mssg["id"]  # get id of individual message
        message = (
            GMAIL.users().messages().get(userId=user_id, id=m_id).execute()
        )  # fetch the message using API
        payld = message["payload"]  # get payload of the message
        headr = payld["headers"]  # get header of the payload

        for one in headr:  # getting the Subject
            if one["name"] == "Subject":
                msg_subject = one["value"]
                temp_dict["Subject"] = msg_subject
            else:
                pass

        for two in headr:  # getting the date
            if two["name"] == "Date":
                msg_date = two["value"]
                date_parse = parser.parse(msg_date)
                m_date = date_parse.date()
                temp_dict["Date"] = str(m_date)
            else:
                pass

        for three in headr:  # getting the Sender
            if three["name"] == "From":
                msg_from = three["value"]
                temp_dict["Sender"] = msg_from
            else:
                pass

        temp_dict["Snippet"] = message["snippet"]  # fetching message snippet

        try:

            # Fetching message body
            mssg_parts = payld["parts"]  # fetching the message parts
            part_one = mssg_parts[0]  # fetching first element of the part
            part_body = part_one["body"]  # fetching body of the message
            part_data = part_body["data"]  # fetching data from the body
            clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
            clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
            clean_two = base64.b64decode(
                bytes(clean_one, "UTF-8")
            )  # decoding from Base64 to UTF-8
            soup = BeautifulSoup(clean_two, "lxml")
            mssg_body = soup.body()
            # mssg_body is a readible form of message body
            # depending on the end user's requirements, it can be further cleaned
            # using regex, beautiful soup, or any other method
            temp_dict["Message_body"] = mssg_body

        except:
            pass

        print(temp_dict)
        final_list.append(
            temp_dict
        )  # This will create a dictonary item in the final list

        # This will mark the messagea as read
        GMAIL.users().messages().modify(
            userId=user_id, id=m_id, body={"removeLabelIds": ["UNREAD"]}
        ).execute()

    print("Total messaged retrived: ", str(len(final_list)))

    """

    The final_list will have dictionary in the following format:

    {   'Sender': '"email.com" <name@email.com>', 
        'Subject': 'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet', 
        'Date': 'yyyy-mm-dd', 
        'Snippet': 'Lorem ipsum dolor sit amet'
        'Message_body': 'Lorem ipsum dolor sit amet'}


    The dictionary can be exported as a .csv or into a databse
    """
    file_path = "scrapped_email.csv"

    # Check if file exists
    if os.path.isfile(file_path):
        # Append to existing file
        with open(file_path, "a", encoding="utf-8", newline="") as csvfile:
            fieldnames = ["Sender", "Subject", "Date", "Snippet", "Message_body"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=",")
            for val in final_list:
                writer.writerow(val)
    else:
        # Create new file
        with open(file_path, "w", encoding="utf-8", newline="") as csvfile:
            fieldnames = ["Sender", "Subject", "Date", "Snippet", "Message_body"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=",")
            writer.writeheader()
            for val in final_list:
                writer.writerow(val)

    return "done"


# This Function is used to summarize the Mails using the OpenAI.
def email_summary(mail, subject, sender_id):
    """Using the OpenAI to summarize the Mails

    Args:
        mail (String): The main body of the mail
        subject (String): The subject of the mail
        sender_id (String): Sender ID of the mail

    Returns:
        String: Response
    """
    OPENAI_API_KEY = "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"
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Summarize the given Email. Use this {subject}  and {sender_id} in the summarization. Make sure that every Summary should have all the important points from the Mails and the Summary should be the detailed format. \nMails:{mail}\nSummary:",
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["text"]
