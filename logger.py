import logging

_error_format = f"%(asctime)s - [%(func)s] - %(name)s - %(message)s"
_info_format = f"%(asctime)s - %(message)s"

def get_function_errors_handler():
    file_handler = logging.FileHandler("logs/functions_errors.log")
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter(_error_format))
    return file_handler

def get_commands_handler():
    file_handler = logging.FileHandler("logs/commands.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_info_format))
    return file_handler

def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_error_format))
    return stream_handler

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_function_errors_handler())
    logger.addHandler(get_commands_handler())
    # logger.addHandler(get_stream_handler())
    return logger