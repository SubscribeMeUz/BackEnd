from fastapi import Depends
from app.middleware.auth import AuthHandler


auth_handler = AuthHandler()
admin_auth_handler = AuthHandler(check_admin=True)
provider_auth_handler = AuthHandler(check_provider=True)
auth = lambda: Depends(auth_handler.auth_wrapper)
admin_auth = lambda: Depends(admin_auth_handler.auth_wrapper)
provider_auth = lambda: Depends(provider_auth_handler.auth_wrapper)
