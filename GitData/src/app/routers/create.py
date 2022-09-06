from src.app.services.gitlab_datastore import git_datastore
from src.app.services.gitlab_datastore_files import auth_to_project
from fastapi import APIRouter

from src.app.models import models
from typing import Any

router = APIRouter()


@router.post('/create_new_group_project', tags=["Create"], response_model=Any,
          responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def create_new_group_project(auth_git_lab: models.AuthGitLab, directory: models.Group):
    """
    create new group project in GitLab
    """
    response = git_datastore.create_subgroup(directory.group_name)
    return response



@router.post('/create_new_project', tags=["Create"], response_model=Any,
          responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def create_new_project(auth_git_lab: models.AuthGitLab, directory: models.Project):
    """
    create new project in GitLab
    """
    response = git_datastore.create_project(directory.project_name, directory.group_name)
    return response


@router.post('/create_new_folder', tags=["Create"], response_model=Any,
          responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def create_new_folder(auth_git_lab: models.AuthGitLab, directory: models.Directory):
    """
    create new folder in project GitLab
    """
    git_files = auth_to_project(directory.group_name, directory.project_name)
    if type(git_files) == dict:
        return git_files
    response = git_files.create_folder(directory.path, auth_git_lab.author_email, auth_git_lab.author_name)
    return response


@router.post('/create_new_document', tags=["Create"], response_model=Any,
          responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def create_new_document(auth_git_lab: models.AuthGitLab, directory: models.Directory):
    """
    create new document in project GitLab
    """
    git_files = auth_to_project(directory.group_name, directory.project_name)
    if type(git_files) == dict:
        return git_files
    response = git_files.create_new_document(directory.path, auth_git_lab.author_email, auth_git_lab.author_name)
    return response
