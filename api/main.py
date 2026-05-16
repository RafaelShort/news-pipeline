import sys

import strawberry
import uvicorn
from fastapi import FastAPI
from loguru import logger
from strawberry.fastapi import GraphQLRouter

from src.schema.queries import Query

# Logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
    level="DEBUG",
)

# GraphQL Schema
schema = strawberry.Schema(query=Query)
graphql_router = GraphQLRouter(schema, graphiql=True)

# FastAPI App
app = FastAPI(
    title="News Pipeline API",
    description="GraphQL API para busca de artigos processados",
    version="1.0.0",
)

app.include_router(graphql_router, prefix="/graphql")


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    logger.info("News API iniciada em http://localhost:8080/graphql")
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
