from pydantic import BaseModel


class CreateRepo(BaseModel):
    username: str
    password: str
    name: str
    repo: str
    insecure: bool


class CreateApp(BaseModel):
    username: str
    password: str
    name: str
    path: str
    repo: str
    target_revision: str

