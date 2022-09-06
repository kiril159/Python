from fastapi import FastAPI
from create_repo_app import create_repo, create_app
import models

app = FastAPI()


@app.post('/repo_argoCD')
def create_repository(repo: models.CreateRepo):
    return create_repo(repo)


@app.post('/app_argoCD')
def create_application(application: models.CreateApp):
    return create_app(application)



