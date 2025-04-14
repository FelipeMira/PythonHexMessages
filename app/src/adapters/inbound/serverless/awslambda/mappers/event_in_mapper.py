import logging
from app.src.application.domain.message import Message


class EventToMessageMapper:
    """
    Mapper para converter eventos AWS (como HTTP via API Gateway) para o modelo de domínio Message.
    """

    @staticmethod
    def event_to_message(event):
        """
        Converte um evento AWS para o modelo de domínio Message.

        :param event: Evento recebido pelo Lambda (ex.: HTTP via API Gateway).
        :return: Instância de Message representando o modelo de domínio.
        """
        logging.info("Iniciando a conversao do evento AWS para o modelo de dominio.")
        logging.debug(f"Evento recebido: {event}")

        # Extrai o payload do corpo do evento
        payload = event.get("body", "")

        # Extrai os headers do evento
        headers = event.get("headers", {})

        # Converte os headers para atributos de mensagem
        message_attributes = EventToMessageMapper.map_headers_to_message_attributes(headers)

        # Cria a instância de Message
        domain_message = Message(
            text=payload,
            message_attributes=message_attributes,
        )

        logging.info("Evento convertido com sucesso para o modelo de dominio.")
        logging.debug(f"Mensagem convertida: {domain_message}")
        return domain_message

    @staticmethod
    def map_headers_to_message_attributes(headers):
        """
        Converte os cabeçalhos HTTP para um dicionário de strings.

        :param headers: Dicionário de cabeçalhos HTTP.
        :return: Dicionário com os valores extraídos de 'StringValue' ou convertidos para string.
        """
        logging.info("Iniciando a conversao dos cabecalhos HTTP para um dicionario de strings.")
        logging.debug(f"Cabecalhos recebidos para conversao: {headers}")

        result = {}
        for key, value in headers.items():
            if isinstance(value, dict):
                string_value = value.get("StringValue")
                if string_value is not None:
                    result[key] = string_value
                    logging.debug(f"Atributo processado: {key} = {string_value}")
            else:
                result[key] = str(value)
                logging.debug(f"Atributo processado: {key} = {value} (convertido para string)")

        logging.info("Conversao dos cabecalhos concluida.")
        logging.debug(f"Resultado da conversao: {result}")
        return result