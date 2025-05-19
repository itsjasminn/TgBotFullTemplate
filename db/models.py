from sqlalchemy import BigInteger, String, select, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from db import Base, db
from db.utils import CreatedModel


class User(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(56), nullable=True)

    @classmethod
    async def get_ids(cls):
        query = select(cls.id)
        results = await db.execute(query)
        ids = [result.id for result in results]
        return ids

    @classmethod
    async def exists_user(cls, id_):
        query = select(cls.id).where(cls.id == id_)
        result = await db.execute(query)
        return result.first() is not None


class Controller(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    @classmethod
    async def exists_admin(cls, id_):
        query = select(cls.id).where(cls.id == id_)
        result = await db.execute(query)
        return result.first() is not None


class Social(CreatedModel):
    url: Mapped[str] = mapped_column(String(255), unique=True)

    @classmethod
    async def get_all_url(cls):
        query = select(cls)
        results = await db.execute(query)
        return results.scalars().all()



class Group(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=True)
    force: Mapped[bool] = mapped_column(Boolean, default=True)

    @classmethod
    async def get_group_ids(cls):
        query = select(cls.id).where(cls.force == True)
        results = await db.execute(query)
        ids = [result[0] for result in results.all()]
        return ids

    @classmethod
    async def get_all_column(cls):
        query = select(cls).where(cls.force == True)
        results = await db.execute(query)
        return results.scalars().all()

metadata = Base.metadata
