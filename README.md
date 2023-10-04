# Excel with Python

We all know there is no better software in the world than Excel.
The powerful idea behind the cells and formulas allows many of us to understand programming. 

This project implements simple excel-alike API with Python and Django Rest Framework.

## Endpoints

Users can interact with the service through the following methods and endpoints:

1. POST /api/v1/:sheet_id/:cell_id: Accepts parameters to update or insert data in a cell. It implements an UPSERT strategy, returning a 201 status if successful and a 422 status if there are issues, such as formula errors.

  Here are examples of requests (it might be any mathematical expression, including +-*/ and ()):
  - {"value": "1"}
  - {"value": "=A1+B1"} if you want to evaluate the formula (here A1 and B1 are cells names in this spreadsheet)
  - {"value": "=2+2"} if you want to evaluate numbers and not cells

2. GET /api/v1/:sheet_id/:cell_id: Retrieves data from a specified cell, returning a 200 status if the data is present and a 404 status if it's missing.

3. GET /api/v1/:sheet_id: Retrieves data from an entire sheet, returning a 200 status if the sheet exists and a 404 status if it's missing.

## Supported Features

- Supports basic data types: string, integer, and float.
- Handles basic math operations such as addition (+), subtraction (-), division (/), multiplication (*), and parentheses ().
- Case-insensitive for sheet and cell IDs.
- Persists data, ensuring availability between Docker container restarts.
- Supports JWT authentication.

## Thoughts and Choices
Here are some thoughts on the choices made during the development of this project:
- Docker: Docker was chosen to containerize the application and database for easy setup and reproducibility across different environments.
- Environment Variables: Environment variables are used for sensitive configuration settings, making it easy to manage different configurations for development, testing, and production.
- PostgreSQL: PostgreSQL was chosen as the database because of its robustness and support for Django.

## Next Steps
To make this service even better, consider the following next steps:
- Django Settings: Review and optimize Django settings for security, performance, and scalability.
- Continuous Integration: Set up a CI/CD pipeline to automate testing and deployment.
- Frontend: If applicable, integrate a frontend framework or library to create a complete web application.
- Documentation: Expand the project documentation, including API documentation if it's an API service.
- Scaling: Plan for scaling the application by considering load balancing and database replication.

## Getting Started

To get started, you'll need Docker installed on your machine.

### Running the Service

To start the service, follow these steps:

- Create venv and activate it through terminal:
```git
python -m venv myvenv

#Windows activaition:
myvenv\Scripts\activate

#Unix or Linux activation:
source myvenv/bin/activate
```
- Copy .env.sample file, rename it to .env. Populate it with all required data.
- Run app via Docker through terminal:
```git
docker-compose up --build
```
- Create admin user

## How to register
- Create user at /user/ endpoint
- Get user token at /user/token/ endpoint
- Authorize with it or use ModHeader with Request header:
```
Header: Authorization
Value: Bearer <Your access token> 
```

## How to run tests
This project has test which can be run via Docker. To run them use this command:
```git
docker-compose run app sh -c "python manage.py test"
```
