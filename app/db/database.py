from sqlalchemy.orm import declarative_base, Session, with_loader_criteria
from sqlalchemy import create_engine, inspect
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from app.config.config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_PORT


engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
                       query_cache_size=3600,  pool_size=100, max_overflow=10)

Base = declarative_base()


class CustomSession(Session):
    def delete(self, instance):
        if hasattr(instance, "is_deleted"):
            setattr(instance, "is_deleted", True)
            self.add(instance)
        else:
            super().delete(instance)

    def query(self, *entities, **kwargs):
        query_obj = super().query(*entities, **kwargs)

        for model in self._collect_models(entities):
            if hasattr(model, "is_deleted"):
                query_obj = query_obj.options(
                    with_loader_criteria(
                        model, lambda cls: cls.is_deleted == False, include_aliases=False
                    )
                )

        for model in entities:
            if hasattr(model, "is_deleted"):
                query_obj = query_obj.filter(model.is_deleted == False)

        return query_obj

    def _collect_models(self, entities):
        models = set()
        for entity in entities:
            try:
                insp = inspect(entity)
                if insp.is_mapper:
                    models.add(insp.class_)
            except:
                continue
        return models


SessionLocal = sessionmaker(bind=engine, class_=CustomSession)


@contextmanager
def SessionManager():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
