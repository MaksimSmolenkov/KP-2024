from random import randint, sample

INT_MAX = 2147483647
V = 5  # Количество городов
GENES = "ABCDE"  # Имена городов
START = 0  # Начальный город
POP_SIZE = 10  # Размер популяции

class Individual:
    def __init__(self) -> None:
        self.gnome = ""
        self.fitness = 0

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

# Функция для генерации случайного числа в заданном диапазоне
def rand_num(start, end):
    return randint(start, end-1)

# Функция для проверки, повторяется ли символ в строке
def repeat(s, ch):
    return ch in s

# Функция для мутации генома (случайный обмен двух генов)
def mutated_gene(gnome):
    gnome = list(gnome)
    while True:
        r = rand_num(1, V)
        r1 = rand_num(1, V)
        if r1 != r:
            gnome[r], gnome[r1] = gnome[r1], gnome[r]
            break
    return ''.join(gnome)

# Функция для создания начального генома
def create_gnome():
    gnome = "0"
    while True:
        if len(gnome) == V:
            gnome += gnome[0]
            break

        temp = rand_num(1, V)
        if not repeat(gnome, chr(temp + 48)):
            gnome += chr(temp + 48)

    return gnome

# Функция для вычисления приспособленности (длины пути)
def cal_fitness(gnome, mp):
    f = 0
    for i in range(len(gnome) - 1):
        if mp[ord(gnome[i]) - 48][ord(gnome[i + 1]) - 48] == INT_MAX:
            return INT_MAX
        f += mp[ord(gnome[i]) - 48][ord(gnome[i + 1]) - 48]
    return f

# Функция для снижения температуры
def cooldown(temp):
    return (90 * temp) / 100

# Функция для кроссовера (рекомбинации) двух родителей
def crossover(parent1, parent2):
    child_p1 = ""
    child_p2 = ""

    geneA = int(rand_num(1, V) * len(parent1))
    geneB = int(rand_num(1, V) * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        if i < len(parent1):  # Проверяем, не вышли ли за границы длины генома
            child_p1 += parent1[i]

    child_p2 = [item for item in parent2 if item not in child_p1]

    child = child_p1 + ''.join(child_p2)
    return child

# Основная функция, реализующая генетический алгоритм для TSP
def TSPUtil(mp):
    gen = 1
    gen_thres = 100

    # Инициализация популяции
    population = []
    best_gnome = None
    best_fitness = float('inf')

    for _ in range(POP_SIZE):
        temp = Individual()
        temp.gnome = create_gnome()
        temp.fitness = cal_fitness(temp.gnome, mp)
        population.append(temp)

    print("\nInitial population: \nGNOME     FITNESS VALUE\n")
    for ind in population:
        print(ind.gnome, ind.fitness)
        if ind.fitness < best_fitness:
            best_fitness = ind.fitness
            best_gnome = ind.gnome
    print("Best Gnome in Generation 0:", best_gnome, "Length:", best_fitness)

    temperature = 10000

    # Основной цикл генетического алгоритма
    while temperature > 1000 and gen <= gen_thres:
        population.sort()  # Сортировка популяции по приспособленности
        print("\nCurrent temp: ", temperature)
        new_population = []

        for i in range(POP_SIZE):
            parent1 = population[rand_num(0, POP_SIZE)].gnome
            parent2 = population[rand_num(0, POP_SIZE)].gnome
            child_gnome = crossover(parent1, parent2)  # Кроссовер

            if rand_num(0, 10) < 5:
                child_gnome = mutated_gene(child_gnome)  # Мутация

            new_gnome = Individual()
            new_gnome.gnome = child_gnome
            new_gnome.fitness = cal_fitness(new_gnome.gnome, mp)

            new_population.append(new_gnome)

        temperature = cooldown(temperature)  # Снижение температуры
        population = new_population
        print("Generation", gen)
        print("GNOME     FITNESS VALUE")
        best_gnome = None
        best_fitness = float('inf')
        for ind in population:
            print(ind.gnome, ind.fitness)
            if ind.fitness < best_fitness:
                best_fitness = ind.fitness
                best_gnome = ind.gnome
        print("Best Gnome in Generation", gen, ":", best_gnome, "Length:", best_fitness)
        gen += 1

if __name__ == "__main__":
    mp = [
        [0, 2, INT_MAX, 12, 5],
        [2, 0, 4, 8, INT_MAX],
        [INT_MAX, 4, 0, 3, 3],
        [12, 8, 3, 0, 10],
        [5, INT_MAX, 3, 10, 0],
    ]
    TSPUtil(mp)
