from app.utils import jira


def info_jira_task(id_task):
    for singleIssues in jira.search_issues(jql_str=f' id={id_task} '):
        return [singleIssues.fields.summary, singleIssues.fields.description]


def get_key_project_jira(id_task):
    for singleIssues in jira.search_issues(jql_str=f' id={id_task} '):
        return singleIssues.fields.project.key


def jira_subtask_key(id_task):
    return jira.search_issues(jql_str=f'parent = {id_task} ')


def create_subtask_jira(id_jira, info_red):
    jira.create_issue(project=get_key_project_jira(id_jira), summary=info_red[0],
                      description=info_red[1], issuetype={'name': 'Подзадача'},
                      parent={'id': str(id_jira)})


def create_task_jira(id_jira, info_red):
    task = jira.create_issue(project=id_jira, summary=info_red[0], description=info_red[1],
                      issuetype={'name': 'Задача'})
    return task.id



