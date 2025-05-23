from app.src.adapters.config.sqs.sqs_config import SqsConfig
from app.src.adapters.outbound.message.sqs.mappers.message_out_mapper import MessageOutMapper
from app.src.adapters.outbound.message.sqs.base.base_queue import BaseQueue
from app.src.common.properties_env import x_type_alert, queue_alert_url


class SQSOutputAlert(BaseQueue):
    """
    Classe para envio de mensagens de alerta para a fila SQS.
    """

    def __init__(self):
        super().__init__(
            x_type=x_type_alert,
            queue_url=queue_alert_url,
            sqs_client=SqsConfig().get_client(),
            message_out_mapper=MessageOutMapper()
        )