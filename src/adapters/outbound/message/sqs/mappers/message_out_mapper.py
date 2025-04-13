class MessageOutMapper:
    """
    Mapper para converter mensagens do domínio para o formato SQS.
    """

    @staticmethod
    def message_to_send_message_request(message, queue_url):
        """
        Converte uma instância de Message para o formato esperado pelo SQS.

        :param message: Instância de Message contendo texto e atributos.
        :param queue_url: URL da fila SQS.
        :return: Dicionário representando a requisição de envio de mensagem.
        """
        message_attributes = {}
        for key, value in message.message_attributes.items():
            if isinstance(value, dict):
                data_type = value.get("DataType", "String")  # Padrão para "String" se não especificado
                string_value = value.get("StringValue")
                binary_value = value.get("BinaryValue")
                number_value = value.get("NumberValue")

                if data_type == "String" and string_value is not None:
                    message_attributes[key] = {
                        "DataType": "String",
                        "StringValue": string_value
                    }
                elif data_type == "Number" and number_value is not None:
                    message_attributes[key] = {
                        "DataType": "Number",
                        "StringValue": str(number_value)  # SQS espera números como strings
                    }
                elif data_type == "Binary" and binary_value is not None:
                    message_attributes[key] = {
                        "DataType": "Binary",
                        "BinaryValue": binary_value
                    }
            else:
                # Caso o valor seja uma string simples, assume "String" como DataType
                message_attributes[key] = {
                    "DataType": "String",
                    "StringValue": str(value)
                }

        return {
            "QueueUrl": queue_url,
            "MessageBody": message.text,
            "MessageAttributes": message_attributes
        }