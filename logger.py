import logging

_error_format = f"%(asctime)s - [%(func)s] - %(name)s - %(message)s"
_info_format = f"%(asctime)s - %(message)s"

def commands_errors_handler():
    file_handler = logging.FileHandler("logs/commands_errors.log")
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter(_error_format))
    return file_handler

def commands_info_handler():
    file_handler = logging.FileHandler("logs/commands_info.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_info_format))
    return file_handler

def ml_info_handler():
    file_handler = logging.FileHandler("logs/ml_info.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_info_format))
    return file_handler

def ml_errors_handler():
    file_handler = logging.FileHandler("logs/errors_info.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_info_format))
    return file_handler

def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_error_format))
    return stream_handler

def get_commands_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(commands_errors_handler())
    logger.addHandler(commands_info_handler())
    # logger.addHandler(get_stream_handler())
    return logger

def get_ml_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(ml_errors_handler())
    logger.addHandler(ml_info_handler())
    return logger