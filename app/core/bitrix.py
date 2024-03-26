import asyncio
import random

from fast_bitrix24 import Bitrix


class BitrixAvatarex:
    def __init__(self, webhook: str):
        self.bitrix: Bitrix = Bitrix(webhook, verbose=False)

    async def get_deal(self, deal_id):
        response = await self.bitrix.call(method='crm.deal.get', items={
            'id': deal_id
        })
        return response

    async def get_lead(self, lead_id):
        response = await self.bitrix.call(method='crm.lead.get', items={
            'id': lead_id
        })
        return response

    async def send_message(self, dialog_id, message, bot_id, client_id):
        await self.bitrix.call(
            'imbot.message.add',
            items={
                'BOT_ID': bot_id,
                'DIALOG_ID': dialog_id,
                'CLIENT_ID': client_id,
                'MESSAGE': message
            }
        )

    async def set_field(self, deal_id, field_id, field_value):
        response = await self.bitrix.call(method='crm.lead.update', items={
            'id': deal_id,
            'fields': {
                field_id: field_value
            }
        })
        print(response)

    async def register_bot(self):
        client_id = random.randint(1, 10000000)
        response = await self.bitrix.call(
            'imbot.register',
            items={
                'CODE': 'Avatarex AI Assistant',
                'TYPE': 'S',
                'CLIENT_ID': client_id,
                'EVENT_HANDLER': 'http://bitrix.avatarex.tech/',
                'OPENLINE': 'Y',
                'PROPERTIES': {
                    'NAME': "Avatarex AI Assistant",
                    'LAST_NAME': "",
                    "COLOR": "PURPLE",
                    'EMAIL': "odpash.itmo@gmail.com",
                    "PERSONAL_BIRTHDAY": '2003-12-23',
                    'WORK_POSITION': "Avatarex AI - assistant",
                }
            }
        )
        print(response)
        return client_id

    async def get_pipeplines_and_stages(self):
        try:
            pipelines = await self.bitrix.get_all(method='crm.category.list', params={'entityTypeId': 2})
            return {
                pipeline['id']: {
                    'name': pipeline['name'],
                    'id': pipeline['id'],
                    'stages': {
                        stage['STATUS_ID']: {
                            'name': stage['NAME'],
                            'id': stage['STATUS_ID']
                        } for stage in
                        await self.bitrix.get_all(method='crm.dealcategory.stage.list', params={'id': pipeline['id']})
                    }
                } for pipeline in pipelines
            }
        except:
            return {}

    async def get_all_fields(self):
        fields = await self.bitrix.call(method='crm.lead.fields', items={
            'order': {
                'ID': 'desc'
            }
        })
        answer = {}
        for f in fields.keys():
            if 'UF_CRM_' in f:
                try:
                    answer[fields[f]['listLabel']] = {'code': fields[f]['title'],
                                                      'enum': fields[f]['items']
                                                      }
                except:
                    pass
        return answer


def get_pipeline_and_status(deal):
    status = deal.get('STAGE_ID', 'NEW')
    pipeline = 0 if status == 'NEW' else int(status.split(':')[0].replace('C', ''))
    return pipeline, status


async def main():
    deals_wh = 'https://b24-5r9tse.bitrix24.ru/rest/1/51suk4hoa3ksawbp/'
    leads_wh = 'https://b24-1x2ywp.bitrix24.ru/rest/1/2m3yqqnu2etjcjrt/'
    b = BitrixAvatarex(webhook=leads_wh)
    response = await b.get_lead(3)
    print(response)


data = {'event': 'ONIMBOTMESSAGEADD', 'data[BOT][11][BOT_ID]': '11', 'data[BOT][11][BOT_CODE]': 'Avatarex AI Assistant',
        'data[PARAMS][FROM_USER_ID]': '13', 'data[PARAMS][MESSAGE]': 'hahahahaha', 'data[PARAMS][TO_CHAT_ID]': '5',
        'data[PARAMS][MESSAGE_TYPE]': 'L', 'data[PARAMS][SYSTEM]': 'N', 'data[PARAMS][SKIP_URL_INDEX]': 'N',
        'data[PARAMS][SKIP_COUNTER_INCREMENTS]': 'N', 'data[PARAMS][SKIP_COMMAND]': 'N',
        'data[PARAMS][SKIP_CONNECTOR]': 'N', 'data[PARAMS][IMPORTANT_CONNECTOR]': 'N',
        'data[PARAMS][SILENT_CONNECTOR]': 'N', 'data[PARAMS][AUTHOR_ID]': '13', 'data[PARAMS][CHAT_ID]': '5',
        'data[PARAMS][CHAT_AUTHOR_ID]': '0', 'data[PARAMS][CHAT_ENTITY_TYPE]': 'LINES',
        'data[PARAMS][CHAT_ENTITY_ID]': 'telegrambot|1|1398715343|13',
        'data[PARAMS][CHAT_ENTITY_DATA_1]': 'Y|LEAD|3|N|N|1|1711455826|0|0|0',
        'data[PARAMS][CHAT_ENTITY_DATA_2]': 'LEAD|3|COMPANY|0|CONTACT|0|DEAL|0',
        'data[PARAMS][COMMAND_CONTEXT]': 'TEXTAREA', 'data[PARAMS][MESSAGE_ORIGINAL]': 'hahahahaha',
        'data[PARAMS][TO_USER_ID]': '0', 'data[PARAMS][DIALOG_ID]': 'chat5', 'data[PARAMS][MESSAGE_ID]': '17',
        'data[PARAMS][CHAT_TYPE]': 'L', 'data[PARAMS][LANGUAGE]': 'ru', 'data[USER][ID]': '13',
        'data[USER][NAME]': '[Dev] Oleg Pashchenko', 'data[USER][FIRST_NAME]': '[Dev] Oleg',
        'data[USER][LAST_NAME]': 'Pashchenko', 'data[USER][GENDER]': 'M', 'data[USER][IS_BOT]': 'N',
        'data[USER][IS_CONNECTOR]': 'Y', 'data[USER][IS_NETWORK]': 'N', 'data[USER][IS_EXTRANET]': 'Y',
        'ts': '1711455834', 'auth[domain]': 'b24-1x2ywp.bitrix24.ru',
        'auth[client_endpoint]': 'https://b24-1x2ywp.bitrix24.ru/rest/',
        'auth[server_endpoint]': 'https://oauth.bitrix.info/rest/',
        'auth[member_id]': '869e4953d7e841e02de675524e65f51a', 'auth[application_token]': '192735'}
if __name__ == '__main__':
    asyncio.run(main())
