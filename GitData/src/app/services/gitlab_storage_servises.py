from git_datastore_api_dev_v2.src.app.utils.gitlab_util import gl
from git_datastore_api_dev_v2.src.app.utils.gitlab_util import branch
from git_datastore_api_dev_v2.src.app.utils.gitlab_util import group
from git_datastore_api_dev_v2.src.app.services.gitlab_to_local import localfile
from gitlab import GitlabGetError


def get_group_list():
    localfile.create_local_dir(group)
    group_list = gl.groups.list()
    return group_list


def get_project_list(subgroup):
    localfile.copy_subgroup_to_local(group, subgroup.name)
    project_list = subgroup.projects.list()
    return project_list


def get_all_files(subgroup, project):
    localfile.copy_project_to_local(group, subgroup.name, project.name)
    project = gl.projects.get(project.id)
    try:
        all_files = project.repository_tree(ref=branch, all=True)
        return all_files
    except GitlabGetError:
        return []


def get_file_value(dict_files, subgroup, project, path_to_file):
    file_value = project.files.get(file_path=path_to_file,
                                   ref=branch).decode().decode(encoding='utf-8')
    if not file_value:
        file_value = 'nothing'
    dict_files[group][subgroup.name][project.name].update({path_to_file: file_value.split('\n')})
    localfile.copy_file_to_local(group, subgroup.name, project.name, path_to_file, file_value)


def unpack_folder(dict_files, subgroup, project, folder):
    folders = [folder]

    while folders != []:
        for folder in folders:
            localfile.copy_folder_to_local(group, subgroup.name, project.name, folder)
            folder_value = project.repository_tree(path=f"{folder}/", ref=branch, all=True)

            for inner_file in folder_value:
                if inner_file['type'] == 'tree':
                    inner_folder = f'{folder}/{inner_file["name"]}'
                    folders.append(inner_folder)
                else:
                    path_to_file = f"{folder}/{inner_file['name']}"
                    get_file_value(dict_files, subgroup, project, path_to_file)
            folders.remove(folder)


def get_dict_files():
    dict_files = {group: {}}
    group_list = get_group_list()

    for subgroup in group_list:
        if subgroup.name.lower() == group.lower():
            continue
        dict_files[group].update({subgroup.name: {}})
        project_list = get_project_list(subgroup)

        for project in project_list:
            project = gl.projects.get(project.id)
            dict_files[group][subgroup.name].update({project.name: {}})
            all_files = get_all_files(subgroup, project)

            for file in all_files:
                if file['type'] == 'tree':
                    folder = file['name']
                    unpack_folder(dict_files, subgroup, project, folder)
                else:
                    path_to_file = file['name']
                    get_file_value(dict_files, subgroup, project, path_to_file)
    return dict_files


def new_file_value(subgroup, project, file_path):
    db_name_with_namespace = f'{group}/{subgroup}/{project}'
    db = gl.projects.get(db_name_with_namespace)

    file_value = db.files.get(ref=branch, file_path=file_path).decode().decode(encoding='utf-8').split('\n')
    return file_value


def semantics(dict_files):
    semanctic = {}

    for subgroup, subgroup_value in dict_files[group].items():
        semanctic.update({subgroup: {}})
        for project, files in subgroup_value.items():
            semanctic[subgroup].update({project: list(files)})

    return semanctic
