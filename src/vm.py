"""
Thats the PBytes VM or for short, PBVM.
it's a simple and very minimal bytecode vm, which can be used as a base for a prgramming language
or a bytecode VM
"""
import bson

# A Simple way of creating memory
class Stack:
	def __init__(self):
		
		self.arr = []
		
	def empty(self):

		return len(self.arr) == 0

	def pop(self):

		if self.empty():
			print("Cannot pop value from empty stack")
		return self.arr.pop()

	def push(self, val):
		self.arr.append(val)


# parse bytecode
class Parser():
	def __init__(self, code):
		self.aCode = code
		self.code = code["code"]
		self.constants = code["constants"]
		self.opcodes = {
			0xF1: [self._i_ldv_, "LOAD_VALUE"],
			0xF2: [self._i_ldc_, "LOAD_CONST"],
			0xF3: [self._i_cifn_, "CALL_FUNC"],
			0xF4: [self._i_mthf_, "MATH_FUNC"],
			0xF5: [self._i_fndef_, "DEF_FUNC"],
			0xF6: [self._i_fnrun_, "RUN_FUNC"],
			0xF7: [self._i_vrdef_, "DEFN_VAR"],
			0xF8: [self._i_vrld_, "LOAD_VAR"],
			0xF9: [self._i_vrdl_, "DEL_VAR"],
			0xFA: [self._i_cmp_, "COMPARE"],
			0xFF: [self._i_exit_, "EXIT_CODE"]
		}
		self.vars = {}
		self.functions = {}
		self.ip = 0
		self.memory = Stack()

	def _run(self):
		try:
			self._parse_text_(self.code)
		except RecursionError:
			print("\nRecursion depth exceeded")
			exit(0)

	def _i_ldv_(self, n):
		self.memory.push(n)

	def _i_ldc_(self, c):
		self.memory.push(self.constants[c])

	def _i_pop_(self, a):
		self.memory.pop()

	def _i_cifn_(self, f):
		if f == 1:
			print(self.memory.pop(), end="")
		if f == 2:
			self.memory.push(input())

	def _i_mthf_(self, o):
		if o == 1:
			self.memory.push(self.memory.pop() + self.memory.pop())
		if o == 2:
			self.memory.push(self.memory.pop() - self.memory.pop())
		if o == 3:
			self.memory.push(self.memory.pop() * self.memory.pop())
		if o == 4:
			self.memory.push(self.memory.pop() / self.memory.pop())
			
	def _i_fndef_(self, c):
		self.functions[c[0]] = c[1]
		
	def _i_fnrun_(self, n):
		code = self.functions[n]
		
		self._parse_text_(code)

	def _i_vrdef_(self, n):
		self.vars[n] = self.memory.pop()
		
	def _i_vrld_(self, n):
		self.memory.push(self.vars[n])

	def _i_vrdl_(self, n):
		self.vars.pop(n)

	def _i_cmp_(self, c):
		m = c[0]
		true = c[1]
		false = 0

		try:
			false = c[2]
		except:
			false = ["0xf2", -1]
			
		if m == 1:
			if self.memory.pop() == self.memory.pop():
				self._parse_text_(true)
			else:
				self._parse_text_(false)
		elif m == 2:
			if self.memory.pop() != self.memory.pop():
				self._parse_text_(true)
			else:
				self._parse_text_(false)
		elif m == 3:
			if self.memory.pop() > self.memory.pop():
				self._parse_text_(true)
			else:
				self._parse_text_(false)
		elif m == 4:
			if self.memory.pop() < self.memory.pop():
				self._parse_text_(true)
			else:
				self._parse_text_(false)

	def _i_exit_(self, c):
		exit(c)

	def _parse_text_(self, text, ):
		for codePart in text:

			opcode = int(''.join(codePart[0]), base=0)
			oparg = 0
			try:
				oparg = codePart[1]
			except:
				oparg = 0

			if opcode in self.opcodes:
				self.opcodes[opcode][0](oparg)

def _bytecode_to_dict_(filename):
	file = open(filename, "rb")
	filec = file.read()

	jsonfile = bson.loads(filec)
	file.close()
	return jsonfile

def _dict_to_bytecode_(filename):
	pass