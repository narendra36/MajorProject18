##########################################################################################
#			       TIME TABLE GENERATION USING GENETIC ALGORITHM                         #
#                                                                                        #
#				   Saurabh Kumar, Sudhanshu Raman, Narendra Dodwaria,                    #
#                  Milindra Pratap Singh, Anshul Chaintha, Vineet Kumar,                 #
#                  Vedant Khachi                                                         #
##########################################################################################

import random
import pprint

class genetic:
	def  __init__(self, classSubjMap, classHourMap):
		self.nPopulation = 10
		self.mutationProb = 0.1
		self.nClasses = len(classSubjMap)
		self.classes = []
		for i in range(0, self.nClasses):
			t1 = list(classSubjMap[i].keys())
			t2 = []
			t3 = []
			for j in t1:
				t2.append(classSubjMap[i][j])
				t3.append(classHourMap[i][j])
			self.classes.append((t1, t2, t3))
		self.population = [[[[-1 for k in range(0,8)] for j in range(0, 5)] for i in range(0, self.nClasses)] for chromo in range (0, self.nPopulation)]
		self.initializePopulation()
		self.generate()
		# pp = pprint.PrettyPrinter(indent=4)
		# pp.pprint(self.population)

	def initializePopulation(self):
		for chromo in range(0, self.nPopulation//2):
			for i in range(0, self.nClasses):
				(x, y) = (0, 0)
				temp = self.classes[i][2][:]
				totalHours = sum(temp)
				while totalHours != 0:
					j = random.randint(0, len(self.classes[i][0])-1)
					if temp[j] != 0:
						self.population[chromo][i][x][y] = j
						temp[j] -= 1
						totalHours -= 1
						x += 1
						if(x == 5):
							y += 1
							x = 0

		for chromo in range(self.nPopulation//2, self.nPopulation):
			for i in range(0, self.nClasses):
				(x, y) = (0, 7)
				temp = self.classes[i][2][:]
				totalHours = sum(temp)
				while totalHours != 0:
					j = random.randint(0, len(self.classes[i][0])-1)
					if temp[j] != 0:
						self.population[chromo][i][x][y] = j
						temp[j] -= 1
						totalHours -= 1
						x += 1
						if(x == 5):
							y -= 1
							x = 0

	def fitness(self, popu):
		fitness = []
		for chromo in range(0, len(popu)):
			conflict = 1
			for x in range(0,5):
				for y in range(0,8):
					temp = []
					for j in range(0, self.nClasses):
						if popu[chromo][j][x][y] != -1:
							t = self.classes[j][1][popu[chromo][j][x][y]]
							if(t in temp):
								conflict += 1
							else:
								temp.append(t)
			fitness.append(1/conflict)
		return fitness

	def cmp(self, a, b):
		t1 = self.fitness([a])
		t2 = self.fitness([b])
		if(t1 > t2):
			return -1
		elif(t1 == t2):
			return 0
		else:
			return 1

	def cmp_to_key(self, mycmp):
	    'Convert a cmp= function into a key= function'
	    class K:
	        def __init__(self, obj, *args):
	            self.obj = obj
	        def __lt__(self, other):
	            return mycmp(self.obj, other.obj) < 0
	        def __gt__(self, other):
	            return mycmp(self.obj, other.obj) > 0
	        def __eq__(self, other):
	            return mycmp(self.obj, other.obj) == 0
	        def __le__(self, other):
	            return mycmp(self.obj, other.obj) <= 0
	        def __ge__(self, other):
	            return mycmp(self.obj, other.obj) >= 0
	        def __ne__(self, other):
	            return mycmp(self.obj, other.obj) != 0
	    return K

	def crossover(self):
		newPop = [[[[-1 for k in range(0,8)] for j in range(0, 5)] for i in range(0, self.nClasses)] for chromo in range (0, self.nPopulation)]
		for chromo in range(0,10,2):
			for i in range(0, self.nClasses):
				for j in range(0, 5):
					x = random.randint(1,6)
					for k in range(0,x+1):
						newPop[chromo][i][j][k] = self.population[chromo][i][j][k]
					for k in range(x+1,8):
						newPop[chromo][i][j][k] = self.population[chromo+1][i][j][k]
					x = random.randint(1,6)
					for k in range(0,x+1):
						newPop[chromo+1][i][j][k] = self.population[chromo+1][i][j][k]
					for k in range(x+1,8):
						newPop[chromo+1][i][j][k] = self.population[chromo][i][j][k]
				self.enforceConstraints(newPop, chromo, i)
				self.enforceConstraints(newPop, chromo+1, i)
		return newPop

	def mutation(self, popu):
		newPop = [[[[-1 for k in range(0,8)] for j in range(0, 5)] for i in range(0, self.nClasses)] for chromo in range (0, self.nPopulation)]
		for chromo in range(0,self.nPopulation):
			for i in range(0, self.nClasses):
				for x in range(0, 5):
					for y in range(0, 8):
						t = random.randint(0,100)
						if(t > 10): # Probabbility of 0.9
							newPop[chromo][i][x][y] = popu[chromo][i][x][y]
						else: # Probablity of 0.1
							newPop[chromo][i][x][y] = random.randint(0, len(self.classes[i][0]) - 1)
				self.enforceConstraints(newPop, chromo, i)
		return newPop

	def enforceConstraints(self, newPop, chromo, index):
		countOfEach = [0 for i in range(0, len(self.classes[index][0]))]
		for j in range(0, 5):
			for k in range(0, 8):
				if(newPop[chromo][index][j][k] != -1):
					countOfEach[newPop[chromo][index][j][k]] += 1
		for i in range(0, len(countOfEach)):
			if(countOfEach[i] > self.classes[index][2][i]):
				t = countOfEach[i] - self.classes[index][2][i]
				for x in range(0, 5):
					status = False
					for y in range(0,8):
						if(newPop[chromo][index][x][y] == i):
							newPop[chromo][index][x][y] = -1
							t -= 1
							if(t==0):
								status = True
								break
					if(status):
						break
			elif(countOfEach[i] < self.classes[index][2][i]):
				t = countOfEach[i] - self.classes[index][2][i]
				for x in range(0,5):
					status = False
					for y in range(0, 8):
						if(newPop[chromo][index][x][y] == -1):
							newPop[chromo][index][x][y] = i
							t -= 1
							if(t == 0):
								status = True
								break
					if(status):
						break

	def generate(self):
		temp = []
		temp1 = []
		for i in range(0,50):
			initFitness = self.fitness(self.population)
			self.population.sort(key=self.cmp_to_key(self.cmp))
			initFitness.sort(reverse=True)
			if(initFitness[0] == 1):
				break
			temp = self.crossover()
			crossoverFitness = self.fitness(temp)
			crossoverFitness.sort(reverse=True)
			temp1 = self.mutation(temp)
			mutationFitness = self.fitness(temp1)
			mutationFitness.sort(reverse=True)
			if(mutationFitness[0] >= crossoverFitness[0]):
				self.population = temp1
			else:
				self.population = temp2

		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(self.population)
		print(self.fitness(self.population))

if __name__ == '__main__':
	genetic([{'a': 1, 'b': 2}, {'c': 1, 'd': 2}], [{'a': 5, 'b': 6}, {'c': 4, 'd': 3}])