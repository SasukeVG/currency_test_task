from fastapi import FastAPI
from db_app.db.database import engine, Base
from db_app.api.router import router as api_router

app = FastAPI()

app.include_router(api_router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()