from util import stack_trace

import pickle
from typing import Optional, Iterable, Any, Set
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
		self.target_attributes = SyncSet('targets')
		self.target_attributecount = SyncSet('targetcount')
		self.collection = 'degenape'
		self.collection_lock = RLock()

		self.__load_sent()
		self.__load_target_attributes()
		self.__load_target_attributecount()
		self.__load_collection()
	
	def __load_sent(self) -> Optional[str]:
		try:
			with open('sent.pkl', 'rb') as f:
				self.sent = SyncSet('sent', pickle.load(f))
		except Exception as e:
			return stack_trace(e)
		return None
	
	def __load_target_attributes(self) -> Optional[str]:
		try:
			with open('targets.pkl', 'rb') as f:
				self.target_attributes = SyncSet('targets', pickle.load(f))
		except Exception as e:
			return stack_trace(e)
		return None

	def __load_target_attributecount(self) -> Optional[str]:
		try:
			with open('targetcount.pkl', 'rb') as f:
				self.target_attributecount = SyncSet('targetcount', pickle.load(f))
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
		
