from src.app.models import models
from src.app.services.gitlab_datastore import git_datastore
from src.app.services.gitlab_datastore_files import auth_to_project
from fastapi import APIRouter
from typing import Any

router = APIRouter()


@router.post('/delete_group_project', tags=["Delete"], response_model=Any,
          responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def delete_group_project(auth_git_lab: models.AuthGitLab, directory: models.Group):
    """
    delete group project in GitLab
    """
    response = git_datastore.subgroup_delete(directory.group_name)
    return response


@router.post('/delete_project', tags=["Delete"], response_model=Any,
          responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def delete_project(auth_git_lab: models.AuthGitLab, directory: models.Project):
    """
    delete project in GitLab
    """
    response = git_datastore.project_delete(directory.group_name, directory.project_name)
    return response


@router.post('/delete_folder', tags=["Delete"], response_model=Any,
          responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def delete_folder(auth_git_lab: models.AuthGitLab, directory: models.Directory):
    """
    delete folder in project GitLab
    """
    git_files = auth_to_project(directory.group_name, directory.project_name)
    if type(git_files) == dict:
        return git_files
    return git_files.delete_folder(directory.path)


@router.post('/delete_document', tags=["Delete"], response_model=Any,
          responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def delete_document(auth_git_lab: models.AuthGitLab, directory: models.Directory):
    """
    delete document in project GitLab
    """
    git_files = auth_to_project(directory.group_name, directory.project_name)
    if type(git_files) == dict:
        return git_files
    return git_files.delete_file_from_folder(directory.path)
