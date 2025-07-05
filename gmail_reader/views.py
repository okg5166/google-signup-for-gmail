import os
import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Store tokens in session for demo purposes

def home(request):
    return render(request, 'gmail_reader/home.html')

def oauth2callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse('No code provided.')
    # Exchange code for token
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    r = requests.post('https://oauth2.googleapis.com/token', data=data)
    if r.status_code != 200:
        return HttpResponse('Failed to get token: ' + r.text)
    token_data = r.json()
    request.session['google_token'] = token_data
    return redirect('emails')

def emails(request):
    token_data = request.session.get('google_token')
    if not token_data:
        return redirect('home')
    creds = Credentials(
        token=token_data['access_token'],
        refresh_token=token_data.get('refresh_token'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=['https://mail.google.com/']
    )
    service = build('gmail', 'v1', credentials=creds)
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
