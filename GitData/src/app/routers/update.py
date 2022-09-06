from src.app.models import models
from src.app.services.gitlab_datastore_files import auth_to_project
from typing import Any
from fastapi import APIRouter

router = APIRouter()


@router.post('/update_document', tags=["Update"], response_model=Any,
          responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def update_document(auth_git_lab: models.AuthGitLab, directory: models.Directory, new_value):
    """
    update documents in project GitLab
    """
    git_files = auth_to_project(directory.group_name, directory.project_name)
    if type(git_files) == dict:
        return git_files
    return git_files.update_file_in_folder(directory.path, new_value)


@router.post('/update_batch_document', tags=["Update"], response_model=Any,
          responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def update_batch_document(auth_git_lab: models.AuthGitLab, directory: models.Directory, new_value):
    """
    update batch documents in project GitLab
    """
    git_files = auth_to_project(directory.group_name, directory.project_name)
    if type(git_files) == dict:
        return git_files
    return git_files.write_files_in_folder(directory.path, new_value, auth_git_lab.author_email, auth_git_lab.author_name)


@router.post('/rename_file', tags=["Update"], response_model=Any,
          responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def rename_document(auth_git_lab: models.AuthGitLab, directory: models.Directory, new_file_name):
    """
    update batch documents in project GitLab
    """
    git_files = auth_to_project(directory.group_name, directory.project_name)
    if type(git_files) == dict:
        return git_files
    return git_files.rename_file(directory.path, new_file_name)
