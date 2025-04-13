import uuid

class MessageOutDBMapper:

    @staticmethod
    def map(message):
        """
        Mapeia uma instância de Message para o formato necessário pelo DynamoDB.

        :param message: Instância de Message.
        :return: Dicionário no formato esperado pelo DynamoDB.
        """
        return {
            "id": {"S": message.message_attributes.get("id", str(uuid.uuid4()))},
            "text": {"S": message.text or ""},
            "message_attributes": {"S": str(message.message_attributes)},
        }