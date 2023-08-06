"""" The main logic of the live terminal output.

Exit codes are as follows:
    1 - Unable to establish a connection to the imap server.
    2 - An issue with authenticating occurred, likely invalid credentials.
"""

import imaplib
import time

from rich import print
from rich.live import Live
from rich.panel import Panel
from rich.prompt import IntPrompt
from rich.prompt import Prompt
from rich.spinner import Spinner

from .__version__ import __version__
from ._client import Client
from ._config import Config
from ._console import console
from ._layout import layout


def main() -> int:
    """Main entry point into cli map."""
    config: Config = initialise()
    spinner = Spinner(name="aesthetic", text="Connecting to the imap server...")
    panel = Panel(spinner)

    with Live(renderable=panel, console=console) as live:
        time.sleep(5)  # mock for now.
        try:
            with Client(config=config) as client:  # noqa
                while True:
                    live.update(layout)
                    time.sleep(10)  # mock for now.
                    break
        except ConnectionError:
            return 1
        except imaplib.IMAP4.error:
            return 2
    return 0


def initialise() -> Config:
    """Prompt for configuration."""
    print(f"[{__version__} Successfully loaded.]")
    host = Prompt().ask(":rocket: What is the host of the imap server", default="localhost")
    port = IntPrompt().ask(":rocket: What is the port of the imap server", default=993)
    ssl = IntPrompt().ask(":rocket: Use an ssl client", default=True)
    user = Prompt().ask(":couple: What is the imap username")
    password = Prompt().ask(":unlock: Enter the password", password=True)
    return Config(host=host, port=port, ssl=ssl, user=user, password=password)


if __name__ == "__main__":
    raise SystemExit(main())
