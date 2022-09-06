import typing
from typing import Union, Callable, Any

import strawberry
from src.app.routers.read import get_project_list, get_group_list, read_document
from src.app.routers.create import create_new_group_project
from src.app.routers.delete import delete_group_project


@strawberry.input
class Document:
    path: str
    data: str


@strawberry.type
class CreateOut:
    successfully: bool
    errors: typing.List[str] = strawberry.field(default=None)


@strawberry.type
class CommitOut:
    successfully: bool
    errors: typing.List[str] = strawberry.field(default=None)


@strawberry.type
class DeleteOut:
    successfully: bool
    errors: typing.List[str] = strawberry.field(default=None)


@strawberry.type
class ReadOut:
    data: str = strawberry.field(default=None)
    errors: typing.List[str] = strawberry.field(default=None)


@strawberry.type
class ListDirOut:
    listDir: typing.List[str] = strawberry.field(default=None)
    errors: typing.List[str] = strawberry.field(default=None)


@strawberry.type
class GroupQuery:
    @strawberry.field
    def list_groups(self) -> ListDirOut:
        return ListDirOut(listDir=get_group_list)


@strawberry.type
class ProjectQuery:
    @strawberry.field
    def list_projects(self, group_name: str) -> ListDirOut:
        return ListDirOut(listDir=get_project_list(group_name))


@strawberry.type
class DocumentQuery:
    @strawberry.field
    def list_document(self, group_name: str, project_name: str) -> ListDirOut:
        pass

    @strawberry.field
    def read_document(self, group_name: str, project_name: str, path: str) -> ReadOut:
        return ReadOut(data=read_document(group_name, project_name, path))


@strawberry.type
class Query:
    @strawberry.field
    def group_query(self) -> GroupQuery:
        return GroupQuery

    @strawberry.field
    def project_query(self) -> ProjectQuery:
        return ProjectQuery

    @strawberry.field
    def document_query(self) -> DocumentQuery:
        return DocumentQuery


@strawberry.type
class GroupMutation:
    @strawberry.field
    def create_group(self, group_name: str) -> CreateOut:
        try:
            create_new_group_project(group_name)
            return CreateOut(successfully=True)
        except:
            return CreateOut(successfully=False)

    @strawberry.field
    def delete_group(self, group_name: str) -> DeleteOut:
        try:
            delete_group_project(group_name)
            return DeleteOut(successfully=True)
        except:
            return DeleteOut(successfully=False)


@strawberry.type
class ProjectMutation:
    @strawberry.field
    def create_project(self, group_name: str, project_name: str) -> CreateOut:
        pass

    @strawberry.field
    def delete_project(self, group_name: str, project_name: str) -> DeleteOut:
        pass


@strawberry.type
class Mutation:
    @strawberry.mutation
    def project_mutation(self) -> ProjectMutation:
        pass

    @strawberry.mutation
    def group_mutation(self) -> GroupMutation:
        pass

    @strawberry.mutation
    def commit_mutation(self, group_name: str, project_name: str, data: Document) -> CommitOut:
        pass


schema = strawberry.Schema(query=Query, mutation=Mutation)