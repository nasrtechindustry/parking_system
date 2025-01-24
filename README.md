# SMART PARKING MANAGEMENT SYSTEM

## 1. Introduction
Efficient parking management is essential in urban areas where space is limited, and the demand for parking is high. Traditional systems often rely on manual processes, which can lead to errors, inefficiencies, and frustration for both users and administrators. To address these challenges, the Parking Management System is designed as a modern, automated solution.

## 2. System Design and Architecture
The Parking Management System is structured into three primary components:

### Frontend
The GUI, developed using Tkinter, provides an intuitive interface for administrators and users. It features:
- Login screens
- Dashboards
- Modules for reservations, payment processing, and slot availability monitoring

### Backend
MySQL serves as the backend database, storing:
- User information
- Reservation data
- Payment records
- Parking slot statuses

The relational database model ensures data normalization and avoids redundancy.

## 3. Implementation Details

### 3.1. Technologies Used
- **Programming Language:** Python 3
- **Frontend Library:** Tkinter
- **Database Management System:** SQLite3 with SQLAlchemy
- **Tools and Frameworks:** XAMPP, Visual Studio Code, SQLite View

### 3.2. Key Features
- User authentication, allowing access only to operators or admins
- Vehicle and customer management
- Parking slot management
- Reservation management

## 4. How to Start

### 4.1. Clone the Project
```bash
    git clone https://github.com/nasrtechindustry/parking_system.git
```

### 4.2. Move to the Project Folder
```bash
    cd parking_system
```

### 4.3. Create a Virtual Environment
```bash
    python3 -m venv venv
```

### 4.4. Activate the Virtual Environment
#### On macOS and Linux:
```bash
    source venv/bin/activate
```

#### On Windows:
```bash
    venv\Scripts\activate
```

## 5. Developers
This project was completed by a group of four students:

1. **Nasr Hassan Mpalang’ombe** (30326/T.2023)  
   Email: [nasrkihagila@gmail.com](mailto:nasrkihagila@gmail.com)
2. **Nasma Mustafa Juma** (30895/T.2023)
3. **Nuru Mohamed Kisimikwe** (32226/T.2023)
4. **Mary Living Rogath** (31991/T.2023)

