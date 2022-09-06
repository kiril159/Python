from pydantic import BaseModel


class IDRedmineJira(BaseModel):
    id_redmine: int
    id_jira: int


class IDJiraRedmine(BaseModel):
    id_jira: int
    id_redmine: int