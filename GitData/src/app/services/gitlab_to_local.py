import os
from git_datastore_api_dev_v2.src.app.utils.messages import NOT_FOUND
import shutil


class LocalFile:
    def create_local_dir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def create_folders_from_path(self, group, subgroup, project, path):
        folders = path.split('/')
        folder_path = f'{group}/{subgroup}/{project}'
        del folders[-1]

        for folder in folders:
            folder_path += f'/{folder}'
            self.create_local_dir(folder_path)

    def copy_subgroup_to_local(self, group, subgroup):
        self.create_local_dir(f'{group}/{subgroup}')

    def copy_project_to_local(self, group, subgroup, project):
        self.create_local_dir(f'{group}/{subgroup}/{project}')

    def copy_folder_to_local(self, group, subgroup, project, path):
        self.create_local_dir(f'{group}/{subgroup}/{project}/{path}')

    def copy_file_to_local(self, group, subgroup, project, path, file_value):
        self.create_folders_from_path(group, subgroup, project, path)
        file_value = '' if file_value in ([], None, '', "", {}, [""], [''], 'nothing') else file_value
        with open(f'{group}/{subgroup}/{project}/{path}', mode='w', encoding='utf-8') as fl:
            fl.writelines(file_value)

    def delete_local_subgroup(self, group, subgroup):
        shutil.rmtree(f"{group}/{subgroup}")

    def delete_local_project(self, group, subgroup, project):
        shutil.rmtree(f"{group}/{subgroup}/{project}")

    def delete_local_folder(self, group, subgroup, project, folder_path):
        shutil.rmtree(f"{group}/{subgroup}/{project}/{folder_path}")

    def delete_local_file(self, group, subgroup, project, file_path):
        os.remove(f"{group}/{subgroup}/{project}/{file_path}")

    def change_local_file(self, group, subgroup, project, file_path, file_value):
        with open(f"{group}/{subgroup}/{project}/{file_path}", mode='w', encoding='utf-8') as file:
            file.writelines(file_value)

    def rename_file(self, group, subgroup, project, file_path, new_file_path):
        old_localfile_path = f"{group}/{subgroup}/{project}/{file_path}"
        new_localfile_path = f"{group}/{subgroup}/{project}/{new_file_path}"
        os.rename(old_localfile_path, new_localfile_path)


localfile = LocalFile()
