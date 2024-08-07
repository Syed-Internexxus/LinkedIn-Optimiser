import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import fitz  # PyMuPDF
from google.auth.transport.requests import Request  # Import the Request object
from prompts import FirstName_LastName
from prompts import data

# Path to the client_secret.json file

# Scopes required by the API
SCOPES = ['https://www.googleapis.com/auth/documents']

# Function to authenticate and create the Google Docs service
def authenticate_google_docs():
    creds = None
    token_path = 'token.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('docs', 'v1', credentials=creds)
    return service

# Function to extract detailed content from PDF
def extract_detailed_content_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    content = []

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:  # text block
                for line in block["lines"]:
                    for span in line["spans"]:
                        content.append({
                            "text": span["text"],
                            "font": span["font"],
                            "size": span["size"],
                            "bold": bool(span["flags"] & 2),
                            "italic": bool(span["flags"] & 1),
                            "color": span["color"],
                            "bbox": span["bbox"]  # bounding box for positioning
                        })
    return content

# Function to create Google Doc with formatted content
def create_google_doc_with_formatting(service, title, content):
    # Create a new Google Doc
    document = service.documents().create(body={'title': title}).execute()
    document_id = document.get('documentId')

    requests = []
    index = 1

    for item in content:
        text = item["text"]
        text_style = {
            "bold": item["bold"],
            "italic": item["italic"],
            "weightedFontFamily": {
                "fontFamily": item["font"],
                "weight": item["size"]
            },
            "foregroundColor": {
                "color": {
                    "rgbColor": {
                        "red": (item["color"] >> 16 & 255) / 255.0,
                        "green": (item["color"] >> 8 & 255) / 255.0,
                        "blue": (item["color"] & 255) / 255.0
                    }
                }
            }
        }
        requests.append({
            "insertText": {
                "location": {"index": index},
                "text": text
            }
        })
        requests.append({
            "updateTextStyle": {
                "range": {
                    "startIndex": index,
                    "endIndex": index + len(text)
                },
                "textStyle": text_style,
                "fields": "bold,italic,weightedFontFamily,foregroundColor"
            }
        })
        index += len(text)

    # Execute the batch update request
    result = service.documents().batchUpdate(
        documentId=document_id, body={'requests': requests}).execute()

    print(f'Document created with ID: {document_id}')
    print(f'Document URL: https://docs.google.com/document/d/{document_id}/edit')

if __name__ == "__main__":
    pdf_path = 'exportedresume.pdf'
    title = f'Resume_{FirstName_LastName(data).upper}'

    # Authenticate and create the Google Docs service
    service = authenticate_google_docs()

    # Extract detailed content from the PDF
    content = extract_detailed_content_from_pdf(pdf_path)

    # Create Google Doc with the extracted content
    create_google_doc_with_formatting(service, title, content)
