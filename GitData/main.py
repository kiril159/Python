import uvicorn
import strawberry

from fastapi import FastAPI
from src.app.routers import routers
#from strawberry.fastapi import GraphQLRouter

from src.app.utils.graphql import Query, Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)
# graphql_app = GraphQLRouter(schema)

app = FastAPI(title='GitDatastoreApi',
              docs_url='/datastore-api/docs',
              openapi_url='/datastore-api',
              debug=True
              )

app.include_router(routers, prefix='/datastore-api')
#app.include_router(graphql_app, prefix="/datastore-api/graphql")


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        'main:app',
        workers=1,
    )


if __name__ == "__main__":
    main()
