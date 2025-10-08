import os
from dotenv import load_dotenv

#! https://img.vietqr.io/image/<BANK_ID>-<ACCOUNT_NO>-<TEMPLATE>.png?amount=<AMOUNT>&addInfo=<DESCRIPTION>&accountName=<ACCOUNT_NAME>
class VietQR:
    def __init__(self,amount:int, description:str):
        load_dotenv()
        bank_id = os.getenv('bank_type_id')
        account_no = os.getenv('bank_account_id')
        template = os.getenv('bank_template')
        account_name = os.getenv('bank_account_owner_name')
        self.apiqr = f'https://img.vietqr.io/image/{bank_id}-{account_no}-{template}?amount={amount}&addInfo={description}&accountName={account_name}'
    