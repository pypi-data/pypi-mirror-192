
"""Intercept the Python logging module.

"""

import logging

from ..base import BaseInterceptor


class LoggingInterceptor(BaseInterceptor):
    LOGGING_ERROR_DISPLAY_NAME = '{logger_name} [{level_name}]'

    def _callHandlers(self, callHandlers, logger, record):
        self.agent.application_loggers.add(logger)

        with self.log_exceptions():
            if not record.name.startswith('pythonagent') and self.bt:
                self.agent.logger.info("error message as {}".format(record.getMessage()))
                self.add_logged_error(record)

        try:
            if type(record.msg) != str:
                record.msg = str(record.msg)

            context = self.agent.get_transaction_context()
            recordReqIdmsg = f" [ RequestId : {context.aws_request_id} ] " + record.msg 
            record.msg = recordReqIdmsg

            if not record.name.startswith('pythonagent'):
                fpTopo = self.agent.sdk_getTopoFpStr(self.bt)
                record.msg = record.msg + str(fpTopo)

        except Exception as e:
            print(e)

        callHandlers(logger, record)

    def add_logged_error(self, record):
        """Add an error to the BT if the log record should trigger an error.

        If the level is greater or equal than the threshold and the message is
        not ignored, create an ErrorInfo object and add it to the BT.

        """
        #error_config = self.agent.error_config_registry

        #if not error_config.should_detect_logged_errors:
        #    return

        levelno = record.levelno
        if levelno < 40:
            return

        msg = record.getMessage()
        #if any(conditions.match(msg, match_cond) for match_cond in error_config.ignored_messages):
        #    return

        if record.exc_info:
            import traceback
            import os
            import time
            start_time = round(time.time()*1000)
            throwing_method = traceback.extract_tb(record.exc_info[2])[-1][2]
            line_number = traceback.extract_tb(record.exc_info[2])[-1][1]
            stktrc = logging.Formatter().formatException(record.exc_info)
            encodedstktrc = stktrc.replace("\n", "%7C")
            encodedstktrc = encodedstktrc.replace(" ", "")
            encodedstktrc = encodedstktrc.replace(",", "")
            exception_class =  str(record.exc_info[0].__name__)
            exception_message = str(record.exc_info[1])
            exception_cause = str(record.exc_info[0].__cause__)
            self.agent.exceptiondump(self.bt, None, start_time, exception_class, exception_message, "None", throwing_method, exception_cause, line_number, encodedstktrc)
            msg += '\n' + logging.Formatter().formatException(record.exc_info)

        display_name = self.LOGGING_ERROR_DISPLAY_NAME.format(logger_name=record.name, level_name=record.levelname)
        #self.bt.add_logged_error(ErrorInfo(msg, display_name, levelno))
        self.agent.logger.info('Logging error added in logs as message {0} display name as {1} and level of error is {2}'.format(msg,display_name,levelno))


def intercept_logging(agent, mod):
    LoggingInterceptor(agent, mod.Logger).attach('callHandlers')


