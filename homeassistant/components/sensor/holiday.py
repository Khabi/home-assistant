"""
Support for looking up current holidays

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/sensor/holiday/
"""
import logging
from datetime import date
from dateutil.relativedelta import relativedelta as fd # Floating Dates
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from dateutil.easter import easter

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_TYPE
from homeassistant.helpers.entity import Entity
import homeassistant.util as util

REQUIREMENTS = ['python-dateutil==2.6.1']

_LOGGER = logging.getLogger(__name__)

def holiday_dates(year):
	DATES = {
		"US": {
			"New Years Day": 				date(year,1,1),
			"Martin Luther King Jr. Day": 	date(year,1,1) + fd(weekday=MO(3)),
			"Civil Rights Day": 			date(year,1,1) + fd(weekday=MO(3)),
			"Presidents' Day":				date(year,2,1) + fd(weekday=MO(3)),
			"Groundhog Day": 				date(year,2,1),
			"Valentine's Day":				date(year,2,14),
			"St. Patrick's Day":			date(year,3,17),
			"April Fool's Day":				date(year,4,1),
			"Earth Day":					date(year,4,22),
			"Easter":						easter(year=2017),
			"Mother's Day":					date(year,5,1) + fd(weekday=SU(2)),
			"Memorial Day":					date(year,6,1) + fd(weekday=MO(-1)),
			"Father's Day":					date(year,6,1) + fd(weekday=SU(3)),
			"Independence Day":				date(year,7,4),
			"Labor Day":					date(year,9,1) + fd(weekday=MO),
			"Columbus Day":					date(year,10,1) + fd(weekday=MO(2)),
			"Indigenous Peoples' Day":		date(year,10,1) + fd(weekday=MO(2)),
			"Halloween":					date(year,10,31),
			"Veterans Day":					date(year,11,11),
			"Christmas":					date(year,12,25),
			"New Year's Eve":				date(year,12,31),
		},
		"CA": {
			"New Years Day": 				date(year,1,1),
			"Groundhog Day": 				date(year,2,1),
			"Valentine's Day":				date(year,2,14),
			"April Fool's Day":				date(year,4,1),
			"Earth Day":					date(year,4,22),
			"Father's Day":					date(year,6,1) + fd(weekday=SU(3)),
			"Canada Day":					date(year,7,1),
			"Labour Day":					date(year,9,1) + fd(weekday=MO(1)),
			"Halloween":					date(year,10,31),
			"Christmas":					date(year,12,25),
		}
	}
	return DATES

def lookup_holiday(date):
	year = date.year
	month = date.month
	day = date.day

