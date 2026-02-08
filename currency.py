"""NBU Currency Rate Prometheus Exporter.

This module fetches currency exchange rates from the National Bank of Ukraine
API and exposes them as Prometheus metrics.
"""

import logging
import os
import time
from typing import Any, cast

import orjson
import requests
from prometheus_client import Gauge, start_http_server

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
NBU_API_ENDPOINT = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
DEFAULT_PORT = 8000
DEFAULT_UPDATE_INTERVAL = 60 * 60 * 4  # 4 hours

# Configuration from environment
METRICS_PORT = int(os.getenv("METRICS_PORT", DEFAULT_PORT))
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", DEFAULT_UPDATE_INTERVAL))

# Global state
currencies_metrics: dict[str, Gauge] = {}
session = requests.Session()


def fetch_currency_data() -> list[dict[str, Any]]:
    """Fetch currency exchange rates from NBU API.

    Returns:
        List of currency data dictionaries

    Raises:
        requests.RequestException: If API request fails
        ValueError: If response cannot be parsed as JSON
    """
    try:
        response = session.get(NBU_API_ENDPOINT, timeout=10)
        response.raise_for_status()
        return cast(list[dict[str, Any]], orjson.loads(response.content))
    except requests.RequestException as e:
        logger.error(f"Failed to fetch currency data: {e}")
        raise
    except ValueError as e:
        logger.error(f"Failed to parse currency data: {e}")
        raise


def create_metrics() -> None:
    """Create Prometheus metrics for all currencies from NBU API.

    Fetches currency data and creates a Gauge metric for each currency.
    Metrics are stored in the global currencies_metrics dictionary.

    Raises:
        requests.RequestException: If API request fails
        ValueError: If response cannot be parsed
    """
    logger.info("Creating metrics")
    try:
        data = fetch_currency_data()
        for item in data:
            currency_code = item["cc"]
            currency_metric = Gauge(
                currency_code, "Currency exchange rate", ["date", "currency_name"]
            )
            currencies_metrics[currency_code] = currency_metric
        logger.info(f"Created {len(currencies_metrics)} currency metrics")
    except (requests.RequestException, ValueError, KeyError) as e:
        logger.error(f"Failed to create metrics: {e}")
        raise


def reload_currencies() -> None:
    """Update all currency metrics with latest exchange rates.

    Fetches current currency data and updates the Prometheus metrics
    with the latest rates.

    Raises:
        requests.RequestException: If API request fails
        ValueError: If response cannot be parsed
    """
    logger.info("Reloading currencies")
    try:
        data = fetch_currency_data()
        current_date = time.strftime("%Y-%m-%d")

        for item in data:
            currency_code = item["cc"]
            if currency_code in currencies_metrics:
                currencies_metrics[currency_code].labels(
                    date=current_date, currency_name=currency_code
                ).set(item["rate"])

        logger.info(f"Updated {len(data)} currencies")
    except (requests.RequestException, ValueError, KeyError) as e:
        logger.error(f"Failed to reload currencies: {e}")
        raise


def main() -> None:
    """Main entry point for the currency exporter.

    Starts the Prometheus HTTP server and continuously updates currency
    metrics at the configured interval.
    """
    logger.info(f"Starting Prometheus exporter on port {METRICS_PORT}")
    start_http_server(METRICS_PORT)

    try:
        create_metrics()
    except Exception as e:
        logger.error(f"Failed to initialize metrics: {e}")
        return

    while True:
        try:
            logger.info("Updating metrics")
            reload_currencies()
            logger.info(f"Sleeping for {UPDATE_INTERVAL} seconds")
            time.sleep(UPDATE_INTERVAL)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            break
        except Exception as e:
            logger.error(f"Error updating metrics: {e}")
            logger.info("Retrying in 60 seconds...")
            time.sleep(60)


if __name__ == "__main__":
    main()
