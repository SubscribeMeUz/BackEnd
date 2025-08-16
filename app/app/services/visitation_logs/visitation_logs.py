import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload, contains_eager, query
from app.models.purchases import purchases
from app.models.users.users import Users
from app.models.visitation_logs.visitation_logs import VisitationLogs
from app.models.purchases.purchases import Purchases
from app.models.aboniments.aboniments import Aboniments
from app.models.providers.providers import Providers
from app.models.packages.packages import AbonimentPackage
from app.app.schemas.visitation_logs import visitation_logs as sc
from app.web.schemas.purchases import purchases as web_purchases_sc


logger = logging.getLogger(__name__)


def check_purchase_is_valid(db: Session, user: Users, provider_id: int, aboniment_id: int):
    return _check_purchase_is_valid(db=db, user=user, provider_id=provider_id, aboniment_id=aboniment_id)


def _check_purchase_is_valid(db: Session, user: Users, provider_id: int, aboniment_id: int):
    if aboniment_id:
        purchase = (
            db
            .query(Purchases)
            .filter(Purchases.status == web_purchases_sc.PurchasesStatuses.NEW)
            .filter(Purchases.aboniment_id == aboniment_id)
            .filter(Purchases.user_id == user.id)
            .order_by(Purchases.recorded_date.desc())
            .first()
        )
    else:
        purchase = (
            db
            .query(Purchases)
            .join(Purchases.aboniment)
            .filter(Purchases.status == web_purchases_sc.PurchasesStatuses.NEW)
            .filter(Aboniments.provider_id == provider_id)
            .filter(Purchases.user_id == user.id)
            .order_by(Purchases.recorded_date.desc())
            .first()
        )
    if not purchase:
        raise ValueError("Sizda ushbu provayderda aktiv aboniment mavjud emas!")
   # if we have purchase it means that we can calculate the info
    package = (
        db
        .query(AbonimentPackage)
        .join(AbonimentPackage.aboniments)
        .filter(Aboniments.id == purchase.aboniment_id)
        .first()
    )
    # from abonoment package we can take info like expire day and others
    date_now = datetime.now() # get current date 
    expire_date = purchase.recorded_date + timedelta(days=package.expiry_days)  # take when it is going to expire
    logs = (
        db
        .query(VisitationLogs)
        .filter(VisitationLogs.user_id == user.id,
                VisitationLogs.purchase_id == purchase.id)
        .order_by(VisitationLogs.recorded_date.desc())
    )
    visitation_count = logs.count()
    last_visitation = logs.first()
    # if last_visitation and (last_visitation.recorded_date >= datetime.now() - timedelta(hours=1)):
    #     raise ValueError("Bir soat ichida bir nechta joydan foydalanish mumkin emas!")
    if visitation_count >= package.count:
        purchase.status = web_purchases_sc.PurchasesStatuses.USED
        try:
            db.add(purchase)
            db.commit()
        except:
            db.rollback()
        raise ValueError("Abonimentdan foydalanish limiti tugagan!")
    # if expire_date.date() == date_now.date():
    #     raise ValueError("Bir kun ichida abonimentdan faqat bir marta foydalanish mumkin!")
    if expire_date < date_now:
        purchase.status = web_purchases_sc.PurchasesStatuses.USED
        try:
            db.add(purchase)
            db.commit()
        except:
            db.rollback()
        raise ValueError("Aboniment uchun foydalanish muddati tugagan!")
    return purchase

