from dataclasses import dataclass


@dataclass
class GitHubAuthCode:
    code: str


@dataclass
class RefreshTokenKey:
    eid: str

    def __str__(self) -> str:
        return f"refresh_token:{self.eid}"
