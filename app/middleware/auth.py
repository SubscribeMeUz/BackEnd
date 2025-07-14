import jwt
import secrets
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.models.users.users import Users
from app.db.database import SessionLocal
from app.db.database import SessionManager
from app.web.schemas.users.roles import Roles


db = SessionLocal()

class AuthHandler():

    def __init__(self, check_admin: bool = False):
        self.check_admin = check_admin

    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = 'OrIGiN'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, username):
        payload = {
            'iat': datetime.utcnow(),
            'username': username
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        #########################
        if len(token) < 15:
            with SessionManager() as db:
                user = db.query(Users).filter(Users.username == token).first()
                if user:
                    return user
        #########################
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if 'username' not in payload:
                raise HTTPException(status_code=403, detail={'status':'Signature has expired'})
            with SessionManager() as db:
                user = db.query(Users).filter(Users.username == payload['username']).first()
                if (user is None):
                    raise HTTPException(status_code=403, detail='Not authenticated!')
                if self.check_admin and user.role == Roles.user:
                    raise HTTPException(status_code=403, detail={'status': 'User has no admin privilages'})
                return user
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail={'status':'Signature has expired'})
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail={'status':'Invalid token'})

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    refresh_secret = 'OrIGiN'

    def encode_refresh_token(self, user_id: int):
        token = secrets.token_hex(32)
        expires = datetime.utcnow() + timedelta(days=7)
        return token, expires

    def decode_access_token(self, token: str):
        return jwt.decode(token, self.secret, algorithms=['HS256'])