from random import randint, sample
import sys

INT_MAX = float('inf')
V = 50  # Количество городов
START = 0  # Начальный город
POP_SIZE = 10  # Размер популяции

class Individual:
    def __init__(self) -> None:
        self.gnome = []
        self.fitness = 0

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

def rand_num(start, end):
    return randint(start, end-1)

def print_matrix(matrix):
    for row in matrix:
        print(row)

def mutated_gene(gnome):
    gnome = list(gnome)
    while True:
        r = rand_num(1, V)
        r1 = rand_num(1, V)
        if r1 != r:
            gnome[r], gnome[r1] = gnome[r1], gnome[r]
            break
    return gnome

def create_gnome():
    gnome = list(range(1, V))  # Список городов, исключая стартовый город
    sample(gnome, len(gnome))  # Перемешивание списка городов
    gnome.insert(0, START)  # Добавление стартового города в начало
    gnome.append(START)  # Добавление стартового города в конец
    return gnome

def cal_fitness(gnome, mp):
    f = 0
    for i in range(len(gnome) - 1):
        if mp[gnome[i]][gnome[i + 1]] == INT_MAX:
            return INT_MAX
        f += mp[gnome[i]][gnome[i + 1]]
    return f



def crossover(parent1, parent2):
    child_p1 = []
    child_p2 = []

    geneA = rand_num(1, V)
    geneB = rand_num(1, V)

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        if i < len(parent1):
            child_p1.append(parent1[i])

    child_p2 = [item for item in parent2 if item not in child_p1 and item != START]

    child = [START] + child_p1 + child_p2 + [START]
    return child

def generate_distance_matrix(size):
    matrix = [[0 if i == j else rand_num(1, 20) for j in range(size)] for i in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            if matrix[i][j] == matrix[j][i]:
                continue
            value = rand_num(1,40)
            matrix[i][j] = value
            matrix[j][i] = value
    return matrix

def TSPUtil(mp):
    gen = 1
    gen_thres = 10

    population = []
    best_gnome = None
    best_fitness = float('inf')

    for _ in range(POP_SIZE):
        temp = Individual()
        temp.gnome = create_gnome()
        temp.fitness = cal_fitness(temp.gnome, mp)
        population.append(temp)


    while gen <= gen_thres:
        population.sort()
        new_population = []

        for i in range(POP_SIZE):
            parent1 = population[rand_num(0, POP_SIZE)].gnome
            parent2 = population[rand_num(0, POP_SIZE)].gnome
            child_gnome = crossover(parent1, parent2)

            if rand_num(0, 10) < 5:
                child_gnome = mutated_gene(child_gnome)

            new_gnome = Individual()
            new_gnome.gnome = child_gnome
            new_gnome.fitness = cal_fitness(new_gnome.gnome, mp)

            new_population.append(new_gnome)

        population = new_population
        print("Поколение", gen)
        best_gnome = None
        best_fitness = float('inf')
        for ind in population:
            print(ind.gnome, ind.fitness)
            if ind.fitness < best_fitness:
                best_fitness = ind.fitness
                best_gnome = ind.gnome
        print("Лучший маршрут в поколении", gen, ":", best_gnome, "Длина:", best_fitness)
        gen += 1

if __name__ == "__main__":
    mp = generate_distance_matrix(V)
    print("Матрица весов:")
    print_matrix(mp)
    TSPUtil(mp)
