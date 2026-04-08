# Event-Driven Notification System

> A scalable backend notification system that fires a real-time email to users on every login — built on an event-driven, producer-consumer architecture using FastAPI, RabbitMQ, and SendGrid.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-async-009688?style=flat-square&logo=fastapi&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-message_queue-FF6600?style=flat-square&logo=rabbitmq&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-database-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![SendGrid](https://img.shields.io/badge/SendGrid-email-1A82E2?style=flat-square&logo=twilio&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-containerized-2496ED?style=flat-square&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI/CD-GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-22C55E?style=flat-square)

---

## Table of Contents

- [Overview](#-overview)
- [Key Engineering Highlights](#-key-engineering-highlights)
- [How It Works](#-how-it-works)
- [System Architecture](#-system-architecture)
- [Features](#-features)
- [API Reference](#-api-reference)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Docker Setup](#-docker-setup)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Design Decisions](#-design-decisions)
- [Known Limitations & Future Improvements](#-known-limitations--future-improvements)
- [License](#-license)



<img width="1465" height="836" alt="Screenshot 2026-02-24 at 13 43 16" src="https://github.com/user-attachments/assets/a14251be-bd71-429a-a882-a3dd1bb743bc" />

<img width="1467" height="819" alt="Screenshot 2026-02-24 at 13 43 32" src="https://github.com/user-attachments/assets/bcdfb155-ff25-428d-af54-6e689dc6ce7c" />

<img width="1468" height="835" alt="Screenshot 2026-02-24 at 13 44 07" src="https://github.com/user-attachments/assets/0975d308-79e5-4d74-92ec-a2fbf6d1ad60" />

<img width="1469" height="836" alt="Screenshot 2026-02-24 at 13 44 15" src="https://github.com/user-attachments/assets/b9fbdab9-7700-4068-9595-128d75e09bff" />

<img width="1230" height="696" alt="Screenshot 2026-02-24 at 13 44 59" src="https://github.com/user-attachments/assets/445ff790-6beb-4a92-8f41-6bc468ba6fa5" />

a<img width="1468" height="832" alt="Screenshot 2026-02-24 at 13 46 09" src="https://github.com/user-attachments/assets/3626c91d-2569-4ffb-99a1-f3411e2713c1" />


---

## Overview

The **Event-Driven Notification System** is a production-style backend service that demonstrates how modern distributed systems handle asynchronous event processing. Every time a user logs in, the system:

1. Authenticates the user via OAuth2
2. Publishes a login event to a **RabbitMQ message queue**
3. A background worker **consumes** the event from the queue
4. Sends a **login notification email** via SendGrid

This decoupled architecture ensures the login response is never delayed by email delivery — the API responds instantly while the notification pipeline runs independently in the background.

Built to showcase:
- **Event-driven / producer-consumer architecture**
- **Async background processing** with RabbitMQ
- **Reliable message delivery** with durability and acknowledgements
- **OAuth2 authentication** with session management
- **Containerized deployment** with Docker and CI/CD

---

## Key Engineering Highlights

### 1. Producer-Consumer Architecture with RabbitMQ
The login flow is split into two independent components: a **producer** (the FastAPI app) and a **consumer** (the background worker). When a user logs in, the API publishes a JSON message to a durable RabbitMQ queue — then returns immediately. The worker picks it up asynchronously.

```python
channel.basic_publish(
    exchange="",
    routing_key=QUEUE_NAME,
    body=json.dumps({"email": user["email"], "name": user["name"]}),
    properties=pika.BasicProperties(delivery_mode=2)  # Persistent message
)
```

### 2. Durable Queues & Message Persistence
Both the queue and messages are marked **durable/persistent**. This means if RabbitMQ restarts, unprocessed messages are not lost — they survive and are redelivered to the worker.

```python
channel.queue_declare(queue=QUEUE_NAME, durable=True)
# delivery_mode=2 → message persists to disk
```

### 3. Background Worker with Auto-Reconnect
The RabbitMQ consumer runs in a **daemon thread** launched at app startup. It includes a retry loop — if RabbitMQ is temporarily unavailable (e.g., during container startup), the worker keeps retrying every 5 seconds until the connection succeeds.

```python
def start_worker():
    while True:
        try:
            connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            time.sleep(5)  # Retry until RabbitMQ is ready
```

### 4. Manual Message Acknowledgement
The worker uses **manual ACK** (`basic_ack`) — a message is only removed from the queue after the email is successfully sent. If the worker crashes mid-processing, RabbitMQ re-queues the message for redelivery.

```python
def callback(ch, method, properties, body):
    send_email(email, name)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Only ACK after success
```

### 5. OAuth2 Session-Based Authentication
User sessions are managed server-side via **Starlette's SessionMiddleware**, with a protected dependency injected into any route that requires authentication.

```python
def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
```

### 6. Database Migrations with Alembic
Schema changes are managed through **Alembic** migrations — not raw SQL. This keeps the database schema version-controlled and reproducible across environments.

---

## How It Works
```
User Logs In
│
▼
FastAPI validates session (OAuth2)
│
▼
Publishes event → RabbitMQ Queue ("email_queue")
│                        │
│                        ▼
│              Background Worker (daemon thread)
│                        │
▼                        ▼
API responds instantly    Sends email via SendGrid
(user is NOT waiting)     ACKs message from queue
```


**Step-by-step:**
1. User hits `/` and authenticates via OAuth2
2. On successful login, the app publishes `{ "email": "...", "name": "..." }` to `email_queue`
3. The worker thread (started at app startup) is listening on the queue
4. Worker receives the message, calls SendGrid to send the notification email
5. On success, the worker ACKs the message — removing it from the queue
6. On failure, the message remains in the queue and is redelivered

---

## System Architecture
```
┌─────────────────────────────────────────────────────────┐
│                      Browser / Client                   │
│              HTML Templates (Jinja2 + JS)               │
└────────────────────┬────────────────────────────────────┘
│  HTTP
┌────────────────────▼────────────────────────────────────┐
│                   FastAPI Application                    │
│                                                         │
│   GET  /              →  Login Page (HTML)              │
│   GET  /dashboard     →  Dashboard (auth required)      │
│   GET  /logout        →  Clear session, redirect        │
│   POST /test-email    →  Manually publish to queue      │
│                                                         │
│   OAuth2 Router       →  Handles login/callback         │
└──────────┬──────────────────────┬───────────────────────┘
│                      │ publish message
┌──────────▼──────┐    ┌──────────▼──────────────────────┐
│   PostgreSQL     │    │        RabbitMQ                  │
│                  │    │     Queue: email_queue           │
│  - users table   │    │     durable=True                │
│  (Alembic mgmt)  │    └──────────┬──────────────────────┘
└──────────────────┘               │ consume message
┌──────────▼──────────────────────┐
│    Background Worker Thread      │
│   (started on app startup)       │
│   retry loop on disconnect       │
└──────────┬──────────────────────┘
│ send email
┌──────────▼──────────────────────┐
│          SendGrid API            │
│   Login Notification Email       │
└─────────────────────────────────┘
```

---

## Features

- **OAuth2 Login** — Secure user authentication with session management
- **Event Publishing** — Login events pushed to RabbitMQ immediately after auth
- **Background Worker** — Daemon thread consumes events independently of the API
- **Email Notifications** — Login alert emails sent via SendGrid on every login
- **Message Durability** — Persistent queues and messages survive restarts
- **Auto-Reconnect** — Worker retries connection if RabbitMQ is temporarily down
- **Manual ACK** — Messages only removed from queue after confirmed email delivery
- **Database Migrations** — Schema versioned and managed via Alembic
- **Containerized** — Full stack runs with a single `docker-compose up`
- **CI/CD** — Automated test and deploy pipeline via GitHub Actions
- **Test Endpoint** — `/test-email` allows manual triggering of the notification pipeline

---

## API Reference

Interactive docs available at `/docs` when running locally.

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Login page (HTML) |
| `GET` | `/dashboard` | User dashboard — requires active session |
| `GET` | `/logout` | Clears session, redirects to login |

> OAuth2 login/callback routes are handled by the `oauth2` router (`app/auth/oauth2.py`).

---

### Notifications

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `POST` | `/test-email` | ✅ Yes | Manually publish a login event to the email queue |

**POST `/test-email` — Response:**
```json
{
  "message": "Email event published to queue ✅"
}
```

This endpoint publishes the authenticated user's email and name directly to RabbitMQ, triggering the worker to send a notification. Useful for testing the pipeline end-to-end without a full login flow.

**Error response:**
```json
{
  "error": "ConnectionClosed: ..."
}
```

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Backend | Python + FastAPI | Async-first, lightweight, auto OpenAPI docs |
| Message Queue | RabbitMQ + pika | Reliable async event delivery, durable queues |
| Email | SendGrid | Transactional email API, high deliverability |
| Database | PostgreSQL | Production-grade relational storage |
| Migrations | Alembic | Version-controlled schema management |
| Auth | OAuth2 + SessionMiddleware | Secure login with server-side session |
| Templates | Jinja2 | Server-side HTML rendering |
| Containers | Docker + Docker Compose | Full stack in one command |
| CI/CD | GitHub Actions | Automated test and deployment pipeline |

---

## 📁 Project Structure
```
Event-Driven-Notification-System/
│
├── app/
│   ├── main.py                      # FastAPI app, routes, worker startup
│   ├── config.py                    # Environment config (RabbitMQ URL, secrets)
│   ├── database.py                  # SQLAlchemy engine and session
│   ├── models.py                    # ORM models (User)
│   ├── schemas.py                   # Pydantic schemas
│   ├── auth/
│   │   └── oauth2.py                # OAuth2 login/callback router
│   └── services/
│       ├── rabbitmq.py              # Message queue producer logic
│       └── sendgrid_service.py      # Email sending via SendGrid API
│
├── frontend/
│   ├── static/                      # CSS, JS assets
│   └── templates/
│       ├── login.html               # Login page
│       └── Dashboard.html           # Post-login dashboard
│
├── alembic/                         # Database migration scripts
│   └── versions/
│
├── tests/
│   └── test_auth.py                 # Auth unit tests
│
├── Dockerfile
├── docker-compose.yml               # FastAPI + PostgreSQL + RabbitMQ
├── alembic.ini                      # Alembic config
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- Docker + Docker Compose (recommended)
- A [SendGrid](https://sendgrid.com) account with an API key
- A RabbitMQ instance (local or CloudAMQP)

### Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/notificationdb
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=you@yourdomain.com
SESSION_SECRET_KEY=your_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### Local Setup (without Docker)

```bash
# 1. Clone the repo
git clone https://github.com/jaayysoni/Event-Driven-Notification-System.git
cd Event-Driven-Notification-System

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
alembic upgrade head

# 5. Start the server
uvicorn app.main:app --reload
```

Visit **http://localhost:8000**

> RabbitMQ and PostgreSQL must be running before starting the server.

---

## Docker Setup

Run the entire stack — FastAPI, PostgreSQL, and RabbitMQ — with one command:

```bash
docker-compose up --build
```

Docker Compose handles service networking automatically. The worker inside the FastAPI container will connect to RabbitMQ and begin consuming messages once the queue is ready.

Visit **http://localhost:8000**

---

## CI/CD Pipeline

The project uses **GitHub Actions** for automated testing and deployment:

- On every push to `main`, the pipeline runs the test suite (`tests/test_auth.py`)
- On passing tests, the workflow deploys the updated containers to the target environment
- Pipeline config lives in `.github/workflows/`

---

## Design Decisions

**Why RabbitMQ over a simple async task (e.g., `asyncio.create_task`)?**
A bare async task lives in-process — if the server restarts or crashes, the email is lost. RabbitMQ gives durability: messages survive restarts and are redelivered if processing fails. This is the fundamental difference between a notification system and a real notification *infrastructure*.

**Why a daemon thread for the worker instead of Celery?**
Celery adds significant operational complexity (separate worker process, beat scheduler, result backend). For a single-queue, single-task consumer, a daemon thread with `pika.BlockingConnection` is simpler, more transparent, and sufficient. Celery would be the right upgrade path for multi-queue, multi-worker scaling.

**Why manual ACK instead of auto-ACK?**
Auto-ACK removes the message from the queue the moment it's delivered — before the email is sent. If the worker crashes mid-send, the message is silently lost. Manual ACK guarantees at-least-once delivery: the message stays in the queue until `basic_ack` is called after confirmed success.

**Why OAuth2 + SessionMiddleware over JWT?**
For a server-rendered HTML app with Jinja2 templates, session cookies are the natural fit. JWTs are better suited for stateless REST APIs consumed by frontend frameworks. The session approach here is intentional and appropriate for the architecture.

**Why Alembic over raw SQL or `create_all`?**
`Base.metadata.create_all()` is fine for prototypes but doesn't support schema evolution (adding columns, renaming tables). Alembic gives version-controlled, reversible migrations — the same approach used in production engineering teams.

---

## Known Limitations & Future Improvements

| Limitation | Planned Fix |
|---|---|
| Single worker thread (no horizontal scaling) | Move to Celery with multiple workers |
| No retry count / dead-letter queue | Add DLQ for failed messages after N retries |
| Worker runs in same process as API | Extract to a standalone worker service |
| No email templates | Add HTML email templates via Jinja2 |
| OAuth2 only (Google) | Add username/password auth as fallback |
| No test coverage for queue/email layer | Add integration tests with mocked RabbitMQ and SendGrid |
| `https_only=False` in SessionMiddleware | Set to `True` and enforce HTTPS in production |

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

**Jay Soni** — [GitHub](https://github.com/jaayysoni) | Open to backend, platform, and distributed systems engineering roles.
