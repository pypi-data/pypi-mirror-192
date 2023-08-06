import pkg_resources
from rich.layout import Layout

version = pkg_resources.get_distribution("climap")


layout = Layout()

layout.split(
    Layout(name=f"{version}", size=4),
    Layout(name="metadata", size=8),
    Layout(
        name="body",
    ),
    Layout(name="footer", size=4),
)

layout["metadata"].split_row(Layout(name="mailboxes"), Layout(name="mails"), Layout(name="session"))

layout["body"].split(
    Layout(name="side"),
    Layout(name="core", ratio=2),
    splitter="row",
)

layout["side"].split(Layout())
