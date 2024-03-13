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

    async def set_field(self, lead_id, field_name, field_value):
        pass

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



def get_pipeline_and_status(deal):
    status = deal.get('STAGE_ID', 'NEW')
    pipeline = 0 if status == 'NEW' else int(status.split(':')[0].replace('C', ''))
    return pipeline, status


async def main():
    b = BitrixAvatarex(webhook='https://b24-diyu7k.bitrix24.ru/rest/1/320mlzqaz81oy0rj/')
    response = await b.register_bot()
    print(response)

if __name__ == '__main__':
    asyncio.run(main())