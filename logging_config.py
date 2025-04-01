import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def init_logger(name):
    logs_path = f'{name}.log'
    logger = logging.getLogger(name)
    if not logger.handlers:  # Почему-то иногда создаётся по 2 одинаковых логера, пришлось заифать
        file_handler = logging.FileHandler(logs_path)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.propagate = False
    return logger
