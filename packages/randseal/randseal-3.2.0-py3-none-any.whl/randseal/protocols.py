from typing import Protocol

class FileLike(Protocol):
	"""A :class:`File` from discord or pycord."""

class EmbedLike(Protocol):
	"""An :class:`Embed` from discord or pycord."""

class FileOrPathLike(Protocol):
	"""A :class:`TextIOWrapper` or a :class:`Pathlike`."""

class AsyncFileOrPathLike(Protocol):
	"""An :class:`AsyncTextIOWrapper` or a :class:`Pathlike`."""