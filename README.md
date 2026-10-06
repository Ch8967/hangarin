# Hangarin: Task & To-Do Manager

Django app with Google + GitHub login (django-allauth).

## 1. Local setup
```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations tasks
python manage.py migrate
python manage.py createsuperuser
python manage.py populate          # priorities, categories + fake data
python manage.py runserver
```

## 2. Version control
```bash
git init
git add .
git commit -m "Initial Hangarin project"
git remote add origin <your-repo-url>
git push -u origin main
```

## 3. OAuth credentials (set as environment variables)
| Variable | Where from |
|---|---|
| GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET | Google Cloud Console > APIs & Services > Credentials > OAuth client ID (Web application) |
| GITHUB_CLIENT_ID / GITHUB_CLIENT_SECRET | GitHub > Settings > Developer settings > OAuth Apps |

Redirect / callback URLs to register (add both local and deployed):
- `http://127.0.0.1:8000/accounts/google/login/callback/`
- `http://127.0.0.1:8000/accounts/github/login/callback/`
- `https://<username>.pythonanywhere.com/accounts/google/login/callback/`
- `https://<username>.pythonanywhere.com/accounts/github/login/callback/`

Local example (macOS/Linux): `export GOOGLE_CLIENT_ID=...` etc. before `runserver`.
Windows PowerShell: `$env:GOOGLE_CLIENT_ID="..."`.

## 4. PythonAnywhere deployment
1. Open a Bash console: `git clone <your-repo-url>`, then `mkvirtualenv hangarin --python=python3.10` (or newer) and `pip install -r requirements.txt`.
2. Web tab > Add a new web app > Manual configuration. Set the virtualenv path and source code path.
3. Edit the WSGI file: set the env vars *before* the Django import, e.g.
   ```python
   import os, sys
   sys.path.insert(0, "/home/<username>/hangarin")
   os.environ["DJANGO_SETTINGS_MODULE"] = "hangarin.settings"
   os.environ["DJANGO_SECRET_KEY"] = "a-long-random-string"
   os.environ["DJANGO_DEBUG"] = "0"
   os.environ["GOOGLE_CLIENT_ID"] = "..."
   os.environ["GOOGLE_CLIENT_SECRET"] = "..."
   os.environ["GITHUB_CLIENT_ID"] = "..."
   os.environ["GITHUB_CLIENT_SECRET"] = "..."
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
4. In the console: `python manage.py migrate && python manage.py collectstatic && python manage.py createsuperuser && python manage.py populate`.
5. Web tab > Static files: URL `/static/` -> `/home/<username>/hangarin/staticfiles`. Reload.

## 5. Django Site
`SITE_ID = 1` uses the default `example.com` site. In `/admin/` > Sites, change it to `127.0.0.1:8000` locally or your PythonAnywhere domain when deployed.
