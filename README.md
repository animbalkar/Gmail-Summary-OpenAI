# Gmail-Summary-OpenAI

**What is Gmail Summarizer App?**
- This tool first fetches the Mails from the Workspace and then it creates the Summary of the mails.
----------------
----------------

**Setup Guide to get the Credential.json File:**

Step 1: Enable the API
- In the Google Cloud console, enable the Gmail API.

Step 2: Authorize credentials for a desktop application  

1. In the Google Cloud console, go to Menu menu > APIs & Services > Credentials.
Go to Credentials
2. Click Create Credentials > OAuth client ID.
3. Click Application type > Desktop app.
4. In the Name field, type a name for the credential. This name is only shown in the Google Cloud console.
5. Click Create. The OAuth client created screen appears, showing your new Client ID and Client secret.
6. Click OK. The newly created credential appears under OAuth 2.0 Client IDs.
7. Save the downloaded JSON file as credentials.json, and move the file to your working directory.

*Installing the requirements.* 
- In order to Install the requirements Enter the following command in the Terminal 

>`pip install requirements.txt`

-------------------
-------------------

**To Start the Summary App:**

>`streamlit run main.py`








