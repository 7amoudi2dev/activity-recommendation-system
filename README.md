# Activity Recommendation System

A distributed microservices system that recommends activities based on temperature. Built with Flask, PostgreSQL, and Docker.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│  Admin Client   │     │   Web Client    │
│    (CLI)        │     │  (Port 5003)    │
└────────┬────────┘     └────────┬────────┘
         │ HTTP                  │ HTTP
         ↓                       ↓
┌─────────────────┐     ┌─────────────────┐
│   DAO Service   │◄────│ Activity Service│
│  (Port 5001)    │     │  (Port 5002)    │
└────────┬────────┘     └─────────────────┘
         │ SQL
         ↓
┌─────────────────┐
│   PostgreSQL    │
│    (Docker)     │
└─────────────────┘
```

## Features

- **Microservices Architecture**: Separated concerns with independent services
- **RESTful APIs**: Clean API design with proper HTTP methods
- **Activity Recommendations**: Temperature-based activity suggestions
  - ≥25°C → Swimming
  - ≥18°C → Tennis
  - ≥2°C → Hiking
  - <2°C → Skiing
- **Web Interface**: User-friendly form for activity recommendations
- **Admin CLI**: Direct database management tool
- **PostgreSQL Database**: Persistent data storage with Docker

## Prerequisites

- Python 3.7+
- Docker and Docker Compose
- pip (Python package manager)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/activity-recommendation-system.git
   cd activity-recommendation-system
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Start the services**
   ```bash
   # Terminal 1: Database
   docker-compose up -d
   
   # Terminal 2: DAO Service
   python dao_service.py
   
   # Terminal 3: Activity Service
   python activity_service.py
   
   # Terminal 4: Web Client
   python web_client.py
   ```

4. **Access the application**
   - Web Interface: http://localhost:5003
   - Admin CLI: `python admin_client.py`

## Project Structure

```
activity-recommendation-system/
├── docker-compose.yml      # PostgreSQL configuration
├── init.sql               # Database schema
├── dao_service.py         # Data Access API (Port 5001)
├── activity_service.py    # Business Logic API (Port 5002)
├── web_client.py          # Web Interface (Port 5003)
├── admin_client.py        # Admin CLI tool
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## API Documentation

### Activity Service (Port 5002)
- `POST /api/activity` - Get activity recommendation

### DAO Service (Port 5001)
- `GET /requests` - List all requests
- `POST /requests` - Create new request
- `GET /requests/<id>` - Get specific request
- `PUT /requests/<id>` - Update request
- `DELETE /requests/<id>` - Delete request

## Example API Usage

```bash
# Get activity recommendation
curl -X POST http://localhost:5002/api/activity \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "John Doe",
    "birth_date": "1990-01-01",
    "machine_name": "laptop",
    "username": "john",
    "temperature": 25
  }'

# Response
{
  "activity": "Swimming",
  "message": "Activity recommendation saved",
  "temperature": 25
}
```

## Troubleshooting

- **CORS errors**: Ensure flask-cors is installed
- **Connection refused**: Start services in order: Database → DAO → Activity → Web Client
- **Port already in use**: Change port numbers in the respective files

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask framework for Python web services
- PostgreSQL for reliable data storage
- Docker for containerization
