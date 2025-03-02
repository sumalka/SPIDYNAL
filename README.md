# SPIDY LENS™ SYSTEM

SPIDY LENS™ SYSTEM is an advanced desktop application developed using **Java Swing (JPanel)** with **MS SQL Database** for **City Nursing Home**. This system manages patient records, appointments, doctor information, and hospital staff management.

## Features
- Patient Registration & Management
- Doctor Management
- Appointments Scheduling
- Bill Generation
- User Authentication
- Dashboard with Overview Statistics
- Search & Filter Records

## Technologies Used
- Java (NetBeans IDE)
- Swing (JPanel for GUI)
- MS SQL Database
- JDBC Connectivity

## Setup Instructions
1. Clone this repository:
```bash
https://github.com/SPIDYBROZ/spidy-lens-system.git
```

2. Import the project into **NetBeans IDE**.

3. Configure Database:
   - Install MS SQL Server.
   - Create a database named `spidy_lens_db`.
   - Import the `spidy_lens_db.sql` file into the database.

4. Update Database Credentials in `DBConnection.java`:
```java
String url = "jdbc:sqlserver://localhost:1433;databaseName=spidy_lens_db";
String username = "your_username";
String password = "your_password";
```

5. Build & Run the Project.

## Screenshots
| Feature | Screenshot |
|---------|------------|
| Login Page | ![Login](screenshots/login.png) |
| Dashboard | ![Dashboard](screenshots/dashboard.png) |
| Patient Management | ![Patient](screenshots/patient.png) |

## Developer
**SPIDY BROZ™** 🚀

### Contact Us
- Instagram: [@spidy_broz](https://www.instagram.com/spidy_broz)
- YouTube: [SPIDY BROZ](https://www.youtube.com/@SPIDYBROZ)
- Email: spidybrozofficial@gmail.com

---
🕸️ _"SPIDY LENS™ SYSTEM - Vision Beyond Limits"_
