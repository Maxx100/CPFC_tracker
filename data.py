import json
from datetime import datetime
from time import time


class LogFood:
	def __init__(self, *args):
		if len(args) == 2:
			self.name = args[0]
			self.cal = int(args[1])
			self.datetime = datetime.now()
			self.id = time()
		else:
			temp = args[0].split("|")
			self.name = temp[1]
			self.cal = int(temp[2])
			self.datetime = datetime.fromisoformat(temp[0])
			self.id = float(temp[3])

	def __str__(self):
		return f"{str(self.datetime)}|{self.name}|{str(self.cal)}|{str(self.id)}"

	def beauty_str(self):
		temp = f"{self.datetime.day}.{self.datetime.month}.{self.datetime.year} "
		temp += f"{self.datetime.hour}:{self.datetime.minute}: "
		temp += f"{self.name}, {str(self.cal)}гр"
		return temp

	def __dict__(self):
		return {
			"name": self.name,
			"cal": self.cal,
			"datetime": self.datetime,
			"id": self.id
		}


class Data:
	def __init__(self):
		self.age = 20
		self.weight = 70
		self.sex = 'man'
		self.height = 170
		self.rate = 1.5
		self.products = {}
		self.history = []
		self.load()

	def load(self):
		with open("user_data.json", "r", encoding='UTF8') as file:
			temp = json.load(file)
			self.age = temp['age']
			self.weight = temp['weight']
			self.sex = temp['sex']
			self.height = temp['height']
			self.rate = temp['rate']
		with open("products.json", "r", encoding='UTF8') as file:
			self.products = json.load(file)
		with open("history.json", "r", encoding='UTF8') as file:
			for i in json.load(file)["0"]:
				self.history.append(LogFood(i))
			self.history = self.history[::-1]

	def save(self, new_data):
		self.age = int(new_data['age'])
		self.weight = int(new_data['weight'])
		self.sex = new_data['sex']
		self.height = int(new_data['height'])
		self.rate = float(new_data['rate'])
		with open("user_data.json", "w") as file:
			json.dump(
				{
					"age": self.age,
					"weight": self.weight,
					"sex": self.sex,
					"height": self.height,
					"rate": self.rate
				}, file
			)

	def add(self, name, cal):
		self.history.append(LogFood(name, cal))
		open("history.json", 'w').close()
		with open("history.json", "w") as file:
			json.dump({"0": self.history}, file, default=str)

	def get_normal_cpfc(self):
		if self.sex == "man":
			mifflin = (10 * self.weight + 6.25 * self.height - 5 * self.age + 5) * self.rate
			benedict = (88.362 + 13.397 * self.weight + 4.799 * self.height - 5.677 * self.age) * self.rate
		else:
			mifflin = (10 * self.weight + 6.25 * self.height - 5 * self.age - 161) * self.rate
			benedict = (447.593 + 9.247 * self.weight + 3.098 * self.height - 4.33 * self.age) * self.rate
		middle = (mifflin + benedict) // 2
		return (
			int(middle),
			int(middle / 2000 * 90),  # 0.3
			int(middle / 2000 * 60),  # 0.25
			int(middle / 2000 * 250)  # 0.45
		)


data = Data()
