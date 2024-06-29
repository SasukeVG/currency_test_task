from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db_app.api.schema import CurrencyCreate
from db_app.crud.crud_ops import get_all_currencies, get_currency_by_char_code
from db_app.db.database import get_db
from db_app.domain.inference import update_currency_rates

router = APIRouter(
    prefix="/currencies",
    tags=["currencies"],
)


@router.post("/manual_update")
async def manual_update():
    try:
        await update_currency_rates()
        return {"message": "Currency rates updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/currencies/")
async def read_currencies(db: AsyncSession = Depends(get_db)):
    currencies = await get_all_currencies(db)
    return currencies


@router.post("/update_currency/")
async def update_currency(currency: CurrencyCreate, db: AsyncSession = Depends(get_db)):
    updated_currency = await update_currency(db, currency.char_code, currency.name, currency.value, currency.unit_rate)
    return updated_currency


@router.get("/currency/{char_code}")
async def read_currency(char_code: str, db: AsyncSession = Depends(get_db)):
    currency = await get_currency_by_char_code(db, char_code)
    if currency is None:
        raise HTTPException(status_code=404, detail="Currency not found")
    return currency