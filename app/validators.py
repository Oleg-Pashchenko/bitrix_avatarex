from pydantic import BaseModel
import re


class NewMessageData(BaseModel):
    bot_id: str = None
    deal_id: int = None
    lead_id: int = None
    dialog_id: str = None
    message: str = None
    application_token: str = None

    @classmethod
    def get_deal_id(cls, data_dict):
        deal_id_part = str(data_dict).split('DEAL|')[1]
        deal_id = ''
        for s in deal_id_part:
            if not s.isdigit():
                break

            deal_id += s
        deal_id = int(deal_id)
        return deal_id

    @classmethod
    def get_lead_id(cls, data_dict):
        return int(str(data_dict).split('LEAD|')[1].split('|')[0])

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            bot_id=next((re.search(r'\[BOT\]\[(\d+)\]', key).group(1) for key in data if
                         '[BOT][' in key and '][BOT_ID]' in key), None),
            deal_id=NewMessageData.get_deal_id(data),
            lead_id=NewMessageData.get_lead_id(data),
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
