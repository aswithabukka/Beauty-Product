# Beauty E-commerce Website

A modern e-commerce platform for beauty products with advanced filtering capabilities, similar to Amazon's interface.

## Features

- Product filtering by:
  - Category (Skincare, Makeup, Haircare)
  - Price range
  - Rating
  - Discounts
- Responsive design
- Docker containerization
- MySQL database integration

## Prerequisites

- Docker
- Docker Compose

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd beauty_ecommerce
```

2. Build and start the containers:
```bash
docker-compose up --build
```

3. Access the application:
Open your browser and navigate to `http://localhost:5000`

## Development

The application uses:
- Flask for the backend
- SQLAlchemy for database operations
- Bootstrap 5 for frontend styling
- JavaScript for dynamic filtering

## Project Structure

```
beauty_ecommerce/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── templates/
    ├── base.html
    └── index.html
```

## Environment Variables

The following environment variables can be configured in the `docker-compose.yml` file:
- `MYSQL_ROOT_PASSWORD`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
