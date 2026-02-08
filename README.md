# NBU Currency Rate Prometheus Exporter

This Python application fetches currency exchange rates from the National Bank of Ukraine (NBU) API and exposes them as Prometheus metrics. The exporter follows Python best practices with proper type hints, error handling, and code quality standards.

## Features

- Fetches real-time currency exchange rates from [NBU API](https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json)
- Exposes metrics in Prometheus format
- Configurable update interval and port via environment variables
- Comprehensive error handling and logging
- Type-safe code with full mypy compliance
- Optimized with connection pooling

## Prerequisites

- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Installation

### Using uv (recommended)

```bash
# Clone the repository
git clone https://github.com/shaposhnikoff/NBUStatService-prometheus-exporter.git
cd NBUStatService-prometheus-exporter

# Create virtual environment and install dependencies
uv venv .venv
uv pip install -e .
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/shaposhnikoff/NBUStatService-prometheus-exporter.git
cd NBUStatService-prometheus-exporter

# Create virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

## Configuration

The application can be configured using environment variables:

- `METRICS_PORT` - Port for Prometheus metrics endpoint (default: 8000)
- `UPDATE_INTERVAL` - Update interval in seconds (default: 14400 = 4 hours)

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
# Edit .env with your preferred settings
```

## Usage

### Running locally

```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the exporter
python currency.py
```

### Using Docker

```bash
# Build Docker container
docker build . -t nbustat-exporter

# Run the container
docker run -p 8000:8000 nbustat-exporter

# With custom configuration
docker run -p 9090:9090 -e METRICS_PORT=9090 -e UPDATE_INTERVAL=3600 nbustat-exporter
```

### Accessing metrics

Open your browser and navigate to:

```
http://localhost:8000
```

## Development

### Code Quality Tools

Install development dependencies:

```bash
uv pip install ruff mypy types-requests pytest
```

Run code quality checks:

```bash
# Format code
.venv/bin/ruff format currency.py

# Lint code
.venv/bin/ruff check currency.py

# Type check
.venv/bin/mypy currency.py
```

## Project Structure

```
.
├── currency.py          # Main application
├── pyproject.toml       # Project configuration and dependencies
├── Dockerfile           # Docker build configuration
├── .env.example         # Example environment variables
├── .gitignore          # Git ignore rules
├── README.md           # This file
└── argo/               # ArgoCD deployment configuration
    └── argo-app.yaml
```

## Contributing

Contributions are welcome! Please ensure your code:

- Passes all ruff and mypy checks
- Includes type hints for all functions
- Follows PEP 8 style guidelines
- Includes docstrings for public functions
- Has proper error handling

See [CLAUDE.md](CLAUDE.md) for detailed coding guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
