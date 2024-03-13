from app.core import database, bitrix
from app.core.bitrix import BitrixAvatarex
from app.validators import *


async def new_message(data: NewMessageData):
    btx_hook = database.get_btx_hook(data.application_token)
    print(btx_hook)
    btx = BitrixAvatarex(webhook=btx_hook)
    deal = await btx.get_deal(data.deal_id)
    pipeline, status = bitrix.get_pipeline_and_status(deal)
    fields_info = await btx.get_all_fields()
    database.add_bitrix_message(data.message, pipeline, status, data.application_token, btx_hook, data.dialog_id,
                                data.bot_id, deal, fields_info)


async def get_lead(data: GetLeadData):
    btx = BitrixAvatarex(webhook=data.rest_hook)
    return await btx.get_lead(data.lead_id)


async def set_field(data: SetFieldData):
    btx = BitrixAvatarex(webhook=data.rest_hook)
    await btx.set_field(data.lead_id, data.field_name, data.filed_value)

async def send_message(data: SendMessageData):
    btx = BitrixAvatarex(webhook=data.rest_hook)
    await btx.send_message(data.dialog_id, data.message, data.bot_id, data.client_id)
    database.set_message_finished(data.message_id)


async def get_account(data: GetInfoData):
    btx = BitrixAvatarex(webhook=data.rest_hook)
    return await btx.get_pipeplines_and_stages()
    return  {'pipelines': btx.get_pipeplines_and_stages(), 'fields': btx.get_all_fields()}


async def create_bot(data: ConnectData):
    btx = BitrixAvatarex(webhook=data.rest_hook)
    cleint_id = await btx.register_bot()
    database.save_setting(cleint_id, data.rest_hook)

