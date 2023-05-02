import json
import pathlib

import dotenv
import veryfi
import os


class VeryfiClient:
    """
    A class that interacts with the Veryfi server.
    """
    def __init__(self):
        """
        Create a new instance of the class.
        """
        dotenv.read_dotenv()
        veryfi_client_id = os.environ.get('VERYFI_CLIENT_ID')
        veryfi_api_key = os.environ.get('VERYFI_API_KEY')
        veryfi_client_secret = os.environ.get('VERYFI_CLIENT_SECRET')
        veryfi_username = os.environ.get('VERYFI_USERNAME')
        self.client = veryfi.Client(veryfi_client_id, veryfi_client_secret, veryfi_username, veryfi_api_key)

    def process_document(self, receipt_image, category):
        """
        Sends a receipt to Veryfi to be processed.
        :param receipt_image: The image to send to Veryfi.
        :param category: The categories that should be used for parsing the receipt.
        :return: The response from Veryfi.
        """
        url = receipt_image.image.path
        return self.client.process_document(url, [category])


class VeryfiMockClient:
    """
    A mock client for processing receipts.
    """
    def process_document(self, receipt_image, category):
        """
        Mock method for returning sample JSON.
        :param receipt_image: Unused. Sample JSON will be returned.
        :param category: Unused. Sample JSON will be returned.
        :return: Sample JSON.
        """
        path = pathlib.Path(__file__).parent.parent.parent.joinpath('static', 'img', 'sample_receipts', 'hyvee_json_response')
        file = open(path)
        mock_json = json.load(file)
        file.close()
        return mock_json


class ReceiptProcessor:
    def __init__(self, veryfi_client):
        """
        Creates a new instance with the specified client.
        :param veryfi_client: The client that should be used for processing documents.
        """
        self.veryfi_client = veryfi_client

    def process_document(self, receipt_image, category, current_user):
        """
        Processes the provided document and saves it in the database.
        :param receipt_image: The image that was uploaded by the user.
        :param category: The categories associated with the receipt.
        :param current_user: The user uploading the image.
        :return: Does not return anything.
        """
        from apps.receipts.models import Receipt
        json = self.veryfi_client.process_document(receipt_image, category)
        print(current_user)

        vendor = self.process_receipt_vendor(json['vendor'])

        receipt = Receipt()

        receipt.user = current_user
        receipt.image = receipt_image

        receipt.subtotal = json['subtotal']
        receipt.tax = json['tax']
        receipt.total_price = json['total']
        receipt.vendor = vendor
        receipt.date = json['date']
        receipt.save()

        self.process_receipt_item(json['line_items'], receipt)

    def process_receipt_item(self, items, receipt):
        """
        Parses the provided JSON and saves the items as ReceiptItems in the database.
        :param items: JSON representing the receipt items to be stored in the database.
        :return: The parsed receipt items.
        """
        from apps.receipts.models import ReceiptItem
        for item in items:
            receipt_item = ReceiptItem()
            receipt_item.name = item['description']
            if item['description'] is None:
                continue
            receipt_item.name = item['description']
            receipt_item.price = item['total']
            receipt_item.type = item['type']
            receipt_item.receipt = receipt
            receipt_item.save()

    def process_receipt_vendor(self, vendor):
        """
        Parses the provided JSON into a Vendor and saves it in the database.
        :param vendor: JSON representing the vendor to be stored in the database.
        :return: The parsed Vendor.
        """
        from apps.receipts.models import Vendor
        receipt_vendor = Vendor()
        receipt_vendor.name = vendor['name']
        receipt_vendor.category = vendor['category']

        receipt_vendor.save()

        return receipt_vendor
