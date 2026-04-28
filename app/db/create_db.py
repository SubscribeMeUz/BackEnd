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
from app.models.departments.departments import Departments
from sqlalchemy.orm import Session
from app.db.database import SessionLocal


def create_table():
    print("Creating db...")
    Base.metadata.create_all(engine)
    
    # Seed departments data if not exists
    seed_departments()
    
    return "Tables created and data seeded"


def seed_departments():
    session = SessionLocal()
    try:
        # Check if departments already exist
        existing_count = session.query(Departments).count()
        if existing_count > 0:
            print("Departments already seeded")
            return
        
        # Seed data from the migration
        departments_data = [
            {'name': 'Молиявий директор'},
            {'name': 'Юридик департамент'},
            {'name': 'HR ривожланиш департаменти '},
            {'name': 'Комплаенс назорат департаменти  .'},
            {'name': 'Коррупцияга қарши курашиш бошқарма.'},
            {'name': 'Муаммоли кредитлар билан ишлаш департаменти'},
            {'name': 'Ахборот хавфсизлиги департаменти '},
            {'name': 'Банк аппарати департаменти '},
            {'name': 'Мижозлар билан алоқалар маркази '},
            {'name': 'Ғазначилик департаменти'},
            {'name': 'Корпоратив бошқарув хизмати'},
            {'name': 'Риск менежменти департаменти '},
            {'name': 'Кредит Андеррайтинги маркази.'},
            {'name': 'Стратегия ва трансформация маъмусаси'},
            {'name': 'Бизнес ва рақамли маҳсулотлар маъмусаси'},
            {'name': 'Ахборот сиёсати, маънавият ва давлат тили масалалари бўйича маслаҳатчи – Матбуот хизмати'},
            {'name': 'Бизнесни қўллаб-қувватлаш департаменти'},
            {'name': 'Сув ва ижтимоий лойиҳалар маркази'},
            {'name': 'Ҳудудий дастурлар мониторинги бошқармаси'},
            {'name': 'Хорижий ҳамкорлар билан ишлаш департаменти'},
        ]
        
        for dept_data in departments_data:
            dept = Departments(**dept_data)
            session.add(dept)
        
        session.commit()
        print(f"Seeded {len(departments_data)} departments")
        
    except Exception as e:
        session.rollback()
        print(f"Error seeding departments: {e}")
    finally:
        session.close()
