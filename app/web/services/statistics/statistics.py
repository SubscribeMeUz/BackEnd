import logging
from datetime import date
from sqlalchemy import Date, cast, func, extract
from sqlalchemy.orm import Session
from app.web.schemas.statistics import statistics as sc
from app.models.users.users import Users
from app.models.providers.providers import Providers
from app.models.aboniments.aboniments import Aboniments
from app.models.purchases.purchases import Purchases
from app.models.visitation_logs.visitation_logs import VisitationLogs


logger= logging.getLogger(__name__)


# reutrn daily purchases
def get_daily_purchases(
    db: Session,
    provider_id: int = None,
    from_date: date = None,
    to_date: date = None
):
    if not from_date and not to_date:
        today = date.today()
        from_date = today
        to_date = today

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
    if not from_date and not to_date:
        today = date.today()
        from_date = today
        to_date = today

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
    if not from_date and not to_date:
        today = date.today()
        from_date = today
        to_date = today

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


# return uses according to time
def get_uses_with_time(
    db: Session,
    provider_id: int = None,
    from_date: date = None,
    to_date: date = None
):
    if not from_date and not to_date:
        today = date.today()
        from_date = today
        to_date = today

    query = (
        db.query(
            extract('hour', Purchases.recorded_date).label("hour"),
            func.count(Purchases.id).label("total_sales")
        )
        .join(Aboniments, Aboniments.id == Purchases.aboniment_id)
        .join(Providers, Providers.id == Aboniments.provider_id)
        .filter(Purchases.is_deleted == False)
        .filter(Aboniments.is_deleted == False)
        .filter(cast(Purchases.recorded_date, Date) >= from_date)
        .filter(cast(Purchases.recorded_date, Date) <= to_date)
        .group_by(extract('hour', Purchases.recorded_date))
        .order_by("hour")
    )

    if provider_id:
        query = query.filter(Providers.id == provider_id)

    results = query.all()

    hours_map = {i: 0 for i in range(24)}
    for row in results:
        hours_map[int(row.hour)] = row.total_sales

    data = [{"hour": hour, "total_sales": count} for hour, count in sorted(hours_map.items())]

    return data
