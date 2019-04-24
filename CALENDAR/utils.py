from datetime import datetime, timedelta
from calendar import HTMLCalendar
import calendar

class Calendar(HTMLCalendar):
	""" This class represents an HTML Calendar
	"""
	def __init__(self, year=None, month=None):
		""" Constructor
		:param year: the calendar year
		:param month: the calendar month
		"""
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	def formatday(self, day, events):
		""" Formats a day as a td (html). Filters eventes by day
		:param day: a specific day
		:param events: daily events
		:return: a new html column (day)
		"""
		events_per_day = events.filter(date_start__day=day)
		d = ''
		for event in events_per_day:
			d += f'<li>{event.get_start_time_format}-{event.get_end_time_format} {event.get_html_url}</li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'


	def formatweek(self, theweek, events):
		""" Formats a week as a tr (html).
		:param theweek: current week
		:param events: weekly events
		:return: a new html row (week)
		"""
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'


	def formatmonth(self, events, withyear=True):
		""" Formats a month as a table. Filters events by year and month
		:param events: the list of events
		:param withyear: current year
		:return: a new html table
		"""
		# events = self.request.user.user_meetings.filter(date_start__year=self.year, date_start__month=self.month)
		# events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal


def get_date(req_day):
	""" Returns the current date
	:param req_day: current day
	:return: current date in datetime format
	"""
	if req_day:
		year, month = (int(x) for x in req_day.split('-'))
		return datetime(year, month, day=1)
	return datetime.today()

def prev_month(date):
	""" Returns the previous month
	:param date: current date
	:return: A string that represents the previous month
	"""
	first = date.replace(day=1)
	prev_month = first - timedelta(days=1)
	month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
	return month

def next_month(date):
	""" Returns the next month
	:param date: current date
	:return: A string that represents the next month
	"""
	days_in_month = calendar.monthrange(date.year, date.month)[1]
	last = date.replace(day=days_in_month)
	next_month = last + timedelta(days=1)
	month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
	return month