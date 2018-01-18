import hashlib
import json
from time import time
from uuid import uuid4

"""	Accounts format
	key = 'address'
	value = 'balances'
	Address format = Rhc.......

block = {
	'index': 1,
	'timestamp': 234.912,
	'transactions': [
		{
			'sender': 0x,
			'recipient': 0x1,
			'amount': 500
		},
		{
			'sender': 0x2,
			'recipient': 0x3,
			'amount': 600
		}
	],
	'proof': 23412310000,
	'previous_hash': 123123
}

"""


class Blockchain():
	def __init__(self):
		self.chain = []
		self.current_transactions = []
		self.accounts = {}
		# we must create a genesis block
		self.new_block(previous_hash=1, proof=100)

	def __apply_balances(self):
		for tx in self.current_transactions:
			try:
				sender = tx['sender']
				recipient = tx['recipient']
				amount = tx['amount']
				self.accounts[sender] -= amount
				self.accounts[recipient] += amount
			except KeyError as e:
				print('invalid address used')

	def init_account(self, name):
		account_hash = "Rhc" + hashlib.sha256(name.encode()).hexdigest()
		assert account_hash not in self.accounts.keys()
		self.accounts[account_hash] = 1

	def new_block(self, proof, previous_hash=None):
		# creates a new block
		# proof = priven given by PoW algo
		# previous_hash (optional) Hash of previous block
		block = {
			'index': len(self.chain),
			'timestamp': time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1])
		}
		if len(self.current_transactions) > 0:
			self.__apply_balances()
		self.current_transactions = []
		self.chain.append(block)
	

	def new_transaction(self, sender, recipient, amount):
		# creates a new transaction
		# returns the index of the block that will contain this tx
		self.current_transactions.append({
			'sender': sender,
			'recipient': recipient,
			'amount': amount
			})
		return self.last_block['index'] + 1


	def proof_of_work(self, last_proof):
		proof = 0
		while self.valid_proof(last_proof, proof) is False:
			proof += 1
		return proof

	def balanceOf(self, address):
		return self.accounts[address]

	@staticmethod 
	def valid_proof(last_proof, proof):
		guess = f'{last_proof}{proof}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"

	@staticmethod # knows nothing of the class
	def hash(block):
		# hashes a block
		block_string = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()

	@property
	def last_block(self):
		# returns the last block of the blockchain
		return self.chain[-1]


"""

block = {
	'index': 1,
	'timestamp': 234.912,
	'transactions': [
		{
			'sender': 0x,
			'recipient': 0x1,
			'amount': 500
		},
		{
			'sender': 0x2,
			'recipient': 0x3,
			'amount': 600
		}
	],
	'proof': 23412310000,
	'previous_hash': 123123
}

"""