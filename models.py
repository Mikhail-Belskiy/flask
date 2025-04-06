import os
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func
import datetime
import atexit

POSTGRES_USER=os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_HOST=os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT=os.getenv('POSTGRES_PORT', '5431')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD', 'password')
POSTGRES_DB=os.getenv('POSTGRES_DB', 'flask')

PG_DNS = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'


engine = create_engine(PG_DNS)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    @property
    def id_dict(self):
        return {'id': self.id}

class Advert(Base):
    __tablename__ = 'adverts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True) #Id
    title: Mapped[str] = mapped_column(String) #Заголовок
    description: Mapped[str] = mapped_column(String) #Описание
    owner_id: Mapped[str] = mapped_column(String) #Владелец
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now()) #Дата создания

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'owner_id': self.owner_id,
            'date': self.registration_time.isoformat(),
        }

Base.metadata.create_all(bind=engine)

atexit.register(engine.dispose)
