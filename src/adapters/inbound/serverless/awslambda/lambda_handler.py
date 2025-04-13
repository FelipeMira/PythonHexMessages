import logging

from src.adapters.inbound.serverless.awslambda.errors.global_exception_handler import GlobalExceptionHandler
from src.adapters.inbound.serverless.awslambda.mappers.event_in_mapper import EventToMessageMapper
from src.adapters.inbound.serverless.awslambda.response.response import Response
from src.application.ports.inbound.process_message_use_case import ProcessMessage

class LambdaHandler:
    def __init__(self, event_in_mapper: EventToMessageMapper, process_message: ProcessMessage):
        """
        Inicializa o handler com as dependências necessárias.

        :param event_in_mapper: Mapper para converter eventos AWS para o domínio.
        :param process_message: Caso de uso para processar mensagens.
        """
        self.event_in_mapper = event_in_mapper
        self.process_message = process_message

    def handle(self, event, context):
        """
        Handler para processar mensagens recebidas por uma AWS Lambda.

        :param event: Evento recebido pela Lambda (ex.: mensagem SQS).
        :param context: Contexto de execução da Lambda.
        """
        logging.basicConfig(level=logging.INFO)
        logging.info("Iniciando o handler da Lambda...")

        try:
            # Processa cada registro do evento
            logging.info(f"Processando evento: {event}")
            body = event["body"]

            # Extrai os headers do evento (ex.: vindo do API Gateway)
            headers = event.get("headers", {})
            headers_list = [(key, value) for key, value in headers.items()]  # Converte para lista de tuplas

            # Mapeia a mensagem para o domínio
            domain_message = self.event_in_mapper.event_to_message({"body": body, "headers": headers})

            # Processa a mensagem
            self.process_message.run(domain_message)
            logging.info("Mensagem processada com sucesso.")

            # Retorna resposta de sucesso após processar todos os registros
            return Response(
                status_code=200,
                body="{\"result\": \"Sucesso\"}",
                headers=headers_list,
                method=event["requestContext"]["http"]["method"],
            ).to_dict()

        except Exception as e:
            response = GlobalExceptionHandler.handle_exception(e, event)
            logging.error(f"Resposta de erro: {response}")
            return response