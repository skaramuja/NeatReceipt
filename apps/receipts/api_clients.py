import json

import dotenv
import veryfi
import os
import pathlib


class VeryfiClient:
    def __init__(self, client_id, client_secret, username, api_key):
        self.client = veryfi.Client(client_id, client_secret, username, api_key)

    def process_document(self, local_url, category):
        return self.client.process_document(local_url, category)


class VeryfiMockClient:
    def process_document(self, local_url, category):
        path = pathlib.Path(__file__).parent.parent.parent.joinpath('static', 'img', 'sample_receipts', 'hyvee_jason_response')
        file = open(path)
        mock_json = json.load(file)
        file.close()
        return mock_json


class ReceiptProcessor:
    def __init__(self, veryfi_client):
        self.veryfi_client = veryfi_client

    def process_document(self, local_url, category):
        return self.veryfi_client.process_document(local_url, category)


if __name__ == '__main__':
    dotenv.read_dotenv()
    client_id = os.environ.get('VERYFI_CLIENT_ID')
    client_secret = os.environ.get('VERYFI_CLIENT_SECRET')
    username = os.environ.get('VERYFI_USERNAME')
    api_key = os.environ.get('VERYFI_API_KEY')
    local_url = pathlib.Path(__file__).parent.parent.parent.joinpath('static', 'img', 'sample_receipts', 'hyvee.jpg')
    catagories = ['Grocery', 'Hardware', 'Auto', 'Clothing', 'Travel']

    veryfi_client = VeryfiClient(client_id, client_secret, username, api_key)
    mock_client = VeryfiMockClient()
    receipt_processor = ReceiptProcessor(mock_client)
    jason_mock_result = receipt_processor.process_document(local_url, catagories)
    print(jason_mock_result)
