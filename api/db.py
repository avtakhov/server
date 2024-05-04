import os
from functools import lru_cache
from typing import Iterator
from .settings import settings

import sqlalchemy as sqla
from sqlalchemy.orm import Session, declarative_base, sessionmaker

Base = declarative_base()


@lru_cache(maxsize=None)
def get_engine(db_url: str = settings.database_url):
    return sqla.create_engine(db_url, pool_pre_ping=True)


def get_db_session() -> Iterator[Session]:
    session = sessionmaker(bind=get_engine())()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
