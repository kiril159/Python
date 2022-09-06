from git_datastore_api_dev_v2.src.app.services.gitlab_storage_servises import get_dict_files, new_file_value, semantics
from git_datastore_api_dev_v2.src.app.utils.gitlab_util import group
from git_datastore_api_dev_v2.src.app.utils.messages import NOT_FOUND
from git_datastore_api_dev_v2.src.app.services.gitlab_to_local import localfile


class Storage:
    dict_files = get_dict_files()
    semantics = {}
# Можно сделать отдельный класс для семантики
    @classmethod
    def update_semantics(cls):
        cls.semantics = semantics(cls.dict_files)

    def __init__(self):
        self.update_semantics()

    @classmethod
    def create_file(cls, subgroup, project, path, file_value=None):
        if not file_value:
            file_value = new_file_value(subgroup, project, path)
        try:
            cls.dict_files[group][subgroup][project].update({path: file_value})
            cls.update_semantics()
            localfile.copy_file_to_local(group, subgroup, project, path, file_value=None)
        except KeyError:
            return {'404': NOT_FOUND}

    @classmethod
    def create_project(cls, subgroup, project):
        try:
            cls.dict_files[group][subgroup].update({project: {}})
            cls.update_semantics()
            localfile.copy_project_to_local(group, subgroup, project)
        except KeyError:
            return {'404': NOT_FOUND}

    @classmethod
    def create_subgroup(cls, subgroup):
        try:
            cls.dict_files[group].update({subgroup: {}})
            cls.update_semantics()
            localfile.copy_subgroup_to_local(group, subgroup)
        except KeyError:
            return {'404': NOT_FOUND}

    @classmethod
    def delete_file(cls, subgroup, project, file_path):
        try:
            del cls.dict_files[group][subgroup][project][file_path]
            cls.update_semantics()
            localfile.delete_local_file(group, subgroup, project, file_path)
        except KeyError:
            return {'404': NOT_FOUND}

    @classmethod
    def delete_project(cls, subgroup, project):
        try:
            del cls.dict_files[group][subgroup][project]
            cls.update_semantics()
            localfile.delete_local_project(group, subgroup, project)
        except KeyError:
            return {'404': NOT_FOUND}

    @classmethod
    def delete_subgroup(cls, subgroup):
        try:
            del cls.dict_files[group][subgroup]
            cls.update_semantics()
            localfile.delete_local_subgroup(group, subgroup)
        except KeyError:
            return {'404': NOT_FOUND}

    @classmethod
    def delete_folder(cls, subgroup, project, folder_path):
        folder_files_list = cls.get_path_semantics_in_folder(subgroup, project, folder_path)
        try:
            for file in folder_files_list:
                del cls.dict_files[group][subgroup][project][file]
            cls.update_semantics()
            localfile.delete_local_folder(group, subgroup, project, folder_path)
        except KeyError:
            return {'404': NOT_FOUND}

    @classmethod
    def modify_file(cls, subgroup, project, path, file_value=None):
        if not file_value:
            file_value = new_file_value(subgroup, project, path)
        try:
            cls.dict_files[group][subgroup][project][path] = file_value
            cls.update_semantics()
            localfile.change_local_file(group, subgroup, project, path, file_value)
        except KeyError:
            return {'404': NOT_FOUND}

    @classmethod
    def rename_file(cls, subgroup, project, path, new_file_name):
        path_lst = path.split('/')
        del path_lst[-1]
        new_path = '/'.join(path_lst) + f'/{new_file_name}' if len(path_lst) != 0 else new_file_name
        try:
            file_value = cls.dict_files[group][subgroup][project][path]
            cls.dict_files[group][subgroup][project][new_path] = file_value
            del cls.dict_files[group][subgroup][project][path]
            cls.update_semantics()
            localfile.rename_file(group, subgroup, project, path, new_path)
        except KeyError:
            return {'404': NOT_FOUND}

    @classmethod
    def read_file_from_dict(cls, subgroup, project, path):
        try:
            return cls.dict_files[group][subgroup][project][path]
        except KeyError:
            return {'404': NOT_FOUND}

    @classmethod
    def get_path_semantics_in_folder(cls, subgroup_name, project_name, folder_path):
        project_value = cls.semantics[subgroup_name][project_name]
        semantics_in_folder = [file for file in project_value if file.startswith(folder_path)]
        return semantics_in_folder

    def get_path_semantics_in_group(self, subgroup_name):
        try:
            semantics_in_group = {subgroup_name: self.semantics[subgroup_name]}
            return semantics_in_group
        except KeyError:
            return {'404': NOT_FOUND}

    def get_path_semantics_in_project(self, subgroup_name, project_name):
        try:
            project_value = self.semantics[subgroup_name][project_name]
            semantics_in_project = {subgroup_name: {project_name: project_value}}
            return semantics_in_project
        except KeyError:
            return {'404': NOT_FOUND}

    def get_group_list(self):
        group_list = [subgroup for subgroup in self.semantics]
        return group_list

    def get_project_list(self, subgroup_name):
        try:
            semantics_in_group = self.semantics[subgroup_name]
            project_list = [project for project in semantics_in_group]
            return project_list
        except KeyError:
            return {'404': NOT_FOUND}


storage = Storage()
