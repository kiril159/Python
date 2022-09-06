from __future__ import annotations

from pydantic import BaseModel, Field


class AuthGitLab(BaseModel):
    author_email: str = Field(..., example='test@yandex.ru')
    author_name: str = Field(..., example='Данилков Николай Сергеевич')


class Group(BaseModel):
    group_name: str = Field(..., example='Group')


class Project(BaseModel):
    group_name: str = Field(..., example='Group')
    project_name: str = Field(..., example='ProjectName')


class Directory(BaseModel):
    group_name: str = Field(..., example='Group')
    project_name: str = Field(..., example='ProjectName')
    path: str = Field(..., example='api/config.json')


class ApiResponse(BaseModel):
    code: int
    type: str
    message: str