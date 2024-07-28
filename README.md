# Qeasily - Higher Education Quiz application 
### Check out the Live API docs at
 - [Qeasily REST API documentation](https://qeasily-backend.onrender.com/redoc)

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


The application follows a layer-first directory structure


### Core dependencies

- Python 3.8+
- MySQL database
- FastAPI
- aiomysql
- Uvicorn
- Paystack account for payment integration



## Usage and Features 

### API Features

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

