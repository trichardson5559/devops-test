import sys
import argparse
from datetime import datetime
import importlib.util

def check_dependencies():
    """
    Checks if the required 'requests' library is installed.
    If not, it prints an error and exits.
    """
    if importlib.util.find_spec("requests") is None:
        print("Error: The 'requests' library is not installed.", file=sys.stderr)
        print("Please install it by running: pip install requests", file=sys.stderr)
        sys.exit(2)  # Exit code 2 for configuration/dependency errors

# It's good practice to import after the dependency check.
check_dependencies()
import requests

def perform_health_check(url, timeout=5):
    """
    Sends an HTTP GET request to the given URL to check its health.

    Args:
        url (str): The URL to check.
        timeout (int): The request timeout in seconds.

    Returns:
        A tuple (bool, str) where the bool is True if healthy (200 OK)
        and the str contains a descriptive message.
    """
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return (True, "OK")
        else:
            return (False, f"Status code {response.status_code}")
    except requests.exceptions.Timeout:
        return (False, "Connection timed out")
    except requests.exceptions.ConnectionError:
        return (False, "Connection failed")
    except requests.exceptions.RequestException as e:
        return (False, f"An unexpected error occurred: {e}")

def log_failure(url, reason):
    """Appends a timestamped failure message to the log file."""
    with open("healthcheck.log", "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] Health check for {url} failed. Reason: {reason}\n")

def main():
    """
    Parses command-line arguments and orchestrates the health check.
    Exits with 0 on success, 1 on failure, and 2 on dependency errors.
    """
    parser = argparse.ArgumentParser(
        description="Performs an HTTP GET health check on a URL.",
        epilog="Exits with 0 on success (200 OK), 1 on failure (e.g., 503, timeout), and 2 on dependency errors."
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8080/health",
        help="The URL to check. Defaults to http://localhost:8080/health"
    )
    args = parser.parse_args()

    # Run the check and get the result.
    is_ok, message = perform_health_check(args.url)

    # Process the result.
    if is_ok:
        print("OK")
        sys.exit(0)
    else:
        print("UNAVAILABLE")
        log_failure(args.url, message)
        sys.exit(1)

if __name__ == "__main__":
    main()