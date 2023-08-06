from __future__ import annotations

import types
import typing
from imaplib import IMAP4
from imaplib import IMAP4_SSL

from ._config import Config
from ._console import console
from ._types import MailBoxesType


class Client:
    """An encapsulation of an IMAP Client.  This client is underpinned by
    either a IMAP4 client if port 143 is provided otherwise it utilises an
    IMAP4_SSL Client.

    :param host: The imap server host.
    :param port: The imap server port.
    """

    def __init__(self, config: Config) -> None:
        self.config = config
        self._delegate = self.initialise_client()

    def initialise_client(self) -> typing.Union[IMAP4, IMAP4_SSL]:
        """Initialise the underlying wrapped client."""
        client_cls = IMAP4_SSL if self.config.ssl else IMAP4
        try:
            client = client_cls(**self.config.client_args)
            client.login(self.config.user, self.config.password)
            return client
        except ConnectionError:
            console.print_exception()
            raise
        except IMAP4.error:
            console.print_exception()
            raise

    @property
    def total_mailboxes(self) -> int:
        """Retrieve the total number of mail boxes in the server."""
        return 10

    @property
    def total_mails(self) -> int:
        """Retrieve the total number of emails in all mailboxes."""
        return 1337

    def retrieve_mailboxes(self, directory: str = '""', pattern: str = "*") -> MailBoxesType:
        """Retrieves all the mailboxes available in the server.

        :param directory: The directory to recurse, top-level by default.
        :param pattern: Pattern to apply to names, matches anything by default.
        """
        return self._delegate.list()

    def close(self) -> None:
        """Close the underlying imap client."""
        self._delegate.close()

    def __enter__(self) -> Client:
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]] = None,
        exc_val: typing.Optional[BaseException] = None,
        exc_tb: typing.Optional[types.TracebackType] = None,
    ) -> None:
        """Allow the client to be used as a context manager itself."""
        self._delegate.__exit__(exc_type, exc_val, exc_tb)
