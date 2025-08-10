from app.web.services.aboniments import aboniments
from app.web.services.packages import packages
from app.web.services.provider_tabs import provider_tabs
from app.web.services.providers import providers
from app.web.services.purchases import purchases
from app.web.services.purchasing_requests import purchasing_requests
from app.web.services.user_auth import login
from app.web.services.users import users
from app.web.services.workouttimes import workout_times
from app.web.services.statistics import statistics
from app.helpers.routes_helper import wrap_modules


MODULES = [
    aboniments,
    packages,
    provider_tabs,
    providers,
    purchases,
    purchasing_requests,
    login,
    users,
    workout_times,
    statistics
]


wrap_modules(MODULES=MODULES)
