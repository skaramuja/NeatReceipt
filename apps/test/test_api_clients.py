import unittest

from apps.receipts.api_clients import ReceiptProcessor, VeryfiMockClient


class TestReceiptProcessor(unittest.TestCase):

    def test_receipt_processor(self):
        mock_client = VeryfiMockClient()
        unit_under_test = ReceiptProcessor(mock_client)
        json_mock_result = unit_under_test.process_document('', '', '')
        actual = json_mock_result['total']
        assert actual == 131.38


if __name__ == '__main__':
    unittest.main()
