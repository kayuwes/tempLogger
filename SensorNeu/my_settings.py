# Atmospi settings.
import os
dir = os.path.dirname(__file__)
db = os.path.join(dir, 'log.db')

#db= log.db

span1HOUR = 60*60
span12HOUR = 60*60*12
span1DAY = 60*60*24
span3DAY = 60*60*24*3
span7DAY = 60*60*24*7
span30DAY = 60*60*24*30


    # How far into the past should data be loaded (in seconds)?
    # Default to 1 week.
#    'range_seconds': 60 * 60 * 24 * 7,

    # The number of digits after the decimal place that will be stored.
#    'precision': 2,

    # Temperature unit of measure (C or F).
#    't_unit': 'F',
#}
