from src.adapters.inbound.message.sqs.config.sqs_config import SqsConfig
from src.adapters.outbound.message.sqs.mappers.message_out_mapper import MessageOutMapper
from src.adapters.outbound.message.sqs.base.base_queue import BaseQueue
from src.common.properties_env import x_type_error, queue_error_url


class SQSOutputError(BaseQueue):
    """
    Classe para envio de mensagens de erro para a fila SQS.
    """

    def __init__(self):
        super().__init__(
            x_type=x_type_error,
            queue_url=queue_error_url,
            sqs_client=SqsConfig().get_client(),
            message_out_mapper=MessageOutMapper()
        )