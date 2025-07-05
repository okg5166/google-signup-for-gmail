from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from allauth.socialaccount.models import SocialToken
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os

@login_required
def email_list(request):
    user = request.user
    try:
        token = SocialToken.objects.get(account__user=user, account__provider='google')
    except SocialToken.DoesNotExist:
        return render(request, 'gmail_reader/error.html', {'error': 'No Google token found.'})

    creds = Credentials(
        token=token.token,
        refresh_token=token.token_secret,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=os.environ.get('GOOGLE_CLIENT_ID'),
        client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
        scopes=['https://mail.google.com/']
    )
    service = build('gmail', 'v1', credentials=creds)

    # Get top 10 emails
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])

    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['From', 'Subject']).execute()
        headers = {h['name']: h['value'] for h in msg_data['payload']['headers']}
        snippet = msg_data.get('snippet', '')
        emails.append({
            'from': headers.get('From', ''),
            'subject': headers.get('Subject', ''),
            'snippet': snippet,
        })

    return render(request, 'gmail_reader/email_list.html', {'emails': emails}) 