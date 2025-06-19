# Agricon Nigeria Django Backend API

## Project Overview

**Agricon Nigeria – A Shared Agricultural Infrastructure Platform**

Agricon Nigeria is a mobile-first/web platform that connects farmers to shared agricultural infrastructure such as dryers, cold rooms, and processing plants. By leveraging AI, IoT, and USSD technology, it enables affordable access through cooperative bookings, real-time availability tracking, and market linkages, helping reduce post-harvest losses and boost profitability.

**Why It Matters:** Nigerian farmers, especially smallholders, experience up to 40% post-harvest losses due to lack of access to preservation and processing infrastructure. High operational costs, unreliable electricity, and fragmented value chains contribute to these losses. Agricon addresses these challenges by offering shared, technology-driven solutions.

---

## Live Link

[<u>API Live Demo</u>](https://agricon-django-backend.onrender.com/).

## Documentation Link

Postman API Documentation [<u>here</u>](https://documenter.getpostman.com/view/45352371/2sB2x8GBwe#50a1921c-8553-462b-97ba-e2ed07c5bc37).

---

## Tech Stack

- **Language:** Python 3.12
- **Framework:** Django 5.2.3
- **Auth:** djangorestframework\_simplejwt==5.5.0
- **Environment Config:** django-environ==0.12.0
- **Database:** PostgreSQL

---

## Installation Instructions

### Prerequisites

- Python >= 3.9
- pip
- Git
- Virtual environment tool (e.g. `venv`)
- PostgreSQL

### Setup Locally

1. **Clone the repository**

```bash
git clone https://github.com/InternPulse/agricon-django-backend.git
cd agricon-django-backend
```

2. **Create a virtual environment and activate it**

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Add a `.env` file**


```env
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

5. **Run migrations**

```bash
python manage.py migrate
```

6. **Create superuser**

```bash
python manage.py createsuperuser
```

7. **Start the development server**

```bash
python manage.py runserver
```

API will be available at `http://127.0.0.1:8000/`

---

## Features Implemented

- User Registration & Login
- JWT Authentication (Access & Refresh Tokens)
- User Logout
- Email Verification
- Password Reset and Update
- Farmer Profile Management (CRUD)
- Operator Profile Management (CRUD)

---

## API Endpoints

**Base URL:** `/api/v1/`

| Endpoint                       | Method | Description                        |
| ------------------------------ | ------ | ---------------------------------- |
| `auth/register/`               | POST   | Register a new user                |
| `auth/verify-email-otp/`       | POST   | Verify email by sending OTP        |
| `auth/otp/resend/`             | POST   | Resend OTP for verification        |
| `auth/login/`                  | POST   | Login and obtain JWT tokens        |
| `auth/profile/farmer/`         | POST   | Register a farmer profile          |
| `auth/profile/operator/`       | POST   | Register an operator profile       |
| `auth/profile/farmer/`         | GET    | Get farmer profile                 |
| `auth/profile/operator/`       | GET    | Get operator profile               |
| `auth/profile/farmer/`         | PUT    | Full update of farmer profile      |
| `auth/profile/operator/`       | PUT    | Full update of operator profile    |
| `auth/profile/farmer/`         | PATCH  | Partial update of farmer profile   |
| `auth/profile/operator/`       | PATCH  | Partial update of operator profile |
| `auth/password-reset/request/` | POST   | Reset a new password for user      |
| `auth/password-reset/confirm/` | POST   | Confirm new password for user      |
| `auth/logout/`                 | POST   | Logout and blacklist token         |

---

## Project Structure

```plaintext
agricon-backend/
├── manage.py
├── agricon_django/
│   ├── asgi.py
│   ├── manage.py
│   ├── urls.py
│   └── settings/
├── users/
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
...
```

---

## Contribution Guidelines

1. Clone the repository:

```bash
git clone https://github.com/InternPulse/agricon-django-backend.git
```

2. Checkout the dev branch:

```bash
git checkout dev
```

3. Create a new branch:

```bash
git checkout -b FT-001/feat-user-authentication
```

4. Make your changes, commit and push:

```bash
git add .
git commit -m "feat: implement user authentication"
git push -u origin FT-001/feat-user-authentication
```

5. Open a Pull Request to merge into `dev`

---

## Commit Message Format

| Type     | Description                       |
| -------- | --------------------------------- |
| feat     | A new feature                     |
| fix      | A bug fix                         |
| docs     | Documentation changes             |
| style    | Code formatting, no logic changes |
| refactor | Refactor code                     |
| test     | Add or update tests               |
| chore    | Maintenance tasks                 |

**Examples:**

- `feat: add profile registration endpoints`
- `fix: correct token refresh logic`

---

## License

This project is licensed under the MIT License.

