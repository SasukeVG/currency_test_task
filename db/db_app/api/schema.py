from pydantic import BaseModel


class CurrencyBase(BaseModel):
    char_code: str
    name: str
    value: float
    unit_rate: float


class CurrencyCreate(CurrencyBase):
    pass


class Currency(CurrencyBase):
    id: int

    class Config:
        orm_mode = True
