import logging
logger = logging.getLogger('logger') #Create a log with the same name as the script that created it
#logger.setLevel('DEBUG')
logger.setLevel('INFO')


filehandler_dbg = logging.FileHandler(logger.name + '-debug.log', mode='w')

#filehandler_dbg.setLevel('DEBUG')
filehandler_dbg.setLevel('INFO')

#streamformatter = logging.Formatter(fmt='%(levelname)s:\t%(threadName)s:\t%(funcName)s:\t\t\t%(message)s', datefmt='%H:%M:%S') #We only want to see certain parts of the message
streamformatter = logging.Formatter("%(message)10s", '%H:%M:%S') #We only want to see certain parts of the message

filehandler_dbg.setFormatter(streamformatter)

logger.addHandler(filehandler_dbg)
