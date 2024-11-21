# Student Enrollment System

## Overview

The Student Enrollment System is a web application that allows users to register for degree programs and manage their enrollments. The application uses a cloud database (AWS RDS) for data storage and features role-based access control, enabling admin users to manage degrees and enrollments while restricting regular users to enrollment functionalities only.

## Features

- **User Registration and Authentication**: Users can register, log in, and log out securely.
- **Role-Based Access Control**:
  - **Admin Users**: Manage degree programs (create, update, delete).
  - **Regular Users**: View and enroll in available degrees.
- **Cloud Database Integration**: Stores user and degree data in AWS RDS (MySQL).
- **Responsive Design**: Adapts to different screen sizes, including desktops and mobile devices.
- **Secure Configuration**: Uses environment variables to protect sensitive information.
- **Error handling**: Uses parametrized SQL queries and database checks to prevent unauthorized manipulation of the database.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: AWS RDS (MySQL)
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy
- **Deployment**: Local Flask development server

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/camerongardner/Cloud-Databases.git
   cd student-enrollment-system
   ```

2. **Set Up the Virtual Environment**
   Create and activate a Python virtual environment:

   ```bash
   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate

   # On Windows:
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the project root with the following content:
   ```
   # Flask Configuration
   SECRET_KEY=your_secure_secret_key_here

   # AWS RDS Configuration
   DB_USERNAME=admin
   DB_PASSWORD=your_database_password
   DB_HOST=your_database_endpoint
   DB_NAME=student_enrollment
   DB_PORT=3306
   ```

5. **Initialize the Database**
   Run the provided script to create and populate the database:
   ```bash
   python init_db.py
   ```

6. **Run the Application**
   Start the Flask development server:
   ```bash
   python app.py
   ```
   Access the application at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Application Structure

```
student-enrollment-system/
├── app.py               # Main application file
├── config.py            # Configuration for the app
├── init_db.py           # Script to initialize the database
├── models.py            # SQLAlchemy models
├── routes.py            # Application routes
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── admin_dashboard.html # Admin dashboard
│   ├── my_enrollments.html  # User enrollment page
│   └── create_degree.html   # Degree creation form
├── static/              # Static files (CSS)
│   ├── styles.css       # Custom styles
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Database Schema

### User Table
| Column Name    | Type    | Description          |
|----------------|---------|----------------------|
| id             | Integer | Primary Key          |
| username       | String  | Unique, required     |
| email          | String  | Unique, required     |
| password_hash  | String  | Hashed password      |
| is_admin       | Boolean | Admin role flag      |

### Degree Table
| Column Name    | Type    | Description               |
|----------------|---------|---------------------------|
| id             | Integer | Primary Key               |
| degree_name    | String  | Unique, required          |
| description    | Text    | Description of the degree |
| duration       | String  | Length of the degree      |

### Enrollment Table
| Column Name    | Type    | Description                 |
|----------------|---------|-----------------------------|
| id             | Integer | Primary Key                 |
| user_id        | Integer | Foreign Key (User)          |
| degree_id      | Integer | Foreign Key (Degree)        |
| enrolled_on    | DateTime| Timestamp of enrollment     |

## Usage

### Regular Users
- Register or log in.
- View available degrees.
- Enroll in a degree.
- View their enrollments on the "My Enrollments" page.

### Admin Users
- Log in with admin credentials.
- Access the Admin Dashboard to manage degrees.
- Create, update, or delete degree programs.
- Have all permissions that a user has.

## Stretch Challenges Implemented

- **Responsive Design**: Pages scale beautifully on mobile and desktop.
- **Role-Based Access Control**: Admin and user roles have been established to prevent unauthorized access to the database.

## Possible Improvements

- Deploy the application to a cloud server.
- Allow users to unenroll from a degree.
- Configure notifications to users based on when the degree is to start and other information.
- Implement error handling so the application does not crash if a user tries to register an account with an email that has already been used.

## Demonstration Video

You can watch a walkthrough of the application on YouTube: [Student Enrollment System Walkthrough](https://www.youtube.com/watch?v=q-s0SMba91U)

## Contributing

Contributions are welcome! Fork the repository and create a pull request for any feature additions or bug fixes.
