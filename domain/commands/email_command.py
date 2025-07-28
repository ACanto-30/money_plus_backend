from dataclasses import dataclass

@dataclass(frozen=True)
class EmailCommand:
    to: str
    subject: str
    body: str
    cc: list[str]
    bcc: list[str]
    html_body: str