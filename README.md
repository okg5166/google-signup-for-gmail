# Google Signup for Gmail

A Django app that lets users sign up with Google and view their top Gmail emails.

## Features
- Google OAuth2 login (django-allauth)
- Requests full Gmail access (read, send, delete, etc.)
- Shows top 10 emails after login

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
4. Run the server:
   ```bash
   python manage.py runserver
   ```
5. Go to `/admin/` and add a Social Application for Google with your client ID/secret and select your site.
6. Visit `/accounts/login/` to sign in with Google.

## Deploying to Render.com

1. Create a new Web Service on [Render.com](https://render.com/).
2. Connect your repo or upload the code.
3. Set environment variables:
   - `DJANGO_SECRET_KEY` (any random string)
   - `GOOGLE_CLIENT_ID` (from Google Cloud)
   - `GOOGLE_CLIENT_SECRET` (from Google Cloud)
   - `ALLOWED_HOSTS` (set to `*` or your domain)
4. Deploy!
5. After deploy, go to `/admin/` and add a Social Application for Google as above.

## Notes
- For public use, you must submit your app for Google verification if you request full Gmail access.
- For any issues, check logs on Render.com or run locally for debugging. 