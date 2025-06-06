# backend/src/provaia/utils/logger.py

import logging
import sys

# Configuração básica do logger
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

logging.basicConfig(
    level=logging.INFO,  # Nível mínimo de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout)  # Exibe logs no console
    ]
)

def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger configurado para uso em qualquer módulo.

    Args:
        name (str): Nome do módulo que irá utilizar o logger.

    Returns:
        logging.Logger: Instância do logger configurado.
    """
    return logging.getLogger(name)