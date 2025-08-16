from sqlalchemy import func, cast, literal, Interval
from sqlalchemy.orm import Session, joinedload, with_loader_criteria
from sqlalchemy.sql import and_
from app.models.providers.providers import Providers
from app.models.provider_tabs.provider_tabs import ProviderTabs
from app.models.aboniments.aboniments import Aboniments
from app.models.packages.packages import AbonimentPackage
from app.models.workouttimes.workout_times import WorkOutTimes
from app.models.users.users import Users
from app.models.purchases.purchases import Purchases
from app.models.visitation_logs.visitation_logs import VisitationLogs
from app.app.services.providers import providers as app_providers
from app.web.schemas.purchases.purchases import PurchasesStatuses as purchase_statuses


def get_user_purchased_aboniments(db: Session, user: Users):
    resp = (
        db
        .query(Aboniments)
        .join(Aboniments.purchases)
        .join(Aboniments.aboniment_package)
        .filter(Purchases.user_id == user.id, Purchases.status == purchase_statuses.NEW)
        .filter(
            Purchases.recorded_date + cast(literal("1 day"), Interval) * AbonimentPackage.expiry_days >= func.now()
        )
        .options(joinedload(Aboniments.purchases),
                 joinedload(Aboniments.provider),
                 joinedload(Aboniments.aboniment_package),
                 joinedload(Aboniments.workout_time))
        .order_by(Purchases.recorded_date.desc())
        .all()
    )
    for i in resp:
        setattr(i, 'user_id', user.id)
    return resp


def get_provider_aboniments(db: Session, provider_id: int) -> Providers:
    provider: Providers = (
        db
        .query(Providers)
        .filter(Providers.id == provider_id)
        .options(joinedload(Providers.aboniments)
                 .joinedload(Aboniments.aboniment_package),
                 joinedload(Providers.aboniment_packages),
                 joinedload(Providers.workout_times),
                 joinedload(Providers.provider_tabs),
                 with_loader_criteria(Aboniments, Aboniments.is_deleted == False),
                 with_loader_criteria(WorkOutTimes, WorkOutTimes.is_deleted == False),
                 with_loader_criteria(AbonimentPackage, AbonimentPackage.is_deleted == False),
                 with_loader_criteria(ProviderTabs, ProviderTabs.is_deleted == False))
        .first()
    )
    if not provider:
        raise ValueError("Not found!")
    return provider
