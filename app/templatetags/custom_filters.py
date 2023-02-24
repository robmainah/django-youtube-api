from django import template
from numerize import numerize
from isodate import parse_duration
from time import strftime, gmtime
from datetime import timedelta

register = template.Library()

def format_numbers(value):
    return numerize.numerize(int(value))


def format_duration(duration):
    seconds = parse_duration(duration).total_seconds()

    if seconds > 86400: # greater than one day
        # value = parse_duration("PT25H31M30S").total_seconds()
        # return "{}".format(str(timedelta(seconds=seconds)))
        return parse_duration(duration)
    elif int(strftime("%H", gmtime(seconds))) > 0:
        return strftime("%H:%M:%S", gmtime(seconds))
    else:
        return strftime("%M:%S", gmtime(seconds))


register.filter('human_readable', format_numbers)
register.filter('human_duration', format_duration)
