from gc import collect
import requests
from nft import NFT
from typing import Tuple, Optional, List

from util import Timer, stack_trace
from repo import Repository

class Scraper:
	repo = None
	
	@staticmethod
	def set_repo(repo: Repository):
		Scraper.repo = repo
	@staticmethod
	def get_nfts() -> Tuple[Optional[List[NFT]], Optional[str]]:
		timer = Timer()
		print('getting nfts')

		url = 'https://ksfclzmasu.medianet.work/nft_for_sale?collection='+Scraper.repo.get_collection()

		try:
			res = requests.get(url, timeout=7)
			if res.status_code != 200:
				return None, f'status not 200: {res.status_code}\n{res.content[:300]}'
		except Exception as e:
			return None, stack_trace(e)

		nfts = None
		try:
			nfts = NFT.schema().loads(res.content, many=True)
		except Exception as e:
			return None, stack_trace(e)

		print(f'finished getting nfts {timer.time():.2f}s')

		return nfts, None
	