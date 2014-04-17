# -#-coding: utf-8 -#-
import datetime
import ckan.plugins.toolkit as tk
import pytz
import pylons.config as config
from pytz import timezone
from ckan.lib.helpers import date_str_to_datetime
from ckan.common import _
from ckan import model

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

def extend_search_convert_local_to_utc_timestamp(str_timestamp):
    if not str_timestamp:
        return ''

    local_datetime  = datetime.datetime.strptime(str_timestamp, DATETIME_FORMAT);
    tz_code = config.get('ckan.timezone', 'Australia/Melbourne')
    local = timezone(tz_code)
    utc_datetime = _make_aware(local_datetime, local)
    local_datetime = utc_datetime.astimezone(pytz.utc)
    return local_datetime.strftime(DATETIME_FORMAT)

def _is_aware(value):
    """
    Determines if a given datetime.datetime is aware.

    The logic is described in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo
    """
    return value.tzinfo is not None and value.tzinfo.utcoffset(value) is not None

def _is_naive(value):
    """
    Determines if a given datetime.datetime is naive.

    The logic is described in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo
    """
    return value.tzinfo is None or value.tzinfo.utcoffset(value) is None

def _make_aware(value, timezone):
    """
    Makes a naive datetime.datetime in a given time zone aware.
    """
    if hasattr(timezone, 'localize'):
        # available for pytz time zones
        return timezone.localize(value, is_dst=None)
    else:
        # may be wrong around DST changes
        return value.replace(tzinfo=timezone)

def _make_naive(value, timezone):
    """
    Makes an aware datetime.datetime naive in a given time zone.
    """
    value = value.astimezone(timezone)
    if hasattr(timezone, 'normalize'):
        # available for pytz time zones
        value = timezone.normalize(value)
    return value.replace(tzinfo=None)

