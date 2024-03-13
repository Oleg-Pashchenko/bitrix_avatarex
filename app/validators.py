from pydantic import BaseModel
import re


class NewMessageData(BaseModel):
    bot_id: str = None
    deal_id: str = None
    dialog_id: str = None
    message: str = None
    application_token: str = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            bot_id=next((re.search(r'\[BOT\]\[(\d+)\]', key).group(1) for key in data if
                         '[BOT][' in key and '][BOT_ID]' in key), None),
            deal_id = int(''.join(c for c in str(data).split('DEAL|', 1)[-1] if c.isdigit())),
            dialog_id=data['data[PARAMS][DIALOG_ID]'],
            message=data['data[PARAMS][MESSAGE]'],
            application_token=data['auth[application_token]']
        )


class SendMessageData(BaseModel):
    dialog_id: str
    message: str
    bot_id: str
    client_id: str
    message_id: str
    rest_hook: str


class GetInfoData(BaseModel):
    rest_hook: str


class ConnectData(BaseModel):
    rest_hook: str


class GetLeadData(BaseModel):
    rest_hook: str
    lead_id: int


class SetFieldData(BaseModel):
    rest_hook: str
    lead_id: int
    field_name: str
    filed_value: str
