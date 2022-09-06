from src.app.utils.gitlab_util import gl, branch, group
from src.app.services.gitlab_storage import storage
from src.app.utils.messages import CREATED, DELETED, DATA_EXIST, NOT_FOUND, AUTH_ERROR, SERVER_ERROR, UPDATED, RENAMED

from gitlab import GitlabCreateError, GitlabAuthenticationError, GitlabDeleteError, GitlabGetError, GitlabHttpError
from typing import Union

import json
import uuid


class GitDatastoreFiles:
    def __init__(self, subgroup, project):
        self.subgroup = subgroup
        self.project = project
        self._project = gl.projects.get(f'{group}/{subgroup}/{project}')

    def create_folder(self, folder_path: str, author_email: str, author_name: str):
        try:
            file_path = f'{folder_path}/.conf'
            content = ' '
            self._project.files.create(
                {
                    'file_path': file_path,
                    'branch': branch,
                    'content': content,
                    'author_email': author_email,
                    'author_name': author_name,
                    'commit_message': f'Init commit for {folder_path}'
                })
            storage.create_file(self.subgroup, self.project, file_path, content)
            return {'201': CREATED}
        except GitlabCreateError:
            return {'400': DATA_EXIST}

    # def delete_folder(self, subgroup, project, folder_path):
    #     self.auth_to_project(subgroup, project)
    #     for file in self._project.repository_tree(path=f'{folder_path}/', ref=branch, all=True):
    #         file_path = f'{folder_path}/{file["name"]}'
    #         try:
    #             self._project.files.delete(file_path=file_path,
    #                                         commit_message=f'Delete {file["name"]} in folder {folder_path}',
    #                                         branch=branch)
    #             storage.delete_file(subgroup, project, file_path)
    #             return {'200': DELETED}
    #         except GitlabDeleteError:
    #             return {'404': NOT_FOUND}

    def delete_folder(self, folder_path):
        folders = [folder_path]

        while folders != []:
            for folder in folders:
                try:
                    folder_value = self._project.repository_tree(path=f"{folder}/", ref=branch, all=True)
                except:
                    return {'404': NOT_FOUND}

                for inner_file in folder_value:
                    if inner_file['type'] == 'tree':
                        inner_folder = f'{folder}/{inner_file["name"]}'
                        folders.append(inner_folder)
                    else:
                        file_path = f"{folder}/{inner_file['name']}"
                        try:
                            self._project.files.delete(file_path=file_path,
                                                     commit_message=f'Deleted {file_path}',
                                                     branch=branch)
                            #storage.delete_file(self.subgroup, self.project, file_path)
                        except GitlabDeleteError:
                            return {'500': SERVER_ERROR}
                folders.remove(folder)
        try:
            storage.delete_folder(self.subgroup, self.project, folder_path)
        except FileNotFoundError:
            return {'400': NOT_FOUND}
        return {'200': DELETED}

    def create_new_document(self, file_path, author_email, author_name, content=None):
        content = '' if not content else json.dumps(content, ensure_ascii=False)

        data = {
            'branch': branch,
            'author_email': author_email,
            'author_name': author_name,
            'file_path': file_path,
            'content': content,
            'commit_message': "initial_commit"
        }
        try:
            self._project.files.create(data)
            storage.create_file(self.subgroup, self.project, file_path, content)
            return {'201': CREATED}
        except (GitlabCreateError, GitlabHttpError):
            return {'400': DATA_EXIST}
        except:
            return {'500': SERVER_ERROR}

    def write_files_in_folder(self, folder_path: str, content: Union[dict, list],
                                author_email: str, author_name: str, index: Union[str, None] = None):
        """
        Запись файла в папку (= запись строки в таблицу)
        Можно писать как по одному файлу, так и несколько.
        Если параметр content == dict - пишем 1 файл. Если index не указывать, сгенерируется автоматически.
        Если параметр content == list - пишем несколько файлов за 1 раз, index генерируется автоматически.
        Генерация значения для index через uuid.
        """
        # TODO Слишком длинный метод, надо разбить
        if isinstance(content, dict):
            if not index:
                index = uuid.uuid4()

            file_path = f'{folder_path}/{index}.json'
            self.create_new_document(file_path, author_email, author_name, content)

            result = index
        else:
            result = []
            data = {
                'branch': branch,
                'author_email': author_email,
                'author_name': author_name,
                'commit_message': f'Update files in {folder_path}',
                'actions': []
            }

            for item in content:
                content = json.dumps(item, ensure_ascii=False)
                index = uuid.uuid4()
                file_path = f'{folder_path}/{index}.json'
                commit_item_info = {'action': 'create', 'file_path': file_path, 'content': content}

                result.append(index)

                data['actions'].append(commit_item_info.copy())

                storage.create_file(self.subgroup, self.project, file_path, content)
            try:
                self._project.commits.create(data)
            except GitlabAuthenticationError:
                return {'403': AUTH_ERROR}
            except GitlabCreateError:
                return {'500': SERVER_ERROR}
        return result

    def delete_file_from_folder(self, file_path: str):
        try:
            self._project.files.delete(file_path=file_path, commit_message=f'Delete {file_path}', branch=branch)
            storage.delete_file(self.subgroup, self.project, file_path)
            return {'200': DELETED}
        except GitlabDeleteError:
            return {'404': NOT_FOUND}

    def update_file_in_folder(self, file_path, content: dict):
        data = {
            'branch': branch,
            'commit_message': f'Update file {file_path}',
            'actions': [
                {
                    'action': 'update',
                    'file_path': file_path,
                    'content': json.dumps(content, ensure_ascii=False),
                }
            ]
        }
        try:
            self._project.commits.create(data)
            storage.modify_file(self.subgroup, self.project, file_path, content)
            return {'200': UPDATED}
        except (GitlabCreateError, GitlabHttpError):
            return {'400': NOT_FOUND}
        except:
            return {'500': SERVER_ERROR}

    def rename_file(self, file_path, new_file_name):  #можно new_file_path, тогда можно ещё перемещать файл
        path_lst = file_path.split('/')
        file_name = path_lst.pop(-1)
        new_file_path = '/'.join(path_lst) + f'/{new_file_name}' if len(path_lst) != 0 else new_file_name
        if file_name == new_file_name:
            return {'400': DATA_EXIST}
        data = {
            'branch': branch,
            'commit_message': f'Renamed file {file_name}',
            'actions': [
                {
                    'action': 'move',
                    'file_path': new_file_path,
                    'previous_path': file_path
                }
            ]
        }
        try:
            self._project.commits.create(data)
            storage.rename_file(self.subgroup, self.project, file_path, new_file_name)
            return {'200': RENAMED}
        except (GitlabCreateError, GitlabHttpError):
            return {'404': NOT_FOUND}, 'or', {'400': DATA_EXIST}
        except:
            return {'500': SERVER_ERROR}

def auth_to_project(subgroup, project):
    try:
        gitdatastorefiles_object = GitDatastoreFiles(subgroup, project)
        return gitdatastorefiles_object
    except (GitlabHttpError, GitlabGetError):
        return {'404': NOT_FOUND}
    except:
        return {'500': SERVER_ERROR}
