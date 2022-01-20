from booktracker.common.base_model import BaseModel


class User(BaseModel):
    user_id: int
    eid: str
    login: str
    name: str
    avatar: str
    profile: str

    class Meta:
        pk_field = "user_id"
