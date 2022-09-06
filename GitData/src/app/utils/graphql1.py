import typing
import strawberry
from git_datastore_api_dev_v2.src.app.routers.read import get_project_list, get_group_list


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
        return ListDirOut(listDir=get_group_list())


@strawberry.type
class ProjectQuery:
    @strawberry.field
    def list_projects(self, group_name: str) -> ListDirOut:
        return ListDirOut(listDir=get_group_list(group_name))


@strawberry.type
class DocumentQuery:
    @strawberry.field
    def list_document(self, group_name: str, project_name: str) -> ListDirOut:
        pass

    @strawberry.field
    def read_document(self, group_name: str, project_name: str, path: str) -> ReadOut:
        pass


@strawberry.type
class Query:
    @strawberry.field
    def group_query(self) -> GroupQuery:
        pass

    def project_query(self) -> ProjectQuery:
        pass

    def document_query(self) -> DocumentQuery:
        pass


@strawberry.type
class ProjectMutation:
    @strawberry.field
    def create_group(self, group_name: str) -> CreateOut:
        pass

    @strawberry.field
    def delete_group(self, group_name: str) -> DeleteOut:
        pass


@strawberry.type
class GroupMutation:
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
