# Task Management Application

A Flask-based task management system with user authentication, task assignment, and a separate RESTful API service.

## Technical Stack

*   **Backend**: Python 3.11, Flask
*   **Database**: SQLite (SQLAlchemy ORM)
*   **Authentication**: Flask-Login (Session)
*   **Frontend**: Jinja2 Templates, Skeleton CSS (Dark Theme)

## Database Schema

### User Table
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key | Unique user identifier |
| `username` | String(150) | Unique, Not Null | User's login name |
| `email` | String(150) | Unique, Not Null | User's email address |
| `password_hash` | String(150) | Not Null | Hashed password |

### Task Table
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key | Unique task identifier |
| `title` | String(100) | Not Null | Task title |
| `description` | Text | Nullable | Task details |
| `date_posted` | DateTime | Not Null, Default=UTC | Creation timestamp |
| `due_date` | DateTime | Nullable | Task deadline |
| `priority` | String(20) | Not Null, Default='Medium' | Low, Medium, High |
| `status` | String(20) | Not Null, Default='To-Do' | To-Do, In Progress, Done, Cancelled |
| `user_id` | Integer | ForeignKey('user.id'), Not Null | Author of the task |
| `assigned_to_id` | Integer | ForeignKey('user.id'), Nullable | User assigned to the task |

## Setup and Installation

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run Main Application**:
    ```bash
    python app.py
    ```
    Access at `http://localhost:5000`.

3.  **Run API Service**:
    Open a separate terminal:
    ```bash
    python api.py
    ```
    Access at `http://localhost:5001`.

## API Documentation

**Base URL**: `http://localhost:5001/api`
**Authentication**: None (Public Access)

### Endpoints

| Method | Endpoint | Description | Payload/Params |
| :--- | :--- | :--- | :--- |
| `GET` | `/users` | List all users | None |
| `DELETE` | `/users/<id>` | Delete a user | None |
| `GET` | `/tasks` | List tasks | `status`, `priority`, `user_id` (Query Params) |
| `POST` | `/tasks` | Create task | JSON: `{title, user_id, description, ...}` |
| `GET` | `/tasks/<id>` | Get task details | None |
| `PUT` | `/tasks/<id>` | Update task | JSON: `{title, status, ...}` |
| `DELETE` | `/tasks/<id>` | Delete task | None |

## Testing

Run unit tests:
```bash
python -m unittest discover tests
```

## User Interface and application screenshots
### For App
<img width="1233" height="545" alt="image" src="https://github.com/user-attachments/assets/24211c94-4605-459d-a17f-7fb5cf0cbce0" />
<img width="1235" height="616" alt="image" src="https://github.com/user-attachments/assets/09675dfa-0099-4e90-9ef5-481ba74b8e42" />
<img width="1234" height="417" alt="image" src="https://github.com/user-attachments/assets/2644bbee-9803-4fcb-ba7e-06a02ec66dfe" />
<img width="1664" height="901" alt="image" src="https://github.com/user-attachments/assets/47e133ac-172a-4ae9-9311-ad55714b75b9" />
<img width="1736" height="892" alt="image" src="https://github.com/user-attachments/assets/5366e6c3-55c2-4c1c-8f04-cada3b0965e8" />
<img width="1239" height="535" alt="image" src="https://github.com/user-attachments/assets/068bf32d-905c-4a21-8528-765e420b1537" />

### For Rest APIs
<img width="1592" height="834" alt="image" src="https://github.com/user-attachments/assets/435372b7-63fd-4cd0-b066-b4e8102b8ac3" />
<img width="1597" height="835" alt="image" src="https://github.com/user-attachments/assets/67e23e15-a5c9-4b85-9a34-0daeb9360202" />
<img width="1593" height="673" alt="image" src="https://github.com/user-attachments/assets/faad8808-4d88-465a-9376-03e2ddea196d" />
<img width="1628" height="698" alt="image" src="https://github.com/user-attachments/assets/62a7049c-a5b1-44c6-976e-506fa6446f27" />

## Reference

*   [Flask Documentation](https://flask.palletsprojects.com/)
*   [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
*   [Flask-Login Documentation](https://flask-login.palletsprojects.com/)
*   [Werkzeug Documentation](https://werkzeug.palletsprojects.com/)
*   [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
*   [Unittest Documentation](https://docs.python.org/3/library/unittest.html)   
*   [Git Documentation](https://git-scm.com/doc)
*   [https://github.com/pavlo-myskov/flask-task-manager](https://github.com/pavlo-myskov/flask-task-manager)
*   [https://github.com/Nirupama15/flask-task-tracker](https://github.com/Nirupama15/flask-task-tracker)
*   [http://getskeleton.com/](http://getskeleton.com/) - For complete UI.
