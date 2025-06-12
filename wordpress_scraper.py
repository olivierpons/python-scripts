#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WordPress Authenticated Page Fetcher CLI Tool (Advanced).

This script connects to a website, handles complex login forms with CSRF
tokens, and retrieves the HTML source code of a protected page.

It is designed for robustness and adaptability, allowing deep configuration
via a YAML file to handle non-standard login mechanisms.

How to get browser headers:
    1. Open your browser (e.g., Chrome).
    2. Open Developer Tools (F12 or Ctrl+Shift+I).
    3. Go to the "Network" tab.
    4. Manually log in to the website.
    5. Find the main request in the network log (e.g., a POST to a 'login' URL).
    6. Click on it, and scroll down to the "Request Headers" section.
    7. Copy these headers into the `headers` section of your `config.yaml`.
"""

import argparse
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import IO, Any, Dict, List, Union
from urllib.parse import urljoin

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
    """Handles the core logic of session management, CSRF, and web requests."""

    def __init__(
        self, base_url: str, logger: Any, headers: Dict[str, str] | None = None
    ):
        """
        Initializes the Fetcher.

        Args:
            base_url (str): The base URL of the target website.
            logger (Any): A logger object with a `log(msg, level)` method.
            headers (Dict[str, str] | None): Custom HTTP headers to use for all requests.
        """
        self.base_url: str = base_url.rstrip("/")
        self.logger: Any = logger
        self.session: requests.Session = requests.Session()

        # Set default headers and then override/extend with custom ones.
        default_headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            ),
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
            "Connection": "keep-alive",
        }
        self.session.headers.update(default_headers)
        if headers:
            self.session.headers.update(headers)
            self.logger.log("Custom headers have been applied to the session.", level=2)

    def perform_login(self, config: Dict[str, Any]) -> None:
        """
        Performs a robust, multi-step login to handle custom forms and CSRF tokens.

        This method first fetches the login page, parses it to find the form's
        action URL and hidden CSRF tokens, and then submits a complete payload.

        Args:
            config (Dict[str, Any]): A configuration dictionary containing login details
                like username, password, paths, and field names.

        Raises:
            ConnectionError: If the login form cannot be found or if authentication
                is explicitly rejected by the server after submission.
            requests.exceptions.*: All underlying network exceptions are passed through.
        """
        username = config["username"]
        password = config["password"]
        login_path = config.get("login_page_path", "/wp-login.php")
        login_page_url = urljoin(self.base_url, login_path)

        self.logger.log(f"Step 1: Fetching login page for CSRF tokens...", level=1)
        self.logger.log(f"  URL: {login_page_url}", level=2)
        response = self.session.get(login_page_url, timeout=15)
        response.raise_for_status()

        self.logger.log("Step 2: Parsing HTML to extract form data...", level=1)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the form. We prioritize finding a form with a password field.
        form = soup.find("form", {"action": True})
        if soup.find("input", {"type": "password"}):
            form = soup.find("input", {"type": "password"}).find_parent("form")

        if not form:
            raise ConnectionError("Could not find any <form> on the login page.")

        # Extract all hidden inputs for CSRF tokens
        login_payload: Dict[str, str] = {
            field.get("name"): field.get("value", "")
            for field in form.find_all("input", {"type": "hidden"})
            if field.get("name")
        }
        self.logger.log(f"  Found {len(login_payload)} hidden token(s).", level=2)

        # Add credentials using configured field names
        username_field = config.get("username_field", "log")
        password_field = config.get("password_field", "pwd")
        login_payload[username_field] = username
        login_payload[password_field] = password
        self.logger.log(f"  Mapping username to field '{username_field}'.", level=2)
        self.logger.log(f"  Mapping password to field '{password_field}'.", level=2)

        # Determine the POST URL from the form's 'action' attribute
        post_url = urljoin(self.base_url, form["action"])
        self.logger.log(f"Step 3: Submitting login POST to {post_url}", level=1)

        login_response = self.session.post(post_url, data=login_payload, timeout=15)
        login_response.raise_for_status()

        # If the response still contains a password field, login failed.
        if '<input type="password"' in login_response.text.lower():
            raise ConnectionError(
                "Authentication failed. The server returned a page with a login form. "
                "Please double-check credentials and YAML configuration "
                "(field names, etc.)."
            )

        self.logger.log("Login successful. Session is authenticated.", level=1)

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
            description="Connect to a website and fetch a page's source code.",
            formatter_class=argparse.RawTextHelpFormatter,
        )
        parser.add_argument(
            "-c", "--config", type=Path, help="Path to YAML config file."
        )
        parser.add_argument("-u", "--url", type=str, help="Base URL of the website.")
        parser.add_argument("--username", type=str, help="Login username.")
        parser.add_argument("--password", type=str, help="Login password.")
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
        if missing := [key for key in required_keys if key not in config]:
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
            self.abort("Invalid 'url'. Must start with 'http://' or 'https://'.")

        self.log("--- Final Configuration Summary ---", level=1)
        self.log(f"  Base URL: {config['url']}", level=1)
        self.log(f"  Username: {config['username']}", level=1)
        self.log(f"  Target URL: {config['target_url']}", level=1)
        self.log(f"  Custom Headers: {'Yes' if 'headers' in config else 'No'}", level=1)
        self.log(f"  Password: {'*' * len(str(config['password']))}", level=2)
        self.log(f"  Verbosity Level: {self.verbosity}", level=1)
        self.log("-----------------------------------", level=1)

        try:
            fetcher = WordPressFetcher(
                base_url=config["url"],
                logger=self,
                headers=config.get("headers"),
            )
            fetcher.perform_login(config)  # Pass the whole config
            source_code = fetcher.get_page_source(config["target_url"])

            # Print final result directly to stdout for clean piping
            self.log("Operation successful. Printing source code to stdout.", level=1)
            self.stdout.write(source_code)

        except requests.exceptions.HTTPError as e:
            self.abort(
                f"HTTP Error: {e.response.status_code} {e.response.reason} for URL {e.request.url}"
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
