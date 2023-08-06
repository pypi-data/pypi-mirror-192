from loggermodule_XS import logger_x
from test02.test_log_02 import numbersum


log = logger_x(__file__).configLogger()


num, num2 = 20,17
sum = numbersum(num,num2)

log.info("START -----------------------------------------")
for _ in range(50000000):
    log.info(_)

# log.info('THIS is info msg !!')
# log.debug('THIS is debug msg !!')
# log.error('THIS is error msg !!')
# log.warning('THIS is warning msg !!')
# log.critical('THIS is critical msg !!')

# log.info('1st LINE !!!!!')
# while True:
#     log.info('INFO')
#     log.debug('DEBUG')
#     log.error('ERROR')
#     log.warning('WARNING')
#     True
