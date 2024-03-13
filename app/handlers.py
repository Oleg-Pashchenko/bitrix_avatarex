from app.core import methods
from app.decorators import request_processing
from app.validators import *


@request_processing
async def new_message_handler(data: dict):
    print('yes')
    print(data)
    data = NewMessageData.from_dict(data)
    print(data)
    return await methods.new_message(data)


@request_processing
async def send_message_handler(data: dict):
    data = SendMessageData(**data)
    return await methods.send_message(data)


@request_processing
async def get_info_handler(data: dict):
    data = GetInfoData(**data)
    return await methods.get_account(data)


@request_processing
async def connect_handler(data: dict):
    data = ConnectData(**data)
    # Удалить все существующие интеграции Avatarex из нашей базы и Bitrix
    return await methods.create_bot(data)


@request_processing
async def get_lead_handler(data: dict):
    data = GetLeadData(**data)
    return await methods.get_lead(data)


@request_processing
async def set_field_handler(data: dict):
    data = SetFieldData(**data)
    return await methods.set_field(data)
