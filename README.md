# Currency Metrics Updater

This Python script uses Prometheus to collect and update currency exchange rate metrics. 
It fetches data from a specified [API](https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json), creates Prometheus Gauge metrics for each currency, and updates their values over time.

# Getting Started

These instructions will help you set up and run the currency metrics updater.

# Prerequisites

Make sure you have the following installed:

    Python 3.x
    pip (Python package installer)

# Installation

    Clone the repository:

```
git clone https://github.com/shaposhnikoff/NBUStatService-prometheus-exporter.git
```

## Navigate to the project directory:

```cd currency-metrics-updater```

## Build Docker container:

```docker build . -t NBUStatService```


# Usage

Run the container:

```docker run -it NBUStatService```

Open Web browser:

```http://localhost:8000```

# Configuration

Adjust the script's configuration by modifying the variables in the script:

    nbu_api_endpoint: The API endpoint for fetching currency data.

Contributing

Feel free to contribute by opening issues or pull requests. Your feedback and contributions are welcome!
License

This project is licensed under the MIT License - see the LICENSE file for details.