def _get_valid_purchase(db: Session, user: Users, provider_id: int, aboniment_id: int):
        if not provider_id or not aboniment_id:
            raise ValueError("Provider ID va Abonoment ID berilishi shart!")
        
        abonoment = db.query(Aboniments).filter(Aboniments.id == aboniment_id).first()
        if not abonoment:
            raise ValueError("Aboniment topilmadi!")
        if abonoment.provider_id != provider_id:
            raise ValueError("Aboniment provayderi bilan mos kelmaydi!")
        # get abonoment package to calculate the info
        aboniment_pacakage = (
            db.query(AbonimentPackage)
            .join(AbonimentPackage.aboniments)
            .filter(Aboniments.id == aboniment_id)
            .first()
        )

        if not aboniment_pacakage:
            raise ValueError("Aboniment paketi topilmadi!")
        
        # check if user has a valid purchase
        print(user.id, aboniment_id, "tets")
        query = (
            db.query(Purchases)
            .filter(Purchases.status == web_purchases_sc.PurchasesStatuses.NEW)
            .filter(Purchases.user_id == user.id)
            .filter(Purchases.aboniment_id == aboniment_id)
            .order_by(Purchases.recorded_date.asc())
            .all()
        )
        print(len(query), "query count test")
        if not query:
            raise ValueError("Sizda ushbu provayderda aktiv aboniment mavjud emas!")
        
        user_purchase: Purchases| None = None
        for purchase in query:
            if purchase.recorded_date + timedelta(days=aboniment_pacakage.expiry_days) < datetime.now():
                purchase.status = web_purchases_sc.PurchasesStatuses.USED
                try:
                    db.add(purchase)
                    db.commit()
                except:
                    db.rollback()
                    raise ValueError("Aboniment uchun foydalanish muddati tugagan!")
                continue
            if purchase.used_count >= aboniment_pacakage.count:
                purchase.status = web_purchases_sc.PurchasesStatuses.USED
                try:
                    db.add(purchase)
                    db.commit()
                except:
                    db.rollback()
                    raise ValueError("Abonimentdan foydalanish limiti tugagan!")
                continue

            user_purchase = purchase
            break
        if not user_purchase:
            raise ValueError("Sizda ushbu provayderda aktiv aboniment mavjud emas!")
        # if we have purchase it means that we can calculate the info
        
                
        logs = (
            db
            .query(VisitationLogs)
            .filter(VisitationLogs.user_id == user.id,
                    VisitationLogs.purchase_id == purchase.id)
            .order_by(VisitationLogs.recorded_date.desc())
        )
        last_visitation = logs.first()
        # if last_visitation and (last_visitation.recorded_date >= datetime.now() - timedelta(hours=1)):
        #     raise ValueError("Bir soat ichida bir nechta joydan foydalanish mumkin emas!")
        

        return user_purchase
    

def get_user_visitation_log(db: Session, log_id: int):
    return _get_user_visitation_log(db=db, log_id=log_id)


def _get_user_visitation_log(db: Session, log_id: int):
    resp = (
        db
        .query(VisitationLogs)
        .options(joinedload(VisitationLogs.user),
                 joinedload(VisitationLogs.purchase)
                 .joinedload(Purchases.aboniment)
                 .options(joinedload(Aboniments.provider),
                          joinedload(Aboniments.aboniment_package),
                          joinedload(Aboniments.workout_time),
                          joinedload(Aboniments.provider_tab)))
        .filter(VisitationLogs.id == log_id,
                VisitationLogs.is_deleted == False)
        .first()
    )
    if not resp:
        raise ValueError("VisitationLog not found!")
    return resp


def get_user_visitations(db: Session, user: Users,
                         aboniment_id: int = None,
                         provider_id: int = None):
    query = (
        db.query(Providers)
        .join(Providers.aboniments)
        .join(Aboniments.purchases)
        .join(Purchases.visitation_logs)
        .join(Aboniments.workout_time)
        .join(Aboniments.provider_tab)
        .join(Aboniments.aboniment_package)
        .filter(VisitationLogs.user_id == user.id)
    )

    if aboniment_id:
        query = query.filter(Aboniments.id == aboniment_id)

    if provider_id:
        query = query.filter(Providers.id == provider_id)

    query = query.options(
        contains_eager(Providers.aboniments)
        .options(contains_eager(Aboniments.provider_tab),
                 contains_eager(Aboniments.aboniment_package),
                 contains_eager(Aboniments.workout_time),
                 contains_eager(Aboniments.purchases)
                 .contains_eager(Purchases.visitation_logs))
    )

    providers = query.distinct(Providers.id).all()
    return providers


def add_visitation_log(db: Session, request: sc.VisitationLogAddRequest, user: Users):
    provider = db.query(Providers).filter(Providers.id == request.provider_id).first()
    if not provider:
        raise ValueError("Provider not found")

    purchase: Purchases = _get_valid_purchase(db=db, user=user,
                                                  provider_id=request.provider_id,
                                                  aboniment_id=request.aboniment_id)

   # used_count = db.query(VisitationLogs).filter(VisitationLogs.user_id == user.id).count()
    new_log = VisitationLogs(
        user_id = user.id,
        purchase_id = purchase.id
    )
    purchase.used_count = purchase.used_count + 1
    try:
        db.add(new_log)
        db.add(purchase)
        db.commit()
        db.refresh(new_log)
    except Exception as err:
        db.rollback()
        raise err

    return {
        "result":"Ok",
        "log": _get_user_visitation_log(db=db, log_id=new_log.id)
    }


def delete_log(db: Session, log_id: int):
    try:
        resp = db.query(VisitationLogs).filter(VisitationLogs.id == log_id).first()
        db.delete(resp)
        db.commit()
        return {'result': 'deleted!'}
    except Exception as err:
        logger.error(err)
        db.rollback()
        raise err

# code refactoring qilish kerak 
def mark_as_used(db, purchase, message: str):
    purchase.status = web_purchases_sc.PurchasesStatuses.USED
    try:
        db.add(purchase)
        db.commit()
    except:
        db.rollback()
        raise ValueError(message)