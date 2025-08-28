import logging
from datetime import date
from sqlalchemy import Date, cast, func, extract
from sqlalchemy.orm import Session
from typing import List

from app.web.schemas.statistics import statistics as sc
from app.models.users.users import Users
from app.models.providers.providers import Providers
from app.models.aboniments.aboniments import Aboniments
from app.models.packages.packages import AbonimentPackage
from app.models.purchases.purchases import Purchases
from app.models.visitation_logs.visitation_logs import VisitationLogs
from app.models.provider_tabs.provider_tabs import ProviderTabs


logger= logging.getLogger(__name__)


# reutrn daily purchases
def get_daily_purchases(
    db: Session,
    provider_id: int = None,
    from_date: date = None,
    to_date: date = None
):
    from_date = date.today() if not from_date else from_date
    to_date = date.today() if not to_date else to_date

    query = (
        db.query(
            Providers.id.label("provider_id"),
            Providers.name.label("provider_name"),
            Aboniments.id.label("aboniment_id"),
            Aboniments.name.label("aboniment_name"),
            cast(Purchases.recorded_date, Date).label("purchase_date"),
            func.count(Purchases.id).label("total_sales")
        )
        .join(Aboniments, Aboniments.provider_id == Providers.id)
        .join(Purchases, Purchases.aboniment_id == Aboniments.id)
        .filter(Purchases.is_deleted == False)
        .filter(Aboniments.is_deleted == False)
        .filter(cast(Purchases.recorded_date, Date) >= from_date)
        .filter(cast(Purchases.recorded_date, Date) <= to_date)
        .group_by(
            Providers.id,
            Providers.name,
            Aboniments.id,
            Aboniments.name,
            cast(Purchases.recorded_date, Date)
        )
        .order_by(Providers.id, Aboniments.id, cast(Purchases.recorded_date, Date))
    )

    if provider_id:
        query = query.filter(Providers.id == provider_id)

    results = query.all()

    data = []
    for row in results:
        data.append({
            "provider_id": row.provider_id,
            "provider_name": row.provider_name,
            "aboniment_id": row.aboniment_id,
            "aboniment_name": row.aboniment_name,
            "date": row.purchase_date.isoformat(),
            "total_sales": row.total_sales
        })

    return data


# return active abonoments
def get_active_aboniments(
    db: Session,
    provider_id: int = None,
    from_date: date = None,
    to_date: date = None
):
    from_date = date.today() if not from_date else from_date
    to_date = date.today() if not to_date else to_date

    

    query = (
        db.query(
            Providers.id.label("provider_id"),
            Providers.name.label("provider_name"),
            Aboniments.id.label("aboniment_id"),
            Aboniments.name.label("aboniment_name"),
            func.count(Purchases.id).label("active_count")
        )
        .join(Aboniments, Aboniments.provider_id == Providers.id)
        .join(Purchases, Purchases.aboniment_id == Aboniments.id)
        .filter(Purchases.is_deleted == False)
        .filter(Aboniments.is_deleted == False)
        .filter(Purchases.used_count != 0)
        .filter(cast(Purchases.recorded_date, Date) >= from_date)
        .filter(cast(Purchases.recorded_date, Date) <= to_date)
        .group_by(
            Providers.id,
            Providers.name,
            Aboniments.id,
            Aboniments.name
        )
        .order_by(Providers.id, Aboniments.id)
    )

    if provider_id:
        query = query.filter(Providers.id == provider_id)
    

    results = query.all()

    data = []
    for row in results:
        data.append({
            "provider_id": row.provider_id,
            "provider_name": row.provider_name,
            "aboniment_id": row.aboniment_id,
            "aboniment_name": row.aboniment_name,
            "active_count": row.active_count
        })

    return data


# return all abanoments with statuses
def get_all_aboniments():
    return


# return which abonement how many purchases kinda finding most purchased abonoemtns
def get_abonoment_purchases():
    return


# return which user comes to use abonoments
def get_user_aboniment_uses(
    db: Session,
    provider_id: int = None,
    from_date: date = None,
    to_date: date = None
):
    from_date = date.today() if not from_date else from_date
    to_date = date.today() if not to_date else to_date

    query = (
        db.query(
            cast(Purchases.recorded_date, Date).label("purchase_date"),
            Providers.id.label("provider_id"),
            Providers.name.label("provider_name"),
            Aboniments.id.label("aboniment_id"),
            Aboniments.name.label("aboniment_name"),
            Users.id.label("user_id"),
            Users.full_name,
            Users.phone
        )
        .join(Aboniments, Aboniments.id == Purchases.aboniment_id)
        .join(Providers, Providers.id == Aboniments.provider_id)
        .join(Users, Users.id == Purchases.user_id)
        .filter(Purchases.is_deleted == False)
        .filter(Aboniments.is_deleted == False)
        .filter(Users.is_deleted == False)
        .filter(cast(Purchases.recorded_date, Date) >= from_date)
        .filter(cast(Purchases.recorded_date, Date) <= to_date)
        .order_by("purchase_date", "provider_id", "aboniment_id", "user_id")
    )

    if provider_id:
        query = query.filter(Providers.id == provider_id)

    results = query.all()

    # Nested JSON: sana → provider → aboniment → foydalanuvchilar
    data = {}
    for row in results:
        day = row.purchase_date.isoformat()
        if day not in data:
            data[day] = {}

        if row.provider_id not in data[day]:
            data[day][row.provider_id] = {
                "provider_name": row.provider_name,
                "aboniments": {}
            }

        if row.aboniment_id not in data[day][row.provider_id]["aboniments"]:
            data[day][row.provider_id]["aboniments"][row.aboniment_id] = {
                "aboniment_name": row.aboniment_name,
                "users": []
            }

        data[day][row.provider_id]["aboniments"][row.aboniment_id]["users"].append({
            "user_id": row.user_id,
            "full_name": row.full_name,
            "phone": row.phone
        })

    # JSON-friendly list
    formatted = []
    for day, providers in data.items():
        formatted.append({
            "date": day,
            "providers": [
                {
                    "provider_id": pid,
                    "provider_name": pdata["provider_name"],
                    "aboniments": [
                        {
                            "aboniment_id": aid,
                            "aboniment_name": adata["aboniment_name"],
                            "users": adata["users"]
                        }
                        for aid, adata in pdata["aboniments"].items()
                    ]
                }
                for pid, pdata in providers.items()
            ]
        })

    return formatted

# bug fix
# return uses according to time
def get_uses_with_time(
    db: Session,
    provider_id: int = None,
    from_date: date = None,
    to_date: date = None,
    interval_hours : int = 1,
    query: str = None,
    abonoment_id: int = None,
    user: Users = None
):
    from_date = date.today() if not from_date else from_date
    to_date = date.today() if not to_date else to_date

    query_ = (
        db.query(
            extract('hour', Purchases.recorded_date).label("hour"),
            func.count(Purchases.id).label("total_sales")
        )
        .join(Aboniments, Aboniments.id == Purchases.aboniment_id)
        .join(Aboniments.aboniment_package)
        .join(Aboniments.provider_tab)
        .join(Providers, Providers.id == Aboniments.provider_id)
        .filter(Purchases.is_deleted == False)
        .filter(Aboniments.is_deleted == False)
        .filter(Providers.owner_id == user.id)
        .filter(cast(Purchases.recorded_date, Date) >= from_date)
        .filter(cast(Purchases.recorded_date, Date) <= to_date)
        .group_by(extract('hour', Purchases.recorded_date))
        .order_by("hour")
    )

    if provider_id:
        query_ = query_.filter(Providers.id == provider_id)
    if abonoment_id:
        query_ = query_.filter(Aboniments.id == abonoment_id)
    if query:
        query_ = query_.filter(Aboniments.name.ilike(f"%{query}%") |
                               Users.full_name.ilike(f"%{query}%") |
                               Users.phone.ilike(f"%{query}%") |
                               AbonimentPackage.title.ilike(f"%{query}%") |
                               AbonimentPackage.plan_name.ilike(f"%{query}%") |
                               ProviderTabs.label.ilike(f"%{query}%") |
                               ProviderTabs.value.ilike(f"%{query}%"))


    results = query_.all()
    
    hours_map = {i: 0 for i in range(24//interval_hours)}
    for row in results:
        hours_map[int(row.hour)//interval_hours] += row.total_sales

    data = [{"hour": f"{hour * interval_hours}-{(hour+1) * interval_hours}", "total_sales": count} for hour, count in sorted(hours_map.items())]

    return data

# get statistics about accepted and rejected requests from admin

# return user list which uses abonoments 
def get_user_list_by_usetimes(db: Session, user_request: sc.UserAbonimentUseRequest, user: Users)-> List[sc.UserAbonimentUseResponse]:

    query = (db.query(func.date_trunc('second', VisitationLogs.recorded_date).label("use_date"),
                      Aboniments.id.label("aboniment_id"),
                      Aboniments.name.label("aboniment_name"),
                      Users.id.label("user_id"),
                      Users.full_name,
                      Users.phone,
                      Providers.id.label("provider_id"),
                      Providers.name.label("provider_name"),
                      ).join(Purchases, Purchases.id == VisitationLogs.purchase_id)
                      .join(Aboniments, Aboniments.id == Purchases.aboniment_id)
                      .join(Providers, Providers.id == Aboniments.provider_id)
                      .join(Users, Users.id == Purchases.user_id)).where(Providers.owner_id == user.id).order_by(cast(VisitationLogs.recorded_date, Date).desc())
   
    if user_request.from_date:
        query = query.filter(cast(VisitationLogs.recorded_date, Date) >= user_request.from_date)
    if user_request.to_date:
        query = query.filter(cast(VisitationLogs.recorded_date, Date) <= user_request.to_date)
    if user_request.provider_id:
        query = query.filter(Providers.id == user_request.provider_id)
    if user_request.aboniment_id:
        query = query.filter(Aboniments.id == user_request.aboniment_id)
    if user_request.phone:
        query = query.filter(Users.phone == user_request.phone)
    if user_request.name:
        query = query.filter(Users.full_name.ilike(f"%{user_request.name}%"))
    
    results = query.all()
    
    return [sc.UserAbonimentUseResponse(**row._mapping) for row in results]

# return purchase history as list
def get_purchase_history(db: Session, purchase_request: sc.PurchaseHistoryRequest, user: Users) -> List[sc.PurchaseHistoryResponse]:

    query = (db.query(Purchases.id.label("purchase_id"),
                        Users.id.label("user_id"),
                        Users.full_name.label("user_name"),
                        Users.phone.label("user_phone"),
                        Providers.id.label("provider_id"),
                        Providers.name.label("provider_name"),
                        Aboniments.id.label("aboniment_id"),
                        Aboniments.name.label("aboniment_name"),
                        Aboniments.price.label("aboniment_price"),
                        AbonimentPackage.count.label("total_amount"),
                        AbonimentPackage.plan_name.label("abonoment_name"),

                       func.date_trunc('second', Purchases.recorded_date).label("purchase_date"),
                        ).join(Aboniments, Aboniments.id == Purchases.aboniment_id)
                        .join(Providers, Providers.id == Aboniments.provider_id)
                        .join(Users, Users.id == Purchases.user_id)
                        .join(AbonimentPackage, AbonimentPackage.id == Aboniments.aboniment_package_id)
                        .where(Providers.owner_id == user.id).order_by(cast(Purchases.recorded_date, Date).desc()))
  
    if purchase_request.from_date:
        query = query.filter(cast(Purchases.recorded_date, Date)>= purchase_request.from_date)
    if purchase_request.to_date:
        query = query.filter(cast(Purchases.recorded_date, Date) <= purchase_request.to_date)
    if purchase_request.abonoment_id:
        query = query.filter(Aboniments.id == purchase_request.abonoment_id)
    if purchase_request.phone:
        query = query.filter(Users.phone == purchase_request.phone)
    if purchase_request.name:
        query = query.filter(Users.full_name.ilike(f"%{purchase_request.name}%"))
                        
                      
    result = query.all()
    return [sc.PurchaseHistoryResponse(**row._mapping) for row in result]

# get full client info 
def get_client_info(
    db: Session, 
    client_info_request: sc.ClientInfoRequest, 
    user: Users
) -> List[sc.ClientInfoResponse]:
    query = (
        db.query(
            Purchases.user_id.label("user_id"),
            Users.full_name.label("full_name"),
            Users.phone.label("phone_number"),
            func.count(Purchases.id).label("purchase_count"),
            func.max(Purchases.recorded_date).label("last_purchase_date")
        )
        .join(Purchases.aboniment)
        .join(Aboniments.provider)
        .join(Users, Purchases.user_id == Users.id)
        .where(Providers.owner_id == user.id)
        .group_by(Purchases.user_id,
                  Users.full_name,
                  Users.phone)
    )
    
    if client_info_request.name:
        query = query.filter(Users.full_name.ilike(f"%{client_info_request.name}%"))
    if client_info_request.phone:
        query = query.filter(Users.phone == client_info_request.phone)
    if client_info_request.min_count:
        query = query.having(func.count(Purchases.id) >= client_info_request.min_count)
    if client_info_request.max_count:
        query = query.having(func.count(Purchases.id) <= client_info_request.max_count)
    if client_info_request.from_date:
        query = query.having(func.max(Purchases.recorded_date) >= client_info_request.from_date)
    if client_info_request.to_date:
        query = query.having(func.max(Purchases.recorded_date) <= client_info_request.to_date)
    
    results = query.all() or []  # ensure results is always a list

    return [sc.ClientInfoResponse(**row._mapping) for row in results]
