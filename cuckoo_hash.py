# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[int]]]:
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		# TODO
		threshold = self.CYCLE_THRESHOLD
		table_index = 0 		#start with chedking h0
		while threshold >= 0:
			h = self.hash_func(key, table_index)
			print(key, h, table_index)
			displaced_value = self.tables[table_index][h]
			
			self.tables[table_index][h] = key
			if displaced_value is None:  #table was not already occupied
				return True
			table_index = 1 - table_index
			key = displaced_value
			threshold -= 1

		return False

	def lookup(self, key: int) -> bool:
		# TODO
		h0 = self.hash_func(key, 0)    #key as per table 0 hash function
		h1 = self.hash_func(key, 1)	   #key as per table 1 hash function
		if self.tables[0][h0] != key and self.tables[1][h1] != key:    #if doesn't exist in both tables then return false
			return False
		return True
		

	def delete(self, key: int) -> None:
		# TODO
		h0 = self.hash_func(key, 0)
		h1 = self.hash_func(key, 1)
		if self.tables[0][h0] == key:  #found in first table
			self.tables[0][h0] = None
		elif self.tables[1][h1] == key:  #found in second table
			self.tables[1][h1] = None


	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		# TODO
		#track previously mapped keys
		keys = []
		for i in range(2):
			for key in self.tables[i]:
				if key is not None: keys.append(key)
		#initialize table with new size
		self.tables = [[None]*new_table_size for _ in range(2)]

		#rehash these keys into new table
		for i in keys:  
			self.insert(i)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


