from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db_app.db.models import Currency


async def get_all_currencies(db: AsyncSession):
    result = await db.execute(select(Currency))
    return result.scalars().all()


async def create_currency(db: AsyncSession, num_code: str, char_code: str, nominal: int, name: str, value: float, unit_rate: float):
    db_currency = Currency(num_code=num_code, char_code=char_code, nominal=nominal, name=name, value=value, unit_rate=unit_rate)
    db.add(db_currency)
    await db.commit()
    await db.refresh(db_currency)
    return db_currency


async def update_currency(db: AsyncSession, char_code: str, name: str, value: float, unit_rate: float):
    result = await db.execute(select(Currency).where(Currency.char_code == char_code))
    db_currency = result.scalars().first()
    if db_currency:
        db_currency.name = name
        db_currency.value = value
        db_currency.unit_rate = unit_rate
        await db.flush()
        await db.refresh(db_currency)  # Ensure the currency object is refreshed before commit
        await db.commit()
    else:
        db_currency = Currency(char_code=char_code, name=name, value=value, unit_rate=unit_rate)
        db.add(db_currency)
        await db.flush()
        await db.refresh(db_currency)  # Ensure the currency object is refreshed before commit
        await db.commit()
    return db_currency


async def get_currency_by_char_code(db: AsyncSession, char_code: str):
    result = await db.execute(select(Currency).where(Currency.char_code == char_code))
    currency = result.scalars().first()
    return currency