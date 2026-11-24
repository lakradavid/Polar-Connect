# PolarConnect
### Integrated Polar Science Outreach, Knowledge Repository and Media Dissemination Portal

**Organisation:** Ministry of Earth Sciences (MoES), Government of India  
**Category:** Software | Smart India Hackathon 2024  
**Stack:** Python 3.14 · Django 6.1 · Bootstrap 5 · SQLite (PostgreSQL-ready) · Leaflet.js · Chart.js

---

## Project Overview

PolarConnect is a centralised digital platform that promotes polar science awareness, provides access to scientific research and educational resources, preserves polar expedition knowledge, and disseminates scientific discoveries to students, researchers, educators and the general public.

---

## Features

| Module | Description |
|---|---|
| Authentication | Custom user model, role-based login, signup, profile management |
| Knowledge Repository | Upload, search and download scientific documents and reports |
| Research Publications | Submit, review and browse research papers |
| Learning Centre | Categorised modules, quizzes and progress tracking |
| Polar Expeditions | Records of Indian and international polar expeditions |
| Media Gallery | Image/video gallery with lightbox viewer |
| News & Events | Articles, announcements, event calendar |
| Community Forum | Discussions, Q&A and moderation tools |
| Interactive Polar Map | Leaflet.js map with research stations and landmarks |
| User Dashboard | Progress, bookmarks, notifications per role |
| Admin Dashboard | Charts (Chart.js), statistics, content management |
| Global Search | Cross-module keyword search with filters |

---

## Setup Instructions (Windows)

### 1. Prerequisites
- Python 3.10+ installed and on PATH
- pip installed

### 2. Navigate to project folder
```cmd
cd "C:\Users\asus\OneDrive\Documents\Lovely Proffessional University\sem7 year 4\INT 253\Project"
```

### 3. Install dependencies
```cmd
pip install -r requirements.txt
```

### 4. Apply migrations
```cmd
python manage.py migrate
```

### 5. Load sample data
```cmd
python manage.py loaddata fixtures/sample_data.json
```

### 6. Create superuser (already done if you ran setup)
```cmd
python manage.py createsuperuser
```
Or use the pre-created admin:
- **Email:** `admin@polarconnect.in`
- **Password:** `PolarAdmin@2024`

### 7. Run the development server
```cmd
python manage.py runserver
```

### 8. Open in browser
- **Homepage:** http://127.0.0.1:8000/
- **Admin panel:** http://127.0.0.1:8000/admin/
- **Login:** http://127.0.0.1:8000/accounts/login/
- **Register:** http://127.0.0.1:8000/accounts/register/

---

## Project Structure

```
Project/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── polarconnect/          # Main Django project
│   ├── settings.py
│   ├── urls.py
│   ├── views.py           # Home + global search
│   └── context_processors.py
├── accounts/              # Custom user, auth, notifications
├── dashboard/             # User + admin dashboards
├── repository/            # Knowledge repository
├── research/              # Research publications
├── education/             # Learning modules + quizzes
├── expeditions/           # Polar expeditions
├── media_gallery/         # Photo/video gallery
├── news/                  # News articles + events
├── community/             # Discussion forums
├── stations/              # Research stations + map
├── templates/             # All HTML templates
│   ├── base.html
│   ├── home.html
│   ├── search.html
│   └── <app>/
├── static/
│   ├── css/polarconnect.css
│   └── js/polarconnect.js
├── media/                 # Uploaded files (gitignored)
└── fixtures/
    └── sample_data.json   # Demo data
```

---

## User Roles

| Role | Access |
|---|---|
| Super Admin | Full platform management + Django admin |
| Content Administrator | Manage articles, media, resources |
| Researcher | Upload and manage research papers |
| Educator | Access and share educational resources |
| Student | Learning modules, quizzes, progress tracking |
| General User | Browse all public content |

---

## Default Admin Credentials

| Field | Value |
|---|---|
| Email | admin@polarconnect.in |
| Password | PolarAdmin@2024 |

> **Change this password immediately in any production deployment.**

---

## Important Notes

- Sample expedition and station data is clearly labelled as **demonstration data** throughout the platform. It is not verified official information from NCPOR or any government body.
- For production: change `SECRET_KEY`, set `DEBUG=False`, configure PostgreSQL, and use a proper `ALLOWED_HOSTS`.
- Media files are served by Django's development server. Use a web server (Nginx/Apache) with proper media serving in production.

---

## Technology Stack

- **Backend:** Python 3.14, Django 6.1
- **Database:** SQLite (dev) — PostgreSQL-ready
- **Frontend:** HTML5, CSS3, Bootstrap 5.3
- **Icons:** Font Awesome 6.5
- **Maps:** Leaflet.js 1.9
- **Charts:** Chart.js 4.4
- **Image processing:** Pillow
- **Forms:** django-crispy-forms + crispy-bootstrap5

---

*Built for Smart India Hackathon 2024 — Problem Statement: Integrated Polar Science Outreach, Knowledge Repository and Media Dissemination Portal*
