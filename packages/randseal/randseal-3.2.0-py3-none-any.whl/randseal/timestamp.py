import time, datetime, enum, typing

class TimeStampType(enum.StrEnum):
	Default = ""
	MONTHNAME_DATE_YEAR_HOUR_MINUTE = Default
	Short_Time = ":t"
	HOUR_MINUTE = Short_Time
	Long_Time = ":T"
	HOUR_MINUTE_SECOND = Long_Time
	Short_Date = ":d"
	MONTH_DATE_YEAR = Short_Date
	Long_Date = ":D"
	MONTHNAME_DATE_YEAR = Long_Date
	Short_Date_Time = ":f"
	Long_Date_Time = ":F"
	WEEKNAME_MONTHNAME_DATE_YEAR_HOUR_MINUTE = Long_Date_Time
	Relative = ":R"

class TimeStamp:

	__slots__ = ("discordtimestamp", "date", "datetime")

	def __init__(self, date: datetime.datetime, _24h: bool=False) -> None:
		self._date = date
		self._24h = _24h

	def discordtimestamp(self, type: TimeStampType = TimeStampType.Default) -> str:
		return f"<t:{time.mktime(self.datetime.timestamp())}{type._value_}>".replace(".0", "")

	@property
	def date(self) -> str:
		if not self._24h:
			return f"{self.datetime.month}/{self.datetime.day}/{self.datetime.year}"
		else:
			return f"{'0' if len(self.datetime.day) == 1 else '' + str(self.datetime.day)}/{'0' if len(self.datetime.month) == 1 else '' + str(self.datetime.month)}/{self._get_year_num(self.datetime.year)}"

	@property
	def datetime(self) -> datetime.datetime:
		return self._date

	@property
	def time(self):
		if self._24h:
			return f"{self.datetime.hour}:{'0' if len(self.datetime.minute) == 1 else '' + str(self.datetime.minute)}"
		else:
			if self.datetime.hour > 12:
				hour = self.datetime.hour - 12
				pm = True
			elif self.datetime.hour == 0:
				hour = 1
				pm = False
			else:
				hour = self.datetime.hour
				pm = False
			return f"{hour}:{'0' if len(self.datetime.minute) == 1 else '' + str(self.datetime.minute) + 'AM' if not pm else 'PM'}"

	@classmethod
	def _get_year_num(cls, __year: int):
		year = str(__year)
		if len(year) == 3:
			return int("0" + year)
		elif len(year) == 2:
			return int("00" + year)
		elif len(year) == 1:
			return int("000" + year)
		else:
			return int(year)