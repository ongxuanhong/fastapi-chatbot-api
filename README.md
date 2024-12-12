# Gamified Chat Application

## Table of Contents
1. [Component Diagram](#component-diagram)
2. [Sequence Diagram](#sequence-diagram)
3. [Entity-Relationship Diagram (ERD)](#entity-relationship-diagram-erd)
4. [Deployment Diagram](#deployment-diagram)

---

## Component Diagram

### Description
The component diagram showcases the overall structure of the gamified chat application. It highlights the main components:
- **Streamlit UI**: The frontend user interface where users interact with the system.
- **FastAPI Backend**: The backend responsible for handling API requests, business logic, and database interactions.
- **Database**: The persistent storage for user data and pot information.

### Key Features
- Authentication Service for registration and login.
- Currency Management for tracking user balances and deducting currency.
- Messaging Service for dynamic pricing and randomized win logic.
- Pot Management for handling contributions and resets.

### Diagram
![Component Diagram](diagrams/figures/1.components.png)

---

## Sequence Diagram

### Description
The sequence diagram describes the flow of events when a user sends a message. It visualizes interactions between the user, the Streamlit UI, the FastAPI backend, and the database.

### Key Features
- The user initiates the action by clicking "Send Message."
- The backend processes the message, updates the database, and determines whether the user wins the pot.
- The result is returned to the user via the UI.

### Diagram
![Sequence Diagram](diagrams/figures/2.sequence.png)

---

## Entity-Relationship Diagram (ERD)

### Description
The ERD provides a detailed view of the database schema. It defines the relationships between tables:
- **Users Table**: Stores user information, such as `id`, `username`, `balance`, and `message_count`.
- **Pot Table**: Tracks the current amount in the centralized pot.

### Key Features
- The `users` table is related to the `pot` table via contributions.
- Supports operations like balance deduction, pot contributions, and pot resets.

### Diagram
![Entity-Relationship Diagram](diagrams/figures/3.erd.png)

---

## Deployment Diagram

### Description
The deployment diagram illustrates the setup of the application in a real-world environment. It shows how the frontend, backend, and database components are deployed and interact.

### Key Features
- The **Streamlit UI** runs on the user’s device and communicates with the backend.
- The **FastAPI Backend** is hosted on a server, handling all API requests and connecting to the database.
- The **Database** is a centralized data store accessible by the backend.

### Diagram
![Deployment Diagram](diagrams/figures/4.deployment.png)

---

## How to run
```bash
pip install -r requirements.txt
uvicorn uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Deployed Railway: https://web-production-65db.up.railway.app/docs

## How to test
```bash
pytest tests/
```

## How to migration
```bash
alembic init alembic
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## How to generate diagram
1. Install [PlantUML](https://plantuml.com/) locally or use an online PlantUML renderer.
2. Save each `.puml` file provided in the `diagrams` directory.
3. Generate the diagrams:
   - **Command-line**:
     ```bash
     java -jar plantuml-1.2024.8.jar filename.puml
     ```
   - **Online Tool**: Copy and paste the code into [PlantUML Online Editor](http://www.plantuml.com/plantuml/uml/).