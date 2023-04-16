from unittest import TestCase
from apps.receipts import api_clients


# Create your tests here.
class ReceiptAPITestCase(TestCase):

    def setUp(self):
        mock_client = api_clients.VeryfiMockClient()
        self.unit_under_test = api_clients.ReceiptProcessor(mock_client)

    def test_jason_mock_receipt(self):
        """	Check JSON response """
        response = self.unit_under_test.process_document('', '')
        self.assertEqual(response['subtotal'], 129.42)

