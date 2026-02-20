import os
import logging
from logging.handlers import TimedRotatingFileHandler
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.routes import RewriteStaticPathsMiddleware
from app.app.api_routers import user_auth

from app.web.api_routes import create_tables
from app.web.api_routes.user_auth import web_auth
from app.web.api_routes.users import users
from app.web.api_routes.providers import providers
from app.web.api_routes.aboniments import aboniments
from app.web.api_routes.purchases import purchases
from app.web.api_routes.purchasing_requests import purchasing_requests
from app.web.api_routes.workouttimes import workput_times
from app.web.api_routes.packages import packages
from app.web.api_routes.provider_tabs import provider_tabs
from app.web.api_routes.statistics import statistics
from app.web.api_routes.telegram import telegram

from app.app.api_routers.users import user
from app.app.api_routers.aboniments import aboniments as app_aboniments
from app.app.api_routers.providers import providers as app_providers
from app.app.api_routers.visitation_logs import visitation_logs as app_visitation_logs
from app.app.api_routers.purchases import purchasing_requests as app_purchasing_requests
from app.app.api_routers.tools import tools as app_tools

app = FastAPI()

logger = logging.getLogger(__name__)


os.makedirs('logs', exist_ok=True)
formatter = logging.Formatter(u'[%(asctime)s] - %(filename)s:%(lineno)d #%(levelname)-8s  - %(name)s - %(message)s')
handler = TimedRotatingFileHandler('logs/log.log', when="midnight", interval=1, encoding='utf8')
handler.suffix = "%Y-%m-%d_%H-%M-%S"
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


logger.info("Starting fit app")

origins = [
    "*"
    # "https://admin.subme.uz",
    # "http://localhost:3000",
]

app.add_middleware(RewriteStaticPathsMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_auth.router)
app.include_router(user.router)
app.include_router(app_aboniments.router)
app.include_router(app_providers.router)
app.include_router(app_visitation_logs.router)
app.include_router(app_purchasing_requests.router)
app.include_router(app_tools.router)

app.include_router(web_auth.router)
app.include_router(users.router)
app.include_router(packages.router)
app.include_router(provider_tabs.router)
app.include_router(workput_times.router)
app.include_router(providers.router)
app.include_router(aboniments.router)
app.include_router(purchases.router)
app.include_router(purchasing_requests.router)
app.include_router(statistics.router)
app.include_router(create_tables.router)
app.include_router(telegram.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/images", StaticFiles(directory="app/static/images"), name="images")
app.mount("/qr-code", StaticFiles(directory="app/static/qr_codes"), name="qr_codes")
app.mount("/tools", StaticFiles(directory="app/static/tools"), name="tools")
