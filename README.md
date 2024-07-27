# Qeasily - Higher Education Quiz application 

## Overview

This is a backend application for an educational quiz platform built with FastAPI. The application is designed for higher institutions, allowing for the creation and management of quizzes structured into courses and topics. The platform supports various quiz types, user interactions, and payment integrations.

## Features

- RESTful API for quiz functionalities
- Layered directory structure for clean and maintainable code
- MySQL database for data storage
- Dependency injection using FastAPI's dependency injection system
- Support for multiple choice and dual choice (True/False) questions
- Payment and subscription integration with Paystack
- Pagination support for API endpoints

## Directory Structure

The application follows a layer-first directory structure:

app/
├── dependencies/        # Contains dependency functions for injection
├── models/              # Pydantic data models
├── routes/              # API routers, separated by feature
├── utils/               # Utility functions (e.g., for pagination)
├── main.py              # Entry point of the application
├── schema.sql           # Database schema backup

## Getting Started

### Prerequisites

- Python 3.8+
- MySQL database
- FastAPI
- aiomysql
- Uvicorn
- Paystack account for payment integration

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/quiz-app-backend.git
   cd quiz-app-backend
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the MySQL database:**

   - Create a MySQL database.
   - Import the schema from `schema.sql`:

     ```bash
     mysql -u yourusername -p yourdatabase < app/schema.sql
     ```

5. **Configure environment variables:**

   Create a `.env` file in the root directory and add your database and Paystack configuration:

   ```env
   DATABASE_URL=mysql://username:password@localhost/dbname
   PAYSTACK_SECRET_KEY=your_paystack_secret_key
   ```

### Running the Application

1. **Start the FastAPI server:**

   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the API documentation:**

   Open your browser and navigate to `http://127.0.0.1:8000/docs` to explore the interactive API documentation.

## Usage

### API Endpoints

- **Course Management:**
  - Create a course
  - Retrieve courses
  - Update a course
  - Delete a course

- **Topic Management:**
  - Create a topic under a course
  - Retrieve topics for a course
  - Update a topic
  - Delete a topic

- **Quiz Management:**
  - Create a quiz under a topic
  - Retrieve quizzes for a topic
  - Update a quiz
  - Delete a quiz

- **Question Management:**
  - Add questions to a quiz
  - Retrieve questions for a quiz
  - Update a question
  - Delete a question

- **User Interactions:**
  - Take a quiz
  - Submit quiz answers
  - Retrieve user scores

- **Payments and Subscriptions:**
  - Create a subscription
  - Process payments through Paystack

## Contact

For any inquiries or issues, please contact:

- **Author:** Collins Nnanna
- **Email:** kingcollins172@gmail.com
- **GitHub:** [kingcollins17](https://github.com/kingcollins17)

