import logging
from src.application.domain.message import Message


class MessageInMapper:
    """
    Mapper para converter mensagens AWS para o domínio da aplicação.
    """

    @staticmethod
    def aws_to_domain(message, headers):
        """
        Converte uma mensagem AWS para o modelo de domínio.

        :param message: Mensagem AWS (com payload e atributos).
        :param headers: Cabeçalhos da mensagem.
        :return: Instância de Message representando o modelo de domínio.
        """
        logging.info("Iniciando a conversao da mensagem AWS para o modelo de dominio.")
        logging.debug(f"Mensagem recebida: {message}")
        logging.debug(f"Cabecalhos recebidos: {headers}")

        domain_message = Message(
            text=message.get("Payload"),
            message_attributes=MessageInMapper.map_to_string_map(headers),
        )

        logging.info("Mensagem convertida com sucesso para o modelo de dominio.")
        logging.debug(f"Mensagem convertida: {domain_message}")
        return domain_message

    @staticmethod
    def map_to_string_map(headers):
        """
        Converte os atributos da mensagem AWS para um dicionário de strings.

        :param headers: Dicionário de atributos da mensagem AWS.
        :return: Dicionário com os valores extraídos de 'StringValue'.
        """
        logging.info("Iniciando a conversao dos cabecalhos para um dicionario de strings.")
        logging.debug(f"Cabecalhos recebidos para conversão: {headers}")

        result = {}
        for key, value in headers.items():
            if isinstance(value, dict):
                data_type = value.get("DataType")
                string_value = value.get("StringValue")
                if data_type in ["String", "Number", "Binary"] and string_value is not None:
                    result[key] = string_value
                    logging.debug(f"Atributo processado: {key} = {string_value} (DataType: {data_type})")
            else:
                result[key] = str(value)
                logging.debug(f"Atributo processado: {key} = {value} (convertido para string)")

        logging.info("Conversao dos cabecalhos concluida.")
        logging.debug(f"Resultado da conversao: {result}")
        return result