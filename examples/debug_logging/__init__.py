"""Debug logging configuration."""

import argparse
import logging


def configure_logging(debug: bool = False) -> None:
    """Configure logging."""
    if debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s",
            handlers=[
                logging.FileHandler(filename='aiovantage.log', mode='w'),
                logging.StreamHandler(),
            ],
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s",
            handlers=[
                logging.StreamHandler(),
            ],
        )


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="aiovantage example")
    parser.add_argument("host", help="hostname of Vantage controller")
    parser.add_argument("--username", help="username for Vantage controller")
    parser.add_argument("--password", help="password for Vantage controller")
    parser.add_argument("--debug", help="enable debug logging", action="store_true")
    return parser.parse_args()
