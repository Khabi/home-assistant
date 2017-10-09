"""
Support for looking up current holidays

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/sensor/holiday/
"""
import logging
from datetime import date, datetime
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

def setup_platform(hass, config, add_devices, discovery_info=None):
	add_devices([Holiday(hass)])
	return True

def holiday_dates(year):
	""" Map of holiday to dates
	Using relativedelta we can lookup datees that don't fall on the same day each year."""
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
			"Thanksgiving":					date(year,11,1) + fd(weekday=TH(4)),
			"Veterans Day":					date(year,11,11),
			"Christmas Eve":				date(year,12,24),
			"Christmas":					date(year,12,25),
			"New Year's Eve":				date(year,12,31),
			"Fake Holiday":					date.today(),
			"Other Fake Holiday":			date.today()
		},
		"CA": {
			"New Years Day": 				date(year,1,1),
			"Groundhog Day": 				date(year,2,1),
			"Valentine's Day":				date(year,2,14),
			"April Fool's Day":				date(year,4,1),
			"Earth Day":					date(year,4,22),
			"Easter":						easter(year=2017),
			"Mother's Day":					date(year,5,1) + fd(weekday=SU(2)),
			"Father's Day":					date(year,6,1) + fd(weekday=SU(3)),
			"Canada Day":					date(year,7,1),
			"Labour Day":					date(year,9,1) + fd(weekday=MO(1)),
			"Thanksgiving":					date(year,10,1) + fd(weekday=MO(2)),
			"Halloween":					date(year,10,31),
			"Christmas Eve":				date(year,12,24),
			"Christmas":					date(year,12,25),
			"New Year's Eve":				date(year,12,31),
		},
		"UK": {
			"New Years Day": 				date(year,1,1),
			"Valentine's Day":				date(year,2,14),
			"Easter":						easter(year=2017),
			"Mother's Day":					date(year,5,1) + fd(weekday=SU(2)),
			"Father's Day":					date(year,6,1) + fd(weekday=SU(3)),
			"Halloween":					date(year,10,31),
			"Christmas Eve":				date(year,12,24),
			"Christmas":					date(year,12,25),
			"Boxing Day":					date(year,12,26),
			"New Year's Eve":				date(year,12,31),
		}
	}
	return DATES

def get_holiday(date, location):
	dates = holiday_dates(date.year)

	current_holiday = [name for name, h_date in dates[location].items() if h_date == date]
	if len(current_holiday) == 0:
		current_holiday = None

	# this is broken for now
	next_holiday = next(name for name, h_date in dates[location].items() if h_date > date.today())
	return current_holiday, next_holiday

class Holiday(Entity):
	""" Representation of the current holiday """

	def __init__(self, hass):
		self.hass = hass
		self.date = date.today()
		self.holiday = get_holiday(self.date, "US")

	@property
	def name(self):
		"""Return the name."""
		return "Holiday"

	@property
	def state(self):
		"""Return the current holiday."""
		return ", ".join(self.holiday[0])

	@property
	def device_state_attributes(self):
		"""Add platform specific attributes."""
		return {'next_holiday': self.holiday[1]}

	def update(self):
		"""Update holiday."""
		self.datetime = date.today()
		self.holiday = get_holiday(self.date, "US")