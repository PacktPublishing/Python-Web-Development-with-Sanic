from .some_db_connection import FakeDBConnection


class RegistrationService:
    def __init__(self, connection: FakeDBConnection) -> None:
        self.connection = connection

    async def register_user(self, username: str, email: str) -> None:
        query = "INSERT INTO users VALUES ($1, $2);"
        await self.connection.execute(query, username, email)
