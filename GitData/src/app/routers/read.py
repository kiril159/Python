from fastapi import APIRouter

from src.app.models import models
from src.app.services.gitlab_storage import storage
from typing import Any

router = APIRouter()



@router.get('/read_document', tags=["Read"], response_model=Any,
         responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def read_document(group_name, project_name, path):
    """
    Read document from Gitlab
    """
    file_value = storage.read_file_from_dict(group_name, project_name, path)
    return file_value


@router.get('/get_group_list', tags=["Read"]) #dependencies=[Depends(oauth2_scheme)])
def get_group_list():
    """
    get group list
    """
    return storage.get_group_list()


@router.get('/get_project_list', tags=["Read"], response_model=Any,
         responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def get_project_list(group_name):
    """
    get project list
    """
    return storage.get_project_list(group_name)


@router.get('/get_path_semantics_in_project', tags=["Read"], response_model=Any,
         responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def get_path_semantics_in_project(group_name, project_name):
    """
    get path semantics in a project
    """
    return storage.get_path_semantics_in_project(group_name, project_name)


@router.get('/get_path_semantics_in_group', tags=["Read"], response_model=Any,
         responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def get_path_semantics_in_group(group_name):
    """
    get path semantics in a group
    """
    return storage.get_path_semantics_in_group(group_name)



@router.get('/get_path_semantics_in_storage', tags=["Read"], response_model=Any,
         responses={'401': {'model': models.ApiResponse}, '404': {'model': models.ApiResponse}}) #dependencies=[Depends(oauth2_scheme)])
def get_path_semantics_in_storage():
    """
    get complete path semantics in a storage
    """
    return storage.semantics
