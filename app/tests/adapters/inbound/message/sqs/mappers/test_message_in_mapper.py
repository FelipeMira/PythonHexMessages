import unittest
from app.src.adapters.inbound.message.sqs.mappers.message_in_mapper import MessageInMapper
from app.src.application.domain.message import Message


class TestMessageInMapper(unittest.TestCase):
    def test_aws_to_domain(self):
        # Dados de entrada simulados
        aws_message = {"Payload": "Test message"}
        headers = {
            "Attribute1": {"DataType": "String", "StringValue": "Value1"},
            "Attribute2": {"DataType": "Number", "StringValue": "123"},
        }

        # Chamada do método
        result = MessageInMapper.aws_to_domain(aws_message, headers)

        # Verificações
        self.assertIsInstance(result, Message)
        self.assertEqual(result.text, "Test message")
        self.assertEqual(result.message_attributes, {"Attribute1": "Value1", "Attribute2": "123"})

    def test_map_to_string_map(self):
        # Dados de entrada simulados
        headers = {
            "Attribute1": {"DataType": "String", "StringValue": "Value1"},
            "Attribute2": {"DataType": "Number", "StringValue": "123"},
            "Attribute3": "RawValue",
        }

        # Chamada do método
        result = MessageInMapper.map_to_string_map(headers)

        # Verificações
        self.assertEqual(result, {
            "Attribute1": "Value1",
            "Attribute2": "123",
            "Attribute3": "RawValue",
        })

    def test_map_to_string_map_invalid_data(self):
        # Dados de entrada simulados com valores inválidos
        headers = {
            "Attribute1": {"DataType": "String"},
            "Attribute2": {"DataType": "Number", "StringValue": None},
        }

        # Chamada do método
        result = MessageInMapper.map_to_string_map(headers)

        # Verificações
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()