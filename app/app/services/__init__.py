from app.app.services.aboniments import aboniments
from app.app.services.providers import providers
from app.app.services.purchasing_requests import purchasing_requests
from app.app.services.user_auth import user_auth
from app.app.services.users import users
from app.app.services.visitation_logs import visitation_logs
from app.app.services.departments import departments
from app.helpers.routes_helper import wrap_modules


MODULES = [
    aboniments,
    providers,
    purchasing_requests,
    user_auth,
    users,
    visitation_logs,
    departments
]

wrap_modules(MODULES=MODULES)
