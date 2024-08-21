# Task Management System

## Overview

The Task Management System is a powerful web application built with Django, designed to streamline task management, assignment, and tracking. This system is ideal for teams looking to enhance their productivity and organization by offering a feature-rich, user-friendly interface.

## Features

- **Task Management:** Easily create, update, and manage tasks with detailed descriptions and status tracking.
- **User Assignment:** Assign tasks to specific users and monitor their progress through the dashboard.
- **Status Updates:** Track task status with predefined categories such as Open, In Progress, and Completed.
- **Deadline Tracking:** Set and manage deadlines to ensure tasks are completed on time.
- **Time Estimation:** Include estimated time, actual time taken, and complexity for better time management and prediction.
- **User Authentication:** Secure user registration, login, and access management.
- **Email Notifications:** Automatically send email confirmations when users contact through the system.
- **Predictive Analytics:** Use machine learning to predict task completion times based on historical data.
- **User-Friendly Interface:** Responsive design for seamless use across devices, including mobile.
- **API Integration:** Comprehensive CRUD operations for tasks through Django REST Framework.

## API Endpoints

- **Tasks API:** `/api/taskInfo/`
  - **GET**: Retrieve a list of tasks or a specific task by ID.
  - **POST**: Create a new task.
  - **PUT/PATCH**: Update an existing task.
  - **DELETE**: Remove a task.

## Screenshot
![Screenshot (5)](https://github.com/user-attachments/assets/7ed14f5f-74d5-472e-92b9-3a5c8295a7e5)
![Screenshot (6)](https://github.com/user-attachments/assets/4fd44acc-03eb-40fd-97b8-b784afc8e9b9)

![Screenshot (7)](https://github.com/user-attachments/assets/92fd6561-85f9-4163-9187-ca47f4d16f13)
![Screenshot (8)](https://github.com/user-attachments/assets/d96dc89f-d214-424e-b407-c61e70af60eb)

![Screenshot (9)](https://github.com/user-attachments/assets/14fcabe0-4d2b-4f20-9cf1-523be445bf47)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/task-management-system.git
   cd task-management-system
