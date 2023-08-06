class BaseException(Exception):
	"""Base error for all thing that happen in this library."""

class StatusException(BaseException):
	"""Exception for if a HTTP status isn't 200."""
	def __init__(self):
		super().__init__(f"The HTTP status wasn't 200.")

class WhatException(BaseException):
	"""What are you even trying to do..."""
	def __init__(self):
		super().__init__("You are attempting something very strange.")