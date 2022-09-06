import requests

with open("ssh_key") as file:
    key_s = file.read()


def create_repo(repo):
    data_auth = {
        "username": repo.username,
        "password": repo.password
    }
    data_repo = {
        "type": "git",
        "name": repo.name,
        "repo": repo.repo,
        "sshPrivateKey": key_s,
        "insecure": repo.insecure
    }

    s = requests.Session()
    auth = s.post(url="https://argocd.dev.finch.fm/api/v1/session", json=data_auth)
    if "error" in auth.json():
        return auth.json()
    post_repo = s.post('https://argocd.dev.finch.fm/api/v1/repositories', json=data_repo)
    return post_repo.json()


def create_app(application):
    data_auth = {
        "username": application.username,
        "password": application.password
    }
    data_app = {
        "apiVersion": "argoproj.io/v1alpha1",
        "kind": "Application",
        "metadata": {
            "name": application.name
        },
        "spec": {
            "destination": {
                "name": "",
                "namespace": "",
                "server": "https://kubernetes.default.svc"
            },
            "source": {
                "path": application.path,
                "repoURL": application.repo,
                "targetRevision": application.target_revision
            },
            "project": "default"
        }
    }

    s = requests.Session()
    auth = s.post(url="https://argocd.dev.finch.fm/api/v1/session", json=data_auth)
    if "error" in auth.json():
        return auth.json()
    post_app = s.post('https://argocd.dev.finch.fm/api/v1/applications', json=data_app)
    return post_app.json()
