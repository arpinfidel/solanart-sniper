from typing import List, Optional, Tuple
from dataclasses import dataclass

from nft import NFT

class Filter:
	@dataclass
	class Match:
		attributes: Optional[Tuple[bool, List[str]]] = None
		attribute_count: Optional[Tuple[bool, int]] = None
		price_threshold: Optional[Tuple[bool, float]] = None

		def __nonzero__(self):
			return all([a is None or a[0] for a in [getattr(self, an) for an in dir(self) if not an.startswith('__')] if not callable(a)])
		__bool__ = __nonzero__
		def as_dict(self):
			names = [an for an in dir(self) if not an.startswith('__')]
			return {n: a[1] for n, a in [(n, getattr(self, n)) for n in names] if not callable(a) and a is not None}

	def __init__(self, channel:str, attributes:List[str] = None, attribute_count:int = None, price_threshold:float = None) -> None:
		self.channel = channel
		self.attributes = attributes
		self.attribute_count = attribute_count
		self.price_threshold = price_threshold
	
	def match(self, nfts: List[NFT]) -> List[Tuple[NFT, Match]]:
		nfts = sorted(nfts, key=lambda n: n.price)
		matches = [(nft, Filter.Match()) for nft in nfts]
		for i, nft in enumerate(nfts):
			if self.attributes is not None:
				matches[i][1].attributes = (all([a in nft.attributes_list for a in self.attributes]), [a for a in nft.attributes_list if a in self.attributes])
			if self.attribute_count is not None:
				matches[i][1].attribute_count = (len(nft.attributes_list)-5 == self.attribute_count, len(nft.attributes_list)-5)
		if self.price_threshold is not None and len(nfts) != 0:
			matched = [n for n, m in matches if m]

			cheapest, ratio = None, 0
			if len(matched)>=2 and matched[0].price <= self.price_threshold * matched[1].price:
				cheapest, ratio = matched[0], matched[0].price/matched[1].price
			for i, (n, _) in enumerate(matches):
				matches[i][1].price_threshold = (n == cheapest, ratio)

		return matches

	def as_dict(self):
		names = [an for an in dir(self) if not an.startswith('__')]
		return {n: a for n, a in [(n, getattr(self, n)) for n in names] if not callable(a) and a is not None}
