# Event-Driven Notification System

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Swagger UI](https://img.shields.io/badge/Swagger_UI-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![SendGrid](https://img.shields.io/badge/SendGrid-1A82E2?style=for-the-badge&logo=sendgrid&logoColor=white)
![REST API](https://img.shields.io/badge/REST_API-02569B?style=for-the-badge)
![API](https://img.shields.io/badge/API-000000?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

## Project Overview

This project is a scalable backend notification system that sends an email every time a user logs in.

It is built using modern backend technologies and follows an event-driven architecture to ensure reliable and efficient message processing.

The system is fully containerized and deployed using Docker with CI/CD integration.

---

<img width="1465" height="836" alt="Screenshot 2026-02-24 at 13 43 16" src="https://github.com/user-attachments/assets/a14251be-bd71-429a-a882-a3dd1bb743bc" />

<img width="1467" height="819" alt="Screenshot 2026-02-24 at 13 43 32" src="https://github.com/user-attachments/assets/bcdfb155-ff25-428d-af54-6e689dc6ce7c" />

<img width="1468" height="835" alt="Screenshot 2026-02-24 at 13 44 07" src="https://github.com/user-attachments/assets/0975d308-79e5-4d74-92ec-a2fbf6d1ad60" />

<img width="1469" height="836" alt="Screenshot 2026-02-24 at 13 44 15" src="https://github.com/user-attachments/assets/b9fbdab9-7700-4068-9595-128d75e09bff" />

<img width="1230" height="696" alt="Screenshot 2026-02-24 at 13 44 59" src="https://github.com/user-attachments/assets/445ff790-6beb-4a92-8f41-6bc468ba6fa5" />

a<img width="1468" height="832" alt="Screenshot 2026-02-24 at 13 46 09" src="https://github.com/user-attachments/assets/3626c91d-2569-4ffb-99a1-f3411e2713c1" />



## What This System Does

- Allows users to log in securely
- Triggers an event after successful login
- Processes the event in the background
- Sends a login notification email using SendGrid
- Ensures reliable message delivery using RabbitMQ
- Stores user data in PostgreSQL

---

## How It Works (Simple Flow)

1. User logs in
2. The system creates a notification event
3. The event is sent to a message queue
4. A background worker processes the event
5. An email is sent to the user

This design ensures fast response times and reliable processing.

---

## Technologies Used

- FastAPI (Backend Framework)
- RabbitMQ (Message Queue)
- PostgreSQL (Database)
- SendGrid (Email Service)
- Docker (Containerization)
- GitHub Actions (CI/CD)

---

## Key Highlights

- Event-driven architecture
- Asynchronous background processing
- Reliable message delivery
- Email notifications on every login
- Dockerized for easy deployment
- CI/CD pipeline configured
- Cloud deployment ready

---

## Deployment

The application is containerized using Docker and can be deployed easily on cloud platforms such as AWS.

---

## Why This Project Matters

This project demonstrates:

- Backend system design
- Message queue integration
- Email service integration
- Database management
- Containerized deployment
- CI/CD implementation

It reflects practical, production-ready backend development skills.

---

# Project Structure

```
Event-Driven-Notification-System/
│
├── app/                          # Main application package
│   ├── auth/                     # Authentication logic
│   │   └── oauth2.py
│   │
│   ├── services/                 # External service integrations
│   │   ├── rabbitmq.py           # Message queue producer
│   │   └── sendgrid_service.py   # Email sending logic
│   │
│   ├── config.py                 # Application configuration
│   ├── database.py               # Database connection setup
│   ├── models.py                 # Database models
│   ├── schemas.py                # Pydantic schemas
│   └── main.py                   # Application entry point
│
├── frontend/                     # UI templates & static files
│   ├── static/
│   └── templates/
│       ├── login.html
│       └── Dashboard.html
│
├── alembic/                      # Database migrations
│   └── versions/
│
├── tests/                        # Unit tests
│   └── test_auth.py
│
├── Dockerfile                    # Docker image configuration
├── docker-compose.yml            # Multi-container setup
├── alembic.ini                   # Alembic configuration
├── requirements.txt              # Project dependencies
└── README.md                     # Project documentation

```
---

## License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this software in accordance with the license terms.

See the `LICENSE` file for full details.

