from util import stack_trace
from filter import Filter

import pickle
from typing import Optional, Iterable, Any, Set, List
from threading import RLock

class SyncSet:
	def __init__(self, name: str, s: Set=None) -> None:
		if s is None:
			s = set()
		self.name = name
		self.lock = RLock()
		self.set = s
	def add(self, key) -> None:
		with self.lock:
			self.set.add(key)
			self.__save()
	def __contains__(self, key) -> bool:
		with self.lock:
			return key in self.set
	def copy(self) -> Set[Any]:
		with self.lock:
			return self.set.copy()
	def remove(self, key) -> None:
		with self.lock:
			self.set.remove(key)
			self.__save()
	def __save(self):
		with open(f'{self.name}.pkl', 'wb') as f:
			with self.lock:
				pickle.dump(self.set, f)

class Repository:
	def __init__(self):
		self.sent = SyncSet('sent')
		self.collection = 'degenape'
		self.collection_lock = RLock()
		self.filters:List[Filter] = []

		self.__load_sent()
		self.__load_filters()
		self.__load_collection()
	
	def __load_sent(self) -> Optional[str]:
		try:
			with open('sent.pkl', 'rb') as f:
				self.sent = SyncSet('sent', pickle.load(f))
		except Exception as e:
			return stack_trace(e)
		return None
	
	def __load_filters(self) -> Optional[str]:
		try:
			with open('filters.pkl', 'rb') as f:
				self.filters = pickle.load(f)
		except Exception as e:
			return stack_trace(e)
		return None

	def __load_collection(self) -> Optional[str]:
		try:
			with open('collection.pkl', 'rb') as f:
				with self.collection_lock:
					self.collection = pickle.load(f)
		except Exception as e:
			return stack_trace(e)
		return None

	def get_collection(self) -> str:
		with self.collection_lock:
			return self.collection
		
	def set_collection(self, coll: str) -> None:
		with self.collection_lock:
			self.collection = coll
		with open('collection.pkl', 'wb') as f:
			pickle.dump(coll, f)
	
	def save_filters(self) -> None:
		with open('filters.pkl', 'wb') as f:
			pickle.dump(self.filters, f)
