from app.utils import redmine


def get_subtask_id(id_task):
    a = []
    for task in redmine.issue.filter(parent_id=id_task):
        a.append(task.id)
    return a


def get_main_info(id_task):
    project = redmine.project.get(get_id_project(id_task))
    return project.issues.get(id_task)


def get_id_project(id_task):
    test = redmine.issue.get(id_task)
    return test.project.id


def get_info_red(id_task):
    project = redmine.project.get(get_id_project(id_task))
    info_red = project.issues.get(id_task)
    try:
        return [info_red.subject, info_red.description]
    except:
        return [info_red.subject, ' ']


def create_subtask_redmine(id_task, info_task, new_issue):
    redmine.issue.create(
        project_id=id_task,
        subject=info_task[0],
        description=info_task[1],
        parent_issue_id=new_issue)


def create_task_redmine(id_red, info_task):
    task = redmine.issue.create(
        project_id=id_red,
        subject=info_task[0],
        description=info_task[1])
    return task.id




