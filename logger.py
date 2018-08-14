import logging
import os

class Logger():
    def __init__(self, log_file_name="test.log", module_name=None):
        full_root_script_path = os.getcwd()
        self.log_file_path = "{}/{}".format(full_root_script_path, log_file_name)

        self.log_file_name = self.log_file_path

        if module_name is None:
            self.module_name = str(__name__)
        else:
            self.module_name = module_name

        # create file handler which logs even debug messages
        self.logger = logging.getLogger(self.module_name)
        self.logger.setLevel(logging.DEBUG)

        file_h = logging.FileHandler(self.log_file_path)
        file_h.setLevel(logging.INFO)

        # create console handler with a higher log level
        console_h = logging.StreamHandler()
        console_h.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s: %(name)s - %(levelname)s #%(message)s#', "%Y/%m/%d %H:%M:%S")
        console_h.setFormatter(formatter)
        file_h.setFormatter(formatter)

        # add the handlers to logger
        self.logger.addHandler(console_h)
        self.logger.addHandler(file_h)

