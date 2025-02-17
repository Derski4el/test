from datetime import datetime
from typing import List
from sqlalchemy.orm import mapped_column, Mapped, declarative_base
from sqlalchemy import UUID, Date, DateTime, Enum, ForeignKey, String, create_engine
import enum
import uuid

Base = declarative_base()

class Status(enum.Enum):
    pending = 'в ожидании'
    in_progress = 'в работе'
    completed = 'выполнено'
    in_not_performed = 'не выполнено'

class permissionWorkerEnum(enum.Enum):
    in_progress = 'в работе'
    in_rest = 'отдыхает'

class PermissionEnum(enum.Enum):
    admin = 'админ'
    manager = 'менеджер'
    worker = 'работник'
    user = 'пользователь'


class ClientBase(Base):
    __tablename__ = 'clients'

    id: Mapped[UUID] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(30))
    permission: Mapped[PermissionEnum] = mapped_column(Enum(PermissionEnum), default=PermissionEnum.user)


class WorkerBase(ClientBase):
    __tablename__ = 'workers'
    id: Mapped[UUID] = mapped_column(String(36), ForeignKey("clients.id"), primary_key=True)
    status_worker: Mapped[PermissionEnum] = mapped_column(Enum(PermissionEnum), default=PermissionEnum.worker)
    permission: Mapped[permissionWorkerEnum] = mapped_column(Enum(permissionWorkerEnum), default=permissionWorkerEnum.in_rest)

class ManagerBase(ClientBase):
    __tablename__ = 'managers'
    id: Mapped[UUID] = mapped_column(String(36), ForeignKey("clients.id"), primary_key=True)
    permission: Mapped[PermissionEnum] = mapped_column(Enum(PermissionEnum), default=PermissionEnum.manager)

class AdminBase(ClientBase):
    __tablename__ = 'admins'
    id: Mapped[UUID] = mapped_column(String(36), ForeignKey("clients.id"), primary_key=True)
    permission: Mapped[PermissionEnum] = mapped_column(Enum(PermissionEnum), default=PermissionEnum.admin)

class OrderBase(Base):
    __tablename__ = 'orders'

    id: Mapped[UUID] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    date_start: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    date_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    equipment: Mapped[str] = mapped_column(String(30), nullable=False)
    problem_type: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.pending, nullable=False)
    worker: Mapped[str] = mapped_column(String(30), default='Не назначен')
    comment: Mapped[list[str]] = mapped_column(String(500), default=[])

if __name__ == '__main__':
    engine = create_engine('sqlite:///database.db', echo=True)
    Base.metadata.create_all(engine)
    print("База данных успешно создана!")
