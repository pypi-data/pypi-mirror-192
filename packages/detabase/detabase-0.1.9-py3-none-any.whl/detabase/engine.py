__all__ = [
		'get_async_base',
		'get',
		'fetch',
		'fetch_all',
		'update',
		'put',
		'put_many',
		'insert'
]

import datetime
from typing import Union, Optional
from deta import Deta

import os.path

from starlette.config import Config

JsonPrimitive = Union[str, float, int, bool, None]
DetaData = Union[dict, list, str, float, int, bool]
DetaKey = Union[str, None]
ExpireIn = Union[str, None]
ExpireAt = Union[datetime.datetime, int, float, None]
JsonSequence = list[JsonPrimitive]
JsonDict = dict[str, Union[JsonSequence, JsonPrimitive]]
Jsonable = Union[JsonDict, JsonSequence, JsonPrimitive]
DetaQuery = Union[dict[str, JsonPrimitive], list[dict[str, JsonPrimitive]]]

config = Config(os.path.join(os.getcwd(), '.env'))


def get_async_base(table: str):
	return Deta(config.get("DETABASE_PROJECT_KEY", default='DETA_PROJECT_KEY', cast=str)).AsyncBase(table)


async def fetch_all(table: str, query: DetaQuery = None):
	base = get_async_base(table)
	try:
		response = await base.fetch(query=query)
		all_items = response.items
		while response.last:
			response = await base.fetch(last=response.last)
			all_items.extend(response.items)
		return all_items
	finally:
		await base.close()


async def fetch(table: str, query: DetaQuery = None, last: str = None):
	base = get_async_base(table)
	try:
		return await base.fetch(query=query, last=last)
	finally:
		await base.close()


async def get(table: str, key: str):
	base = get_async_base(table)
	try:
		return await base.get(key)
	finally:
		await base.close()


async def put_many(table: str, items: list[Jsonable], expire_in: ExpireIn = None, expire_at: ExpireAt = None):
	base = get_async_base(table)
	processed = dict(items=list())
	failed = dict(items=list())
	try:
		size = len(items) % 20
		gen = (item for item in items)
		while size != 0:
			result = base.put_many(items=[next(gen) for _ in range(20)], expire_in=expire_in, expire_at=expire_at)
			processed['items'].extend(result.get('processed', {}).get('items'))
			failed['items'].extend(result.get('failed', {}).get('items'))
		result = await base.put_many(items=list(gen), expire_in=expire_in, expire_at=expire_at)
		processed['items'].extend(result.get('processed', {}).get('items'))
		failed['items'].extend(result.get('failed', {}).get('items'))
		return {'processed': processed, 'failed': failed}
	finally:
		await base.close()


async def insert(table: str, data: DetaData, key: DetaKey = None, expire_in: ExpireIn = None,
                 expire_at: ExpireAt = None):
	base = get_async_base(table)
	deta_key = data.pop('key', None) or key
	try:
		return await base.insert(data=data, key=deta_key, expire_in=expire_in, expire_at=expire_at)
	except BaseException as e:
		raise e
	finally:
		await base.close()


async def put(table: str, data: DetaData, key: DetaKey = None, expire_in: ExpireIn = None, expire_at: ExpireAt = None):
	base = get_async_base(table)
	deta_key = data.pop('key', None) or key
	try:
		return await base.put(data=data, key=deta_key, expire_in=expire_in, expire_at=expire_at)
	except BaseException as e:
		raise e
	finally:
		await base.close()


async def delete(table: str, key: str):
	base = get_async_base(table)
	try:
		await base.delete(key)
	finally:
		await base.close()


async def update(table: str,
                 key: str,
                 sets: Optional[dict] = None,
                 increments: Optional[dict[str, Union[int, float]]] = None,
                 appends: Optional[dict[str, Union[JsonPrimitive, list]]] = None,
                 prepends: Optional[dict[str, Union[JsonPrimitive, list]]] = None,
                 trims: Optional[list[str]] = None):
	base = get_async_base(table)
	updates = dict()
	if sets:
		for name, value in sets.items():
			updates[name] = value
	if increments:
		for name, value in increments.items():
			updates[name] = base.util.increment(value)
	if appends:
		for name, value in appends.items():
			updates[name] = base.util.append(value)
	if prepends:
		for name, value in prepends.items():
			updates[name] = base.util.prepend(value)
	if trims:
		for name in trims:
			updates[name] = base.util.trim()
	try:
		return await base.update(updates=updates, key=key)
	except BaseException as e:
		raise e
	finally:
		await base.close()
