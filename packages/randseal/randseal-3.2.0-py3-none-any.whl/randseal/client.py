"""Client file"""

from .iters import imgsITER
from .protocols import AsyncFileOrPathLike, FileOrPathLike, FileLike, EmbedLike
import aiohttp
import aiofiles
from datetime import datetime
from io import BytesIO, TextIOWrapper
import json
import asyncio
import random
import advlink
import time
from .errors import StatusException, BaseException, WhatException
from typing import overload, Literal
from os import PathLike
import os
from aiofiles.threadpool.text import AsyncTextIOWrapper
from .vars import MAX_NUMBER, BLANK

class Client:
	"""
	The :class:`Client` class for this package.

	Parameters
	-----------

	session: :class:`aiohttp.ClientSession`
		The main session used to obtain seal images (`auto_decompress=False`). You can input this or the package can create one.

	session2: :class:`aiohttp.ClientSession`
		The secondary session that is currently not used for anything. You can input this or the package can create one.

	loop: :class:`asyncio.AbstractEventLoop`
		The loop used for both sessions. You can input this or the package can create one.

	Attributes
	-----------

	advlink: :class:`advlink.URL`
		An :class:`advlink.URL` containing a seal image url.

	url: :class:`str`
		A simple :class:`str` containing a seal image url.
	
	number: :class:`str`
		A number between 1 and `MAX_NUMBER`, used for getting a seal image by the package.
	"""
	def __init__(self, *, session: aiohttp.ClientSession | None = None, session2: aiohttp.ClientSession | None = None, loop: asyncio.AbstractEventLoop | None = None):
		self.loop = asyncio.get_event_loop() or loop
		self.session = aiohttp.ClientSession(
			auto_decompress=False, loop=self.loop) or session
		self.session2 = aiohttp.ClientSession(loop=self.loop) or session2

	async def File(self, cls: FileLike) -> FileLike:
		"""
		Returns an `File` of a seal which can be used in a message (reworked in version 3.0.0)

		Parameters
		-----------

		cls: :class:`FileLike`
			A py-cord `File` or a discord.py `File`
		"""
		async with self.session.get(self.url) as r:
			if r.status == 200:
				hi = BytesIO(await r.read())
				return cls(fp=hi, filename=self.number + ".jpg")
			else:
				await self.on_error(StatusException)

	def Embed(self, cls: EmbedLike) -> EmbedLike:
		"""
		Returns an `Embed` of a seal which can be edited or used in a message (reworked in version 3.0.0)

		Parameters
		-----------

		cls: :class:`EmbedLike`
			A py-cord `Embed` or a discord.py `Embed`
		"""
		return cls(colour=BLANK).set_image(url=self.url)


	@classmethod
	async def jsonload(cls, fp: AsyncFileOrPathLike, **kwds,) -> dict:
		"""
		Asynchronous `json.load()` using the `aiofiles` package (New in 1.3.0)
		"""
		if isinstance(fp, AsyncTextIOWrapper):
			s = await fp.read()
		else:
			if not os.path.exists(fp):
				async with aiofiles.open(fp, "w") as f:
					s = "{}"
					await f.write(s)
			else:
				async with aiofiles.open(fp) as f:
					s = await f.read()
		return json.loads(s)

	@classmethod
	async def jsondump(
			cls,
			obj: dict,
			fp: AsyncFileOrPathLike,
			**kwds
	) -> None:
		"""
		Asynchronous `json.dump()` using the `aiofiles` package (New in 1.3.0)
		"""
		if isinstance(fp, AsyncTextIOWrapper):
			e = json.dumps(obj, **kwds)
			await fp.write(e)
		else:
			async with aiofiles.open(fp, "w") as f:
				e = json.dumps(obj, **kwds)
				await f.write(e)

	@classmethod
	async def jsonupdate(cls, fp: AsyncFileOrPathLike, data: dict, **dumping_kwargs) -> dict:
		"""
		A combination of `.jsondump` and `.jsonload` to update json files asynchronously. Returns the updated :class:`dict`.
		"""
		e = await cls.jsonload(fp)
		e.update(data)
		await cls.jsondump(e, fp, **dumping_kwargs)
		return e

	@classmethod
	def sync_jsonupdate(cls, fp: FileOrPathLike, data: dict, **dumping_kwargs) -> dict:
		"""
		A non-asynchronous version of `Client.jsonupdate`.
		"""
		if isinstance(fp, TextIOWrapper):
			pf = fp
		else:
			if not os.path.exists(fp):
				with open(fp, "w") as f:
					f.write("{}")
					return {}
			else:
				with open(fp) as f:
					pf = f
		e: dict = json.load(pf)
		e.update(data)
		json.dump(e, pf, **dumping_kwargs)
		return e

	def __hash__(self) -> int:
		return hash(self)

	def __eq__(self, __o: object) -> bool:
		return hash(self) == hash(__o)

	def __ne__(self, __o: object) -> bool:
		return not self.__eq__(__o)

	@property
	def advlink(self) -> advlink.Link:
		"""
		An :class:`advlink.Link` containing a seal image url
		"""
		return advlink.Link(self.url, session=self.session, session2=self.session2)

	@property
	def url(self) -> str:
		"""
		A seal image url
		"""
		return f"https://raw.githubusercontent.com/mariohero24/randsealimgs/main/{self.number}.jpg"


	@property
	def number(self) -> str:
		"""
		A seal number
		"""
		return f"{random.randrange(0, MAX_NUMBER)}"

	def __str__(self):
		return self.url

	def __int__(self):
		return int(self.number)

	def urls(self, *, limit: int = MAX_NUMBER, url: bool=True) -> imgsITER:
		"""
		Returns an :class:`AsyncIterator` for every seal image.

		Parameters
		-----------

		url: :class:`bool`
			If set to ``False``, :class:`bytes` are returned instead of :class:`str`. Defaults to ``True``.
		
		limit: :class:`int`
			How many seal images to return. Defaults to `MAX_NUMBER`.

		Examples
		-----------
		```py
		# Using for loop
		async for url in urls():
			print(url)

		# Flattening into a list
		urlist = await urls().flatten()
		print(urlist)
		```
		"""
		return imgsITER(url=url, session=self.session, limit=limit)

	async def tobytes(self, bytesio: bool=False) -> bytes | BytesIO | None:
		async with self.session.get(self.url) as r:
			if r.status == 200:
				if bytesio:
					n = await r.read()
					hi = BytesIO(n)
				else:
					hi = await r.read()
				return hi
			else:
				await self.on_error(StatusException)

	async def on_error(self, exception: BaseException) -> None:
		"""
		Error handler that can be overridden via subclassing `Client`.

		Parameters
		-----------

		exception: :class:`BaseException`
			The exception that was encountered. Can be determined using `isinstance(exception, {example})`.
		"""
		if isinstance(exception, BaseException):
			raise WhatException()
		else:
			raise exception

# python3 -m twine upload --repository pypi dist/*