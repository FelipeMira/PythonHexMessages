import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logger():
    """
    Configura o logger para exibir mensagens no formato JSON com UTF-8 e renomeia 'asctime' para 'timestamp'.
    """
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setStream(sys.stdout)  # Garante UTF-8 no StreamHandler
    log_handler.setFormatter(
        jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s %(filename)s %(funcName)s %(lineno)d',
            rename_fields={"asctime": "timestamp"}  # Renomeia 'asctime' para 'timestamp'
        )
    )
    log_handler.encoding = "utf-8"  # Define explicitamente a codificação UTF-8

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Define o nível de log para INFO (ignora DEBUG)
    logger.addHandler(log_handler)

    # Desativa logs de bibliotecas externas, como boto3
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)