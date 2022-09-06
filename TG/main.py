from fastapi import FastAPI
from app import models
from app.for_redmine import get_subtask_id, get_id_project, create_task_redmine, create_subtask_redmine, get_info_red
from app.for_jira import info_jira_task, jira_subtask_key, create_task_jira, create_subtask_jira

app = FastAPI()


@app.post('/epic_red_to_jira')
def epic_red_to_jira(epic: models.IDRedmineJira):
    try:
        for id_task in get_subtask_id(epic.id_redmine):
            info_red = get_info_red(id_task)
            create_subtask_jira(epic.id_jira, info_red)
        return 'successful'
    except:
        return "Incorrect values"


@app.post('/epic_jira_to_red')
def epic_jira_to_red(epic: models.IDJiraRedmine):
    try:
        for id_task in jira_subtask_key(epic.id_jira):
            info_jira = info_jira_task(id_task)
            create_subtask_redmine(get_id_project(epic.id_redmine), info_jira, epic.id_redmine)
        return 'successful'
    except:
        return "Incorrect values"


@app.post('/task_red_to_jira')
def task_red_to_jira(task: models.IDRedmineJira):
    try:
        info_red = get_info_red(task.id_redmine)
        new_issue = create_task_jira(task.id_jira, info_red)
        for id_task in get_subtask_id(task.id_redmine):
            info_red = get_info_red(id_task)
            create_subtask_jira(new_issue, info_red)
        return 'successful'
    except:
        return "Incorrect values"


@app.post('/task_jira_to_red')
def task_jira_to_red(task: models.IDJiraRedmine):
    try:
        info_jira = info_jira_task(task.id_jira)
        new_issue = create_task_redmine(task.id_redmine, info_jira)
        for id_task in jira_subtask_key(task.id_jira):
            info_jira = info_jira_task(id_task)
            create_subtask_redmine(task.id_redmine, info_jira, new_issue)

        return 'successful'
    except:
        return "Incorrect values"
