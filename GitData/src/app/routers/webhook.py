import fastapi

from fastapi import APIRouter
from src.app.utils.gitlab_util import gl
from src.app.services.gitlab_storage import storage

router = APIRouter()


@router.post("/v3/hook")
async def git_elastic_hook(req: fastapi.Request):
    # TODO Слишком большая функция, разбить на несколько
    body = await req.json()
    path = body['project']["path_with_namespace"].split("/")
    group_name = path[0]
    project_name = path[1]
    database_name = path[2]
    branch = body['ref'].split('/')[-1]

    # path_with_namespace = body['project']["path_with_namespace"]
    # database = gl.projects.get(path_with_namespace)

    commit_actions = ['added', 'modified', 'removed']
    commit_results = dict.fromkeys(commit_actions, [])

    for commit in body['commits']:
        for change in commit_actions:
            if commit[change]:
                commit_results[change].extend(commit[change])

    # TODO Нужен рефакторинг
    for action in commit_results:
        if not commit_results[action]:
            continue
        if action == 'removed':
            for row in commit_results[action]:
                folder_name, row_index = row[:-5].split('/')
                await storage.hook_remove_file(group_name, project_name, database_name, branch, folder_name)

                continue
        if action == 'added':
            for row in commit_results[action]:
                folder_name, row_index = row[:-5].split('/')
                # content = database.files.get(file_path=row, ref=branch).decode().decode(encoding='utf-8')
                # content = json.loads(content)
                await storage.hook_create_file(group_name, project_name, database_name, branch, folder_name)

                continue
        if action == 'modified':
            for row in commit_results[action]:
                folder_name, row_index = row[:-5].split('/')
                # content = database.files.get(file_path=row, ref=branch).decode().decode(encoding='utf-8')
                # content = json.loads(content)
                await  storage.hook_modified_file(group_name, project_name, database_name, branch, folder_name)
