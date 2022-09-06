from src.app.utils.gitlab_util import gl
from src.app.utils.gitlab_util import group, group_id
from src.app.services.gitlab_storage import storage
from src.app.services.file_service import str_format_verity

from gitlab import GitlabCreateError, GitlabGetError

from src.app.utils.messages import CREATED, CHANGE_NAME, DELETED, NOT_FOUND


class GitDatastore:
    group_id = group_id

    def create_subgroup(self, subgroup):
        str_format_verity(subgroup)
        try:
            gl.groups.create({'name': subgroup, 'path': subgroup, 'parent_id': self.group_id})
            storage.create_subgroup(subgroup)
            return {'201': CREATED}
        except GitlabCreateError:
            return {'400': CHANGE_NAME}

    def create_project(self, project, subgroup):
        str_format_verity(project)
        try:
            group_list = gl.groups.list(search=subgroup)

            for i in range(len(group_list)):
                if group_list[i].name == subgroup:
                    subgroup_id = group_list[i].id

                    gl.projects.create({'name': project, 'namespace_id': subgroup_id})
                    storage.create_project(subgroup, project)

                    project_id = gl.projects.get(f'{group}/{subgroup}/{project}').id
                    project = gl.projects.get(project_id)
                    # project.hooks.create(
                    #     {'url': 'https://pulseteam.dev.finch.fm/datastore-api/hook', 'push_events': True})
                    return {'201': CREATED}
            return {'404': NOT_FOUND}
        except GitlabCreateError:
            return {'400': CHANGE_NAME}
        except:
            return {'404': NOT_FOUND}

    def subgroup_delete(self, subgroup: str):
        group_list = gl.groups.list(search=subgroup)

        for i in range(len(group_list)):
            if group_list[i].name == subgroup:
                subgroup_id = group_list[i].id

                gl.groups.delete(subgroup_id)
                storage.delete_subgroup(subgroup)
                return {'200': DELETED}
        return {'404': NOT_FOUND}

    def project_delete(self, subgroup, project):
        try:
            proj = gl.projects.get(f'{group}/{subgroup}/{project}')
            proj.delete()
            storage.delete_project(subgroup, project)
            return {'200': DELETED}
        except GitlabGetError:
            return {'404': NOT_FOUND}


git_datastore = GitDatastore()
