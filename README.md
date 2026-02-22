# 🏨 QuickStay - Hotel Booking Application

A full-featured hotel booking web application built with Flask, PostgreSQL, and Tailwind CSS. QuickStay allows users to browse rooms, make bookings, manage profiles, and provides an admin dashboard for hotel management.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-green?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.x-38B2AC?logo=tailwind-css&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Getting Started](#-getting-started)
  - [Option 1: Docker (Recommended)](#option-1-docker-deployment-recommended)
  - [Option 2: Manual Setup](#option-2-manual-setup)
- [Environment Variables](#-environment-variables)
- [Database Setup](#-database-setup)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Deployment](#-deployment)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### User Features
- 🔐 **Authentication** — Register, Login, Logout with session management
- 🔑 **Password Recovery** — OTP-based password reset via email (Flask-Mail)
- 👤 **Profile Management** — View, edit profile, change password, delete account
- 📥 **Data Export** — Download personal data as JSON (privacy compliance)
- 🌙 **Dark/Light Mode** — Toggle between themes
- 📱 **Fully Responsive** — Works on desktop, tablet, and mobile

### Security Features
- 🛡️ **CSRF Protection** — All forms protected with Flask-WTF
- 🔒 **Password Hashing** — Werkzeug security with salted hashes
- 🚫 **Account Deactivation** — Soft delete with password confirmation
- ⏱️ **OTP Expiry** — Time-limited OTP codes (10 minutes)

### Admin Features
- 📊 **Admin Dashboard** — Manage users, rooms, and bookings
- 👥 **User Management** — View, block/unblock users

### DevOps & CI/CD
- 🐳 **Docker** — Multi-stage Dockerfile with Docker Compose
- 🔄 **Jenkins Pipeline** — Automated CI/CD with auto-deploy
- 🔍 **SonarQube** — Code quality analysis
- 🛡️ **Trivy** — Container security scanning
- 🔎 **OWASP** — Dependency vulnerability check
- 🗄️ **Auto Migrations** — Database migrations on container startup

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Flask 3.1 (Python 3.11) |
| **Database** | PostgreSQL 15 |
| **ORM** | SQLAlchemy + Flask-Migrate (Alembic) |
| **Frontend** | Tailwind CSS + Jinja2 Templates |
| **Icons** | Lucide Icons |
| **Auth** | Flask-Login + Flask-WTF (CSRF) |
| **Email** | Flask-Mail (SMTP/Gmail) |
| **Containerization** | Docker + Docker Compose |
| **CI/CD** | Jenkins Pipeline |
| **Security Scanning** | SonarQube, Trivy, OWASP Dependency-Check |

---

## 📁 Project Structure
```
QuickStay/
│
├── app/
│ ├── init.py # App factory
│ ├── config.py # Configuration (dev/prod/test)
│ ├── utils.py # Helper functions
│ ├── extensions.py # Flask extensions initialization
│ │
│ ├── models/ # Database models
│ │ ├── init.py
│ │ ├── user.py # User model
│ │ ├── room.py # Room model
│ │ ├── booking.py # Booking model
│ │ └── review.py # Review model
│ │
│ ├── controllers/ # Route handlers (Blueprints)
│ │ ├── init.py
│ │ ├── auth_controller.py # Auth routes (login, register, etc.)
│ │ ├── main_controller.py # Public pages (home, about, etc.)
│ │ ├── booking_controller.py # Booking routes
│ │ ├── profile_controller.py # Profile management routes
│ │ └── admin/
│ │ ├── init.py
│ │ └── dashboard_controller.py # Admin dashboard
│ │
│ ├── templates/ # Jinja2 HTML templates
│ │ ├── base.html # Base layout
│ │ ├── auth/ # Auth pages
│ │ │ ├── login.html
│ │ │ ├── register.html
│ │ │ └── forgot-password.html
│ │ ├── main/ # Public pages
│ │ │ ├── home.html
│ │ │ ├── rooms.html
│ │ │ ├── about.html
│ │ │ ├── contact.html
│ │ │ └── faq.html
│ │ ├── profile/ # Profile pages
│ │ │ ├── view.html
│ │ │ ├── edit.html
│ │ │ └── change_password.html
│ │ ├── admin/ # Admin pages
│ │ └── extra/ # Error & legal pages
│ │ │ ├── 404.html
│ │ │ ├── 500.html
│ │ │ ├── privacy.html
│ │ │ └── terms.html
│ │
│ └── static/ # Static assets
│ ├── css/
│ ├── js/
│ └── images/
│
├── migrations/ # Database migrations (Alembic)
├── .env # Environment variables (dev)
├── .env.production # Environment variables (prod)
├── .dockerignore
├── .gitignore
├── deploy.sh # Deployment script
├── docker-compose.yml # Docker services
├── Dockerfile # Multi-stage Docker build
├── entrypoint.sh # Container startup script
├── Jenkinsfile # CI/CD pipeline
├── requirements.txt # Python dependencies
└── run.py # Application entry point
```
---

## 📋 Prerequisites

### For Docker Deployment (Recommended)
- [Docker](https://docs.docker.com/get-docker/) (v20+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2+)
- Git

### For Manual Setup
- Python 3.11+
- PostgreSQL 15+
- Git
- pip (Python package manager)

### For CI/CD Pipeline
- Jenkins (with Docker)
- SonarQube Server
- Trivy (installed on Jenkins server)
- OWASP Dependency-Check (Jenkins plugin)

---

## 🚀 Getting Started

### Option 1: Docker Deployment (Recommended)

**Step 1: Clone the repository**

```bash
git clone https://github.com/mananurrehman/quickstay.git
cd quickstay
```

**Step 2: Create environment file**
```
cp .env.example .env.production
```
Edit .env.production with your values:
```
# Flask
SECRET_KEY=your-super-secret-key-change-this
FLASK_ENV=production

# Database
DATABASE_URL=postgresql://quickstay_user:quickstay123@db:5432/quickstay

# Email (Gmail SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```
**Step 3: Create required directories**
```
sudo mkdir -p /home/ubuntu/quickstay-data/postgres
sudo mkdir -p /home/ubuntu/quickstay-data/uploads
```
**Step 4: Build and run**
```
docker compose up -d --build
```
**Step 5: Verify**
```
# Check containers are running
docker compose ps

# Check logs
docker compose logs -f web
```
**Step 6: Access the application**
```
http://localhost:5000
```

### Option 2: Manual Setup
**Step 1: Clone the repository**
```
git clone https://github.com/mananurrehman/quickstay.git
cd quickstay
```
**Step 2: Create Virtual Environment**
```
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```
**Step 3: Install dependencies**
```
pip install -r requirements.txt
```
**Step 4: Create environment file**
```
cp .env.example .env
```
Edit .env with your values:
```
# Flask
SECRET_KEY=your-secret-key
FLASK_ENV=development
FLASK_DEBUG=True

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/quickstay

# Email (Gmail SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```
**Step 5: Setup PostgreSQL database**
```
# Login to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE quickstay;
CREATE USER quickstay_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE quickstay TO quickstay_user;
\q
```
**Step 6: Run database migrations**
```
# Initialize migrations (first time only)
flask db init

# Generate migration files
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```
**Step 7: Run the application**
```
python run.py
```
**Step 8: Access the application**
```
http://localhost:5000
```
## 🔐 Environment Variables

| Variable | Description | Required | Default |
|---|---|---|---|
| SECRET_KEY | Flask secret key for sessions | ✅ | None |
| FLASK_ENV | Environment (development/production) | ✅ | development |
| FLASK_DEBUG | Debug mode (True/False) | ❌ | False |
| DATABASE_URL | PostgreSQL connection string | ✅ | None |
| MAIL_SERVER | SMTP server address | ✅ | smtp.gmail.com |
| MAIL_PORT | SMTP port | ✅ | 587 |
| MAIL_USE_TLS | Enable TLS | ✅ | True |
| MAIL_USERNAME | SMTP email address | ✅ | None |
| MAIL_PASSWORD | SMTP password/app password | ✅ | None |
| MAIL_DEFAULT_SENDER | Default sender email | ✅ | None |

### Gmail App Password Setup

1. Go to **Google Account Security**
2. Enable **2-Step Verification**
3. Go to **App Passwords**
4. Select app: **Mail**, device: **Other** (enter "QuickStay")
5. Copy the **16-character password**
6. Use this as **MAIL_PASSWORD** in your `.env`

## 🗄️ Database Setup
### Models Overview

#### Database Schema

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Users   │────→│ Bookings │←────│  Rooms   │
│          │     │          │     │          │
│ id       │     │ id       │     │ id       │
│ username │     │ user_id  │     │ name     │
│ email    │     │ room_id  │     │ type     │
│ password │     │ check_in │     │ price    │
│ role     │     │ check_out│     │ status   │
└──────────┘     └──────────┘     └──────────┘
      │                                 │
      │          ┌──────────┐           │
      └─────────→│ Reviews  │←──────────┘
                 │          │
                 │ id       │
                 │ user_id  │
                 │ room_id  │
                 │ rating   │
                 │ comment  │
                 └──────────┘
```

#### Migration Commands
```
# Generate new migration after model changes
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback last migration
flask db downgrade

# View migration history
flask db history
```
## 🔄 CI/CD Pipeline
#### Pipeline Architecture
```
GitHub Push
    ↓
Jenkins (Poll SCM - every 5 mins)
    ↓
┌─────────────────────────────────────┐
│  Stage 1: Clone Repository         │
│  Stage 2: SonarQube Analysis       │
│  Stage 3: Trivy Security Scan      │
│  Stage 4: OWASP Dependency Check   │
│  Stage 5: Deploy to Staging        │
│  Stage 6: Verify Deployment        │
└─────────────────────────────────────┘
    ↓
✅ App Live on Staging Server
```
#### Jenkins Setup Requirements

| Tool | Purpose |
|---|---|
| SSH Agent Plugin | SSH into staging server |
| SonarQube Scanner | Code quality analysis |
| OWASP Dependency-Check | Vulnerability scanning |
| GitHub Integration | Repository integration |

#### Jenkins Credentials Needed

| Credential ID | Type | Purpose |
|---|---|---|
| oracle-vm-ssh-testuser | SSH Key | Access to staging server |
| SonarQube Token | Secret Text | SonarQube authentication |

#### Pipeline Trigger
The pipeline uses Poll SCM to check for new commits:
```
Schedule: H/5 * * * *  (every 5 minutes)
```
## 🚢 Deployment
#### Docker Deployment Flow
```
docker compose up -d --build
         ↓
┌─────────────────────────────┐
│  PostgreSQL Container       │
│  - Health check passes      │
│  - Database ready           │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  Flask App Container        │
│  1. Wait for database       │
│  2. Run migrations          │
│  3. Start Flask server      │
└─────────────────────────────┘
         ↓
   App live on port 5000
```
#### Useful Docker Commands
```
# Start all services
docker compose up -d --build

# Stop all services
docker compose down

# View running containers
docker compose ps

# View logs (live)
docker compose logs -f web

# View database logs
docker compose logs -f db

# Restart app only
docker compose restart web

# Rebuild app only
docker compose up -d --build web

# Enter app container
docker exec -it quickstay-web bash

# Enter database container
docker exec -it quickstay-db psql -U quickstay_user -d quickstay
```
#### Production Checklist
```
☐ Set strong SECRET_KEY (use: python -c "import secrets; print(secrets.token_hex(32))")
☐ Set FLASK_ENV=production
☐ Set FLASK_DEBUG=False
☐ Configure real SMTP credentials
☐ Use strong database password
☐ Create data directories for volumes
☐ Setup firewall (allow only ports 5000, 22)
☐ Configure SSL/HTTPS (recommended)
☐ Setup regular database backups
```
## 📸 Screenshots

#### Home
![Home Screenshot](app/static/images/Home.png)

#### Rooms 
![Rooms](app/static/images/Rooms.png)

#### About
![About](app/static/images/About.png)

#### Contact
![Contact](app/static/images/Contact.png)

#### FAQ
![FAQ](app/static/images/FAQ.png)

#### Login
![Login](app/static/images/Login.png)

#### Register
![Register](app/static/images/Register.png)

#### Forgot-Password
![Forgot-Password](app/static/images/Forgot-Password.png)



## 🤝 Contributing
1. Fork the repository
2. Create your feature branch
```
git checkout -b feature/amazing-feature
```
3. Commit your changes
```
git commit -m "Add amazing feature"
```
4. Push to the branch
```
git push origin feature/amazing-feature
```
5. Open a Pull Request 

## Development Guidelines

- Follow MVC architecture with Flask Blueprints
- Use Tailwind CSS for styling (match existing design patterns)
- Support dark mode in all templates
- Add CSRF protection on all forms
- Write responsive templates (mobile-first)
- Use Lucide icons consistently

## 📄 Author/Developer
#### Manan ur Rehman
- GitHub: [@mananurrehman](https://github.com/mananurrehman)
- LinkedIn: [@mananurrehman](https://www.linkedin.com/in/mananurrehman/)