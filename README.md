# Seaker-Alert-App
An application buit with FastAPI used to monitor system memory and cpu usuage which will alert the users when a threashold point is met.

## Features

 Monitor CPU, RAM, Disk usage, Uptime, and optionally device temperature.
 Real-time metrics API built with FastAPI using background scheduler.
 Alerting system with customizable thresholds .
 Dockerized for easy deployment.

### Prerequisites

 Python 3.11+
 Docker & Docker Compose installed (if running with containers)



### Installation

1. Clone the repository
2. Set up a virtual environment and install dependencies:
3. Create a `.env` file in the root directory to configure environment variables like database URL, email credentials, etc.



## Running Locally

Start the FastAPI app locally using Uvicorn:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Visit `http://localhost:8000` to access the API.


## Docker Setup

This project is Dockerized for easy deployment.

### Build Docker Image
docker build -t system-monitor .
### Run Docker Container
docker run --env-file .env -p 8001:8000 system-monitor
The API will be available at `http://localhost:8001`.
