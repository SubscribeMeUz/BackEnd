from pydantic import BaseModel, model_validator, field_serializer
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict
from app.models.providers.providers import Providers
from app.models.aboniments.aboniments import Aboniments
from app.models.packages.packages import AbonimentPackage
from app.models.provider_tabs.provider_tabs import ProviderTabs
from app.models.workouttimes.workout_times import WorkOutTimes
from app.models.purchases.purchases import Purchases


class AbonimentResponse(BaseModel):
    id: int
    name: str
    price: int
    provider_id: int
    workout_time_id: int
    provider_tab_id: int
    aboniment_package_id: int


class MyAbonimentProviderOut(BaseModel):
    id: int
    name: str
    logo_path: str = ''
    logo: str = ''

    @field_serializer('logo')
    def lg(self, x):
        return self.logo_path

    class Config:
        from_attributes = True


class MyPurchasedAbonimentResponse(BaseModel):
    id: int
    name: str
    label: Optional[str]
    title: Optional[str]
    subtitle: Optional[str]
    total_count: int
    aviable_count: int
    expire_date: date
    expiry_days: int
    purchased_date: date
    provider: MyAbonimentProviderOut

    @model_validator(mode='before')
    def f(cls, aboniment: Aboniments):
        aboniment.label = aboniment.aboniment_package.label
        aboniment.title = aboniment.aboniment_package.title
        aboniment.subtitle = aboniment.aboniment_package.subtitle
        aboniment.total_count = aboniment.aboniment_package.count
        aboniment.aviable_count = (
            aboniment.aboniment_package.count - aboniment.purchases.__len__()
        )
        aboniment.expiry_days = aboniment.aboniment_package.expiry_days
        aboniment.expire_date = (aboniment.purchases[0].recorded_date + timedelta(days=aboniment.expiry_days)).date()
        aboniment.purchased_date = aboniment.purchases[0].recorded_date.date()
        return aboniment

    class Config:
        from_attributes = True


ListPurchasedAboniments = List[MyPurchasedAbonimentResponse]


class ProviderTabsLess(BaseModel):
    label: str
    value: str


class AbonimentsWithPackage(BaseModel):
    id: int
    plan_name: str
    label: str
    title: str
    subtitle: str

    @model_validator(mode="before")
    def f(cls, aboniment: Aboniments):
        aboniment.plan_name = aboniment.aboniment_package.plan_name
        aboniment.label = aboniment.aboniment_package.label
        aboniment.title = aboniment.aboniment_package.title
        aboniment.subtitle = aboniment.aboniment_package.subtitle
        return aboniment

    class Config:
        from_attributes = True


class WorkoutTimeWithAboniments(BaseModel):
    title: str
    options: List[AbonimentsWithPackage]


class ProvidersLessResponse(BaseModel):
    id: int
    logo_path: str = ''
    logo: str = ''
    name: str
    title: str = ''

    @field_serializer('logo')
    def fv(self, v):
        return self.logo_path

    @field_serializer('title')
    def ttl(self, v):
        return self.name

    class Config:
        from_attributes = True
        validate_by_name = True


class ProviderAbonimentsResponse(BaseModel):
    id: int
    title: str
    logo_path: str
    logo: str = ''
    tabs: List[ProviderTabsLess]
    plansByTab: Dict[str, List[WorkoutTimeWithAboniments]]

    @field_serializer('logo')
    def fpv_logo(self, f):
        return self.logo_path

    @model_validator(mode="before")
    def f(cls, provider: Providers):
        dc = {}
        for provider_tab in provider.provider_tabs:
            assert isinstance(provider_tab, ProviderTabs)
            tabs = []
            for wk_time in provider.workout_times:
                assert isinstance(wk_time, WorkOutTimes)
                options = []
                for package in provider.aboniment_packages:
                    assert isinstance(package, AbonimentPackage)
                    options += [
                        AbonimentsWithPackage.model_validate(aboniment)
                        for aboniment in provider.aboniments
                        if (
                            aboniment.workout_time_id == wk_time.id
                            and
                            aboniment.provider_tab_id == provider_tab.id
                            and
                            aboniment.aboniment_package_id == package.id
                        )
                    ]
                tabs.append(WorkoutTimeWithAboniments(title=wk_time.title, options=options))
            dc[provider_tab.value] = tabs

        setattr(provider, "plansByTab", dc)
        setattr(provider, "title", provider.name)
        setattr(provider, "tabs", provider.provider_tabs)
        return provider

    class Config:
        from_attributes = True
        validate_by_name = True
