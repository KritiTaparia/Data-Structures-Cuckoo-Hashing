# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash24:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.bucket_size = 4
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def get_rand_idx_from_bucket(self, bucket_idx: int, table_id: int) -> int:
		# you must use this function when you need to displace a random key from a bucket during insertion (see the description in requirements.py). 
		# this function randomly chooses an index from a given bucket for a given table. this ensures that the random 
		# index chosen by your code and our test script match.
		# 
		# for example, if you are inserting some key x into table 0, and hash_func(x, 0) returns 5, and the bucket in index 5 of table 0 already has 4 elements,
		# you will call get_rand_bucket_index(5, 0) to determine which key from that bucket to displace, i.e. if get_random_bucket_index(5, 0) returns 2, you
		# will displace the key at index 2 in that bucket.
		rand.seed(int(str(bucket_idx) + str(table_id)))
		return rand.randint(0, self.bucket_size-1)

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[List[int]]]]:
		# the buckets should be implemented as lists. Table cells with no elements should still have None entries.
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		# TODO
		threshold = self.CYCLE_THRESHOLD
		table_index = 0 		#start with chedking h0
		while threshold >= 0:
			h = self.hash_func(key, table_index)
			if self.tables[table_index][h] is None:
				self.tables[table_index][h] = [key]
				return True
			if len(self.tables[table_index][h]) != self.bucket_size:   #is not already full
				self.tables[table_index][h].append(key)
				return True

			displace_position = self.get_rand_idx_from_bucket(h, table_index)
			displaced_value = self.tables[table_index][h][displace_position]
			
			self.tables[table_index][h][displace_position] = key
	
			table_index = 1 - table_index
			key = displaced_value
			threshold -= 1

		return False

	def lookup(self, key: int) -> bool:
		# TODO
		h0 = self.hash_func(key, 0)    #key as per table 0 hash function
		h1 = self.hash_func(key, 1)	   #key as per table 1 hash function
		if (self.tables[0][h0] is None and self.tables[1][h1] is None) or (key not in (self.tables[0][h0] or []) and key not in (self.tables[1][h1], [])):    #if doesn't exist in both tables then return false
			return False
		return True
		

	def delete(self, key: int) -> None:
		# TODO
		h0 = self.hash_func(key, 0)
		h1 = self.hash_func(key, 1)
		if key in self.tables[0][h0]:  #found in first table
			self.tables[0][h0].remove(key)
			if self.tables[0][h0] == []:
				self.tables[0][h0] = None
		elif key in self.tables[1][h1]:  #found in second table
			self.tables[1][h1].remove(key)
			if self.tables[0][h0] == []:
				self.tables[0][h0] = None

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		# TODO
				#track previously mapped keys
		keys = []
		for i in range(2):
			for j in self.tables[i]:
				if j:
					for key in j:
						keys.append(key)
		#initialize table with new size
		self.tables = [[None]*new_table_size for _ in range(2)]

		#rehash these keys into new table
		for i in keys:  
			self.insert(i)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


