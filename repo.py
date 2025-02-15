from datetime import datetime
from typing import List
from uuid import UUID
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Date, DateTime, Enum, String, create_engine
import enum

class Base(DeprecationWarning): pass

class Status(enum.Enum):
    pending = 'в ожидании'
    in_progress = 'в работе'
    completed = 'выполнено'
    in_not_performed = 'не выполнено'

class StatusUser(enum.Enum):
    admin = 'админ'
    user = 'пользователь'

class OrderBase(Base):
    __tablename__ = 'orders'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    #date: Mapped[Date] = mapped_column()
    #created_date = DateTime(default=datetime.datetime.now())
    date_start: Mapped[datetime] = mapped_column(DateTime)
    date_end: Mapped[datetime] = mapped_column(DateTime)
    equipment: Mapped[str] = mapped_column(String(30))
    problem_type: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(200))
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.pending)
    worker: Mapped[str] = mapped_column(String(30))
    comment: Mapped[list[str]] = mapped_column(String(500))

class ClientBase(Base):
    __tablename__ = 'clients'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    status: Mapped[StatusUser] = mapped_column(Enum(StatusUser), default=StatusUser.user)
