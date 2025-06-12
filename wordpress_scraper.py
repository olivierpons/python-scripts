#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WordPress Authenticated Page Fetcher CLI Tool.

This script connects to a WordPress site using provided credentials, and then
retrieves and prints the HTML source code of a specified target page.

It features robust, granular error handling and a structured output system
with multiple verbosity levels. It is designed to be used as a standalone
command-line utility.

Features:
    - Code formatted with `black` for consistent style.
    - Comprehensive type hints for clarity and static analysis.
    - Detailed Google-style docstrings for all methods.
    - Verbosity levels (0=silent, 1=normal, 2=verbose) via the -v flag.
    - Configuration via YAML file with command-line overrides.
    - All parameters are mandatory, ensuring complete configuration.
    - Clear, actionable error messages for each potential failure mode.
"""

import argparse
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import IO, Any, Dict, List, Union

import requests
import yaml
from bs4 import BeautifulSoup


# ==============================================================================
# UTILITY CLASSES AND FUNCTIONS
# ==============================================================================


class CommandError(Exception):
    """A custom exception for application-level errors that should halt execution."""

    pass


def now() -> datetime:
    """
    Returns the current local time.

    A standalone replacement for Django's `timezone.now()`.

    Returns:
        datetime: The current datetime object.
    """
    return datetime.now()


# ==============================================================================
# OUTPUT HANDLER MIXIN
# ==============================================================================


class OutMixin:
    """
    A mixin for handling CLI output. Thread-safe and verbosity-aware.

    This class provides a structured way to print messages to stdout and stderr,
    respecting a verbosity level. All informational and error messages are
    written to stderr to keep stdout clean for the final script output.
    """

    def __init__(
        self, stdout: IO[str] | None = None, stderr: IO[str] | None = None
    ) -> None:
        """
        Initializes the OutMixin.

        Args:
            stdout (IO[str] | None): The stream to use for standard output.
                Defaults to `sys.stdout`.
            stderr (IO[str] | None): The stream to use for error and log output.
                Defaults to `sys.stderr`.
        """
        self._output_lock = threading.RLock()
        self.stdout: IO[str] = stdout or sys.stdout
        self.stderr: IO[str] = stderr or sys.stderr

    def out(self, msg: Union[str, List[str]], is_error: bool = False) -> None:
        """
        Writes a message to the standard error stream with a timestamp.

        This method is thread-safe. It is the core output method used by
        loggers and error handlers.

        Args:
            msg (Union[str, List[str]]): The message or list of messages to write.
            is_error (bool): If True, prefixes the message with an error tag.
        """
        with self._output_lock:
            time_str = now().strftime("%Y-%m-%d %H:%M:%S")
            messages = [msg] if not isinstance(msg, list) else msg
            tag = "ERROR" if is_error else "LOG"

            for line in messages:
                prefix = f"{tag}: {time_str} : "
                self.stderr.write(f"{prefix}{line}\n")

    def abort(self, err: str) -> None:
        """
        Writes a final fatal error message and raises a CommandError.

        This should be used for unrecoverable errors that must terminate the script.

        Args:
            err (str): The final error message to display.

        Raises:
            CommandError: Always raised to halt execution.
        """
        self.stderr.write(f"\n[FATAL ERROR] {err}\n")
        raise CommandError(err)


# ==============================================================================
# WORKER CLASS
# ==============================================================================


class WordPressFetcher:
    """
    Handles the core logic of session management and web requests.

    This class encapsulates the network operations, making it testable and
    separate from the command-line interface logic.
    """

    def __init__(self, base_url: str, logger: Any) -> None:
        """
        Initializes the WordPressFetcher.

        Args:
            base_url (str): The base URL of the WordPress site (e.g., "https://example.com").
            logger (Any): An object with a `log(message, level)` method for output.
        """
        self.base_url: str = base_url.rstrip("/")
        self.logger: Any = logger
        self.session: requests.Session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36"
                )
            }
        )
        self.login_url: str = f"{self.base_url}/wp-login.php"

    def perform_login(self, username: str, password: str) -> None:
        """
        Performs a robust, multistep login to handle custom forms and CSRF tokens.
        """
        # The site's actual login page, not the generic wp-login.php
        login_page_url = f"{self.base_url}/com/login"
        self.logger.log(
            f"Step 1: Fetching login page to get CSRF tokens from {login_page_url}",
            level=2,
        )

        # Step 1: GET the login page to start a session and get the form
        response = self.session.get(login_page_url, timeout=15)
        response.raise_for_status()

        # Step 2: Parse the HTML to find all hidden inputs (CSRF tokens)
        self.logger.log("Step 2: Parsing HTML to extract CSRF tokens...", level=2)
        soup = BeautifulSoup(response.text, "html.parser")
        form = soup.find("form", {"name": "com-login"})
        if not form:
            raise ConnectionError("Could not find the login form on the page.")

        login_payload: Dict[str, str] = {}
        hidden_inputs = form.find_all("input", {"type": "hidden"})
        for field in hidden_inputs:
            # The field might not have a 'value', check for it
            if field.get("name") and field.has_attr("value"):
                login_payload[field["name"]] = field["value"]
                self.logger.log(f"  Found token: {field['name']}", level=2)

        # Add the username and password to the payload
        login_payload["authentication[login]"] = username
        login_payload["authentication[password]"] = password

        # The form's action attribute tells us where to POST
        post_url = self.base_url + form["action"]
        self.logger.log(
            f"Step 3: Sending POST request with credentials and tokens to {post_url}",
            level=1,
        )

        # Step 3: Send the POST request with the complete payload
        login_response = self.session.post(post_url, data=login_payload, timeout=15)
        login_response.raise_for_status()

        # A better success check: After login, the response should NOT contain the login form again.
        # Or, even better, it should contain text like "Mon Compte" or "Déconnexion".
        if (
            "Je me connecte" in login_response.text
            or "authentication[login]" in login_response.text
        ):
            raise ConnectionError(
                "Authentication failed. The server returned the login page again. "
                "Please check credentials. The site might have additional protections."
            )

        self.logger.log("Login successful.", level=1)

    def get_page_source(self, target_url: str) -> str:
        """
        Fetches the source code of the target page using the authenticated session.

        Example:
            This example demonstrates conceptual usage. It is skipped by the
            doctest runner because it requires a live network connection and a
            pre-configured 'logger' object.

            >>> class MockLogger:
            ...     def log(self, *args, **kwargs): pass
            >>> logger = MockLogger()
            >>> fetcher = WordPressFetcher("https://example.com", logger)      # doctest: +SKIP
            >>> source = fetcher.get_page_source("/wp-admin/")                 # doctest: +SKIP
            >>> print("Dashboard" in source)                                    # doctest: +SKIP
            True

        Args:
            target_url (str): The full URL of the page to retrieve.

        Returns:
            str: The HTML source code of the target page.

        Raises:
            requests.exceptions.*: All underlying network exceptions from the
                `requests` library are passed through to the caller.
        """
        self.logger.log(f"Fetching source code from: {target_url}", level=1)
        response = self.session.get(target_url, timeout=20)
        response.raise_for_status()  # Will raise HTTPError for 4xx/5xx responses
        return response.text


# ==============================================================================
# COMMAND CLASS
# ==============================================================================


class WordPressFetcherCommand(OutMixin):
    """
    Manages configuration, orchestration, and user-facing output for the tool.
    """

    def __init__(self) -> None:
        """Initializes the command with default verbosity."""
        super().__init__()
        self.verbosity: int = 1

    def log(self, message: str, level: int = 1) -> None:
        """
        Writes a message to stderr if the current verbosity is high enough.

        Args:
            message (str): The message to log.
            level (int): The required verbosity level to display this message.
                1 is for normal output, 2 is for verbose debug-style output.
        """
        if self.verbosity >= level:
            self.out(message)

    def get_config(self) -> Dict[str, Any]:
        """
        Parses, merges, and validates configuration from YAML and CLI arguments.

        The configuration loading follows a clear priority:
        1. Base values are loaded from the YAML file (if provided).
        2. Any argument provided via the command line will override the YAML value.

        Returns:
            Dict[str, Any]: A validated dictionary containing all required
                configuration parameters.

        Raises:
            CommandError: If configuration is missing required keys or if the
                YAML file is malformed or not found.
        """
        parser = argparse.ArgumentParser(
            description="Connect to a WordPress site and fetch a page's source code.",
            formatter_class=argparse.RawTextHelpFormatter,
        )
        parser.add_argument(
            "-c", "--config", type=Path, help="Path to the YAML config file."
        )
        parser.add_argument(
            "-u", "--url", type=str, help="Base URL of the WordPress site."
        )
        parser.add_argument("--username", type=str, help="WordPress login username.")
        parser.add_argument(
            "--password", type=str, help="WordPress login password or App Password."
        )
        parser.add_argument(
            "-t", "--target-url", type=str, help="Full URL of the page to fetch."
        )
        parser.add_argument(
            "-v",
            "--verbosity",
            type=int,
            choices=[0, 1, 2],
            default=None,  # Default to None to distinguish from user-set '0'
            help="Verbosity level: 0=silent, 1=normal (default), 2=verbose",
        )
        args = parser.parse_args()

        # --- Elegant Configuration Merging ---
        config: Dict[str, Any] = {}

        # 1. Load from YAML file if specified
        if args.config:
            try:
                with open(args.config, "r", encoding="utf-8") as f:
                    yaml_config = yaml.safe_load(f) or {}
                if not isinstance(yaml_config, dict):
                    self.abort(
                        f"Config file '{args.config}' is malformed; root must be a dictionary."
                    )
                config.update(yaml_config)
            except FileNotFoundError:
                self.abort(f"Config file not found at: {args.config}")
            except yaml.YAMLError as e:
                self.abort(f"Error parsing YAML file '{args.config}': {e}")

        # 2. Override with CLI arguments.
        # Create a dictionary of only the arguments provided on the command line.
        cli_overrides = {k: v for k, v in vars(args).items() if v is not None}
        config.update(cli_overrides)

        # Set verbosity for subsequent logging
        self.verbosity = config.get("verbosity", 1)

        # 3. Validate that all required arguments are present in the final config
        required_keys = ["url", "username", "password", "target_url"]
        missing = [key for key in required_keys if key not in config]
        if missing:
            self.abort(
                f"Missing required configuration arguments: {', '.join(missing)}"
            )

        return config

    def execute(self) -> None:
        """
        Main entry point for running the command with detailed error handling.

        This method orchestrates the entire process: getting configuration,
        running the fetcher, and handling all possible exceptions gracefully.
        """
        config = self.get_config()

        # Validate URL format early
        if not str(config["url"]).startswith(("http://", "https://")):
            self.abort("Invalid 'url'. It must start with 'http://' or 'https://'.")

        self.log("--- Final Configuration Summary ---", level=1)
        self.log(f"  Base URL: {config['url']}", level=1)
        self.log(f"  Username: {config['username']}", level=1)
        self.log(f"  Target URL: {config['target_url']}", level=1)
        self.log(f"  Password: {'*' * len(str(config['password']))}", level=2)
        self.log(f"  Verbosity Level: {self.verbosity}", level=1)
        self.log("-----------------------------------", level=1)

        try:
            fetcher = WordPressFetcher(base_url=config["url"], logger=self)
            fetcher.perform_login(config["username"], config["password"])
            source_code = fetcher.get_page_source(config["target_url"])

            if self.verbosity > 0:
                self.log(
                    "Operation successful. Printing source code to stdout.", level=1
                )

            # Print final result directly to stdout for clean piping
            self.stdout.write(source_code)

        # --- GRANULAR EXCEPTION HANDLING ---
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            self.abort(
                f"The server returned an HTTP error: {status_code} {e.response.reason}.\n"
                f"  - URL: {e.request.url}\n"
                f"  - This could mean the page doesn't exist (404), you don't have "
                f"permission (403), or there's a server issue (5xx)."
            )
        except requests.exceptions.Timeout:
            self.abort(
                "The request timed out. The server is taking too long to respond.\n"
                "  - Check your network connection or if the target server is overloaded."
            )
        except requests.exceptions.SSLError:
            self.abort(
                "An SSL error occurred. This can happen with an invalid, "
                "self-signed, or expired certificate.\n"
                "  - Verify the site's SSL certificate is valid."
            )
        except requests.exceptions.ConnectionError:
            self.abort(
                "A connection error occurred. Could not connect to the server.\n"
                "  - Check if the URL/hostname is correct and if you have an active "
                "internet connection.\n"
                "  - A firewall or DNS issue might also be the cause."
            )
        except requests.exceptions.TooManyRedirects:
            self.abort(
                "The request resulted in too many redirects, which often indicates a "
                "server configuration loop."
            )
        except requests.exceptions.RequestException as e:
            # A catch-all for any other exception from the `requests` library.
            self.abort(f"An unexpected network request error occurred: {e}")
        except ConnectionError as e:
            # This catches our custom logical error for a failed login.
            self.abort(str(e))


def main() -> None:
    """Main execution function to instantiate and run the command."""
    try:
        command = WordPressFetcherCommand()
        command.execute()
    except CommandError:
        # The abort() method already printed the specific error. Exit with status 1.
        sys.exit(1)
    except Exception as e:
        # Final, unexpected error catch-all.
        print(f"\n[CRITICAL] An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
