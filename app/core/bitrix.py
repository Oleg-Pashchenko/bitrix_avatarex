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
        response = await self.bitrix.call(method='crm.deal.update', items={
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
        fields = await self.bitrix.call(method='crm.deal.fields', items={
            'order': {
                'ID': 'desc'
            }
        })

        answer = {}
        for f in fields.keys():
            if 'UF_CRM_' in f:
                answer[fields[f]['listLabel']] = {'code': fields[f]['title'],
                                                  'enum': fields[f]['items']
                                                  }
        return answer



def get_pipeline_and_status(deal):
    status = deal.get('STAGE_ID', 'NEW')
    pipeline = 0 if status == 'NEW' else int(status.split(':')[0].replace('C', ''))
    return pipeline, status


async def main():
    b = BitrixAvatarex(webhook='https://b24-diyu7k.bitrix24.ru/rest/1/320mlzqaz81oy0rj/')
    # resp = await b.fill_field(2, 'UF_CRM_1710323772028', '50')
    # print(resp)
    response = await b.get_all_fields()
    print(response)
    response = await b.get_deal(2)
    print(response)

if __name__ == '__main__':
    asyncio.run(main())


# В сценарий нового сообщения