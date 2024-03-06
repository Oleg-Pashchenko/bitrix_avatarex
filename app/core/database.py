import datetime
import time

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, DateTime, BigInteger, Boolean
from sqlalchemy.orm import sessionmaker
import dotenv
import os

dotenv.load_dotenv()
Base = declarative_base()


class Bitrix_Message(Base):
    __tablename__ = 'bitrix_messages'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    date = Column(DateTime, default=datetime.datetime.now())
    pipeline_id = Column(BigInteger)
    status_id = Column(String)
    app_id = Column(Integer)
    rest_hook = Column(String)
    is_started = Column(Boolean, default=False)
    is_finished = Column(Boolean, default=False)
    dialog_id = Column(String)
    bot_id = Column(Integer)


class Bitrix_Setting(Base):
    __tablename__ = "bitrix_settings"
    id = Column(Integer, primary_key=True)
    btx_hook = Column(String)
    app_id = Column(Integer)


engine = create_engine(
    f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}'
    f'@{os.getenv("DB_HOST")}:5432/{os.getenv("DB_NAME")}',
    pool_pre_ping=True,
)

Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


def save(obj):
    while True:
        try:
            session.add(obj)
            session.commit()
            break
        except OperationalError:
            session.rollback()
            time.sleep(10)


def add_bitrix_message(text, pipeline_id, status_id, app_id, rest_hook, dialog_id, bot_id):
    new_message = Bitrix_Message(
        text=text,
        pipeline_id=pipeline_id,
        status_id=status_id,
        app_id=app_id,
        rest_hook=rest_hook,
        dialog_id=dialog_id,
        bot_id=bot_id
    )
    save(new_message)


def get_btx_hook(app_id):
    setting = session.query(Bitrix_Setting).filter(Bitrix_Setting.app_id == app_id).first()
    return setting.btx_hook if setting else None


def set_message_finished(message_id):
    message = session.query(Bitrix_Message).filter(Bitrix_Message.id == message_id).first()
    if message:
        message.is_finished = True
        session.commit()


def save_setting(client_id, rest_hook):
    save(Bitrix_Setting(btx_hook=rest_hook, app_id=client_id))
