# Local setup and verification

Cloned from https://github.com/Ali-Moukallid/portfolio at commit
`0db228e` on 2026-10-18 into a new `portfolio` subfolder.
The initial local setup did not publish to GitHub. Publication is recorded separately in SUBMISSION.md.
The assignment document and GitHub guide were read as reference; publishing was deferred during initial setup according to the user's request.

## Environment and startup

Python 3.13 with Django 5.2.18 and Pillow 12.3.0, isolated in `.venv`.
Django 5.2 was selected for Python 3.13 compatibility rather than the README's 5.0.2.
`requirements.txt` declares runtime dependencies; `requirements-lock.txt` records
the tested versions. The environment also contains pypdf, used only to read the
provided GitHub guide, which the application does not require.

From this folder in PowerShell, to reproduce setup:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

The server was started in a hidden background process with `--noreload`.
Open http://127.0.0.1:8000/. Logs are in the parent folder:
`django-server.stdout.log` and `django-server.stderr.log`.
Restart the server after source edits when using `--noreload`.

## Findings and minimal fixes

- Added the missing requirements file and a Git ignore file for local artifacts.
- Added missing package `__init__.py` files after test discovery failed with
  `ImportError: attempted relative import with no known parent package`.
- Created the configured static directory. Replaced an external profile placeholder
  that returned HTTP 403 with an equivalent local SVG placeholder.
- Preserved layout, content, routes, models, and application features.

## Verification results

- `manage.py check`: no issues.
- `makemigrations portfolio --check --dry-run`: no model changes detected.
- `manage.py migrate`: no pending migrations; all 19 were already applied.
- `manage.py test portfolio -v 2`: five tests passed, covering public pages,
  invalid submissions, valid submissions and dashboard visibility, CSRF enforcement,
  admin authentication and registered model pages. Tests use a separate temporary database.
- `pip check`: no broken requirements.
- Live HTTP checks: home, current work, collaboration form, custom dashboard,
  admin login, local placeholder and admin CSS all returned HTTP 200.
  Anonymous `/admin/` correctly redirected to login.
- Bootstrap and Font Awesome CDN styles returned HTTP 200.
- Browser visual inspection was not performed.

The original database contains two users, four collaboration requests, and no Project
records. No existing passwords were changed or new persistent administrator created.
A backup is in the parent folder as `professor-db-before-setup.sqlite3`.

The supplied custom `/admin-dashboard/` has no login requirement. The current-work
template displays hardcoded examples, even though its view queries Project records.
Both behaviors were preserved. Settings remain configured for local development.
Existing database records should be reviewed before later public publication.

## Public repository preparation

The supplied database and compiled caches are excluded from the submission.
Run migrations after cloning to create a fresh local database; run
`python manage.py createsuperuser` to create your own administrator.
Set the DJANGO_SECRET_KEY environment variable to a private stable value when
needed. Without it, development uses a random key per process, so sessions
expire on restart. The original example key is no longer used.
