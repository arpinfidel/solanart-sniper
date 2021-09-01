import time
import os
import sys

class Timer:
	def __init__(self):
		self.last = [time.perf_counter()]
	def time(self, idx=-1):
		diff = time.perf_counter()-self.last[idx]
		self.last.append(time.perf_counter())
		return diff

def stack_trace(e):
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	return f'{exc_type} {exc_obj} "./{fname}", line {exc_tb.tb_lineno}\n{e}'
