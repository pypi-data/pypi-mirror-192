from loggermodule_XS import logger_x

loggerX = logger_x(__file__, console='DEBUG')
log = loggerX.configLogger()
log.info("START -----------------------------------------")
log.info('test_log_2')

class numbersum:
    def __init__(self, num,num2):
        self.number = num
        self.number2=num2

    def sum(self):
        number = self.number
        number2 = self.number2
        sum = number+number2

        return sum