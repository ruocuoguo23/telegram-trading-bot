import logging.handlers
import os


class LoggerFactory:
    logger = None
    log_formatter = '%(asctime)s - %(process)d - %(thread)d - %(levelname)s - ' \
                    '%(filename)s[line:%(lineno)d] - %(message)s'

    @staticmethod
    def get_log_folder():
        # instead of user_data_dir, use current dir
        current_directory = os.getcwd()
        return os.path.join(current_directory, "log")

    @staticmethod
    def create_file_handler(file_name: str, level: int, backup_count: int):
        file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(LoggerFactory.get_log_folder(), file_name),
            encoding="utf-8",
            maxBytes=20 * 1024 * 1024,
            backupCount=backup_count,
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(LoggerFactory.log_formatter))
        return file_handler

    @staticmethod
    def create_stream_handler(level: int):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setLevel(level)
        stream_handler.setFormatter(logging.Formatter(LoggerFactory.log_formatter))
        return stream_handler

    @staticmethod
    def get_logger_instance():
        return LoggerFactory.logger

    @staticmethod
    def init_logger():
        log_folder = LoggerFactory.get_log_folder()
        if not os.path.exists(log_folder):
            os.makedirs(log_folder, exist_ok=True)

        def create_logger(name: str, file_handler_tuples):
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(LoggerFactory.create_stream_handler(logging.DEBUG))
            for file_name, level, backup_count in file_handler_tuples:
                logger.addHandler(LoggerFactory.create_file_handler(
                    file_name=file_name,
                    level=level,
                    backup_count=backup_count,
                ))
            return logger

        LoggerFactory.logger = create_logger(
            'trading_bot_trader',
            [
                ('debug.log', logging.DEBUG, 5),
                ('error.log', logging.ERROR, 2),
            ])


LoggerFactory.init_logger()

trading_logger = LoggerFactory().get_logger_instance()
