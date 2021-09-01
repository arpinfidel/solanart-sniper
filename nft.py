import dataclasses
from dataclasses_json import dataclass_json
from enum import Enum
from typing import Optional, List, Any

@dataclass_json()
@dataclasses.dataclass
class NFT:
	id: int
	token_add: str
	number: int
	currency: str
	price: float
	link_img: str
	for_sale: int
	name: str
	description: str
	escrowAdd: str
	seller_address: str
	attributes: str
	skin: Optional[str]
	type: Optional[str]
	ranking: Optional[str]
	buyerAdd: Optional[str]
	blockhash: Optional[str]
	lastSoldPrice: Optional[float]
	programId: str
	attributes_list: List[str] = dataclasses.field(init=False)
	name_number: int = dataclasses.field(init=False)

	def __post_init__(self):
		self.name_number = int(self.name.split('#')[-1])
		self.attributes_list = [a.strip() for a in self.attributes.split(',')]
		# self.attributes_list = badger_attributes[self.name_number]

