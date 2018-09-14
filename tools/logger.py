import logging
import os


class Logger:

    def __init__(self, log_file_full_name="test.log", module_name=None):
        # full_root_script_path = os.getcwd()
        # self.log_file_path = "{}/{}".format(full_root_script_path, log_file_name)
        # self.log_file_path = log_file_full_name
        self.log_file_name = log_file_full_name

        if module_name is None:
            self.module_name = str(__name__)
        else:
            self.module_name = module_name

        # create file handler which logs even debug messages
        self.logger_handle = logging.getLogger(self.module_name)
        self.logger_handle.setLevel(logging.DEBUG)

        file_h = logging.FileHandler(self.log_file_name)
        file_h.setLevel(logging.INFO)

        # create console handler with a higher log level
        console_h = logging.StreamHandler()
        console_h.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers
        #formatter = logging.Formatter("%(asctime)-20s%(name)-10s-%(levelname)-8s" +
        #                              "#%(message)s#", "%Y/%m/%d %H:%M:%S")
        formatter = logging.Formatter("%(asctime)-20s %(name)-10s-%(levelname)-8s" +
                                      "|%(message)s|")
        console_h.setFormatter(formatter)
        file_h.setFormatter(formatter)

        # add the handlers to logger
        self.logger_handle.addHandler(console_h)
        self.logger_handle.addHandler(file_h)

