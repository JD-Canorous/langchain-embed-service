from fastapi import FastAPI
from app.api.route_api import router_api

app = FastAPI(title="LangChain Embed Service")

app.include_router(router_api)
