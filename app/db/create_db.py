from app.db.database import Base, engine
from app.models.users.users import Users
from app.models.providers.providers import Providers
from app.models.aboniments.aboniments import Aboniments
from app.models.purchases.purchases import Purchases
from app.models.trainers.trainers import Trainers
from app.models.refresh_token import RefreshToken
from app.models.packages.packages import AbonimentPackage
from app.models.workouttimes.workout_times import WorkOutTimes
from app.models.provider_tabs.provider_tabs import ProviderTabs
from app.models.visitation_logs.visitation_logs import VisitationLogs
from app.models.purchases.purchasing_requests import PurchasingRequests
from app.models.photos.photos import Photos
from app.models.telegram.tg_models import TgSettings


def create_table():
    print("Creating db...")
    return Base.metadata.create_all(engine)
