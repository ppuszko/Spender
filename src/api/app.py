from fastapi import FastAPI


from contextlib import asynccontextmanager
from uuid import UUID

from src.db.main import init_engine, init_sessionmaker
from src.db.models import User
from src.auth.main import get_user_manager, auth_backend, fastapi_users
from src.api.users.schemas import UserRead, UserCreate

@asynccontextmanager 
async def lifespan(app: FastAPI):

    engine = init_engine()
    app.state.engine = engine
    app.state.sessionmaker = init_sessionmaker(engine)

    yield

    await engine.dispose()




app = FastAPI(title="Spender", lifespan=lifespan)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"]
)



