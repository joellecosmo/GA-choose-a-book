import geneticalgo_books
import geneticalgo_crossover as crossover
import random


weights = [5, 2, 3, 4, 1]


def calculate_fitness(chromosome, user_chromosome):
    return sum(w * (int(gene) == int(user_gene)) for w, gene, user_gene in zip(weights, chromosome, user_chromosome))


def roulette_wheel_selection(population, fitness_scores):
    max_fit = sum(fitness_scores)
    pick = random.uniform(0, max_fit)
    current = 0
    for idx, score in enumerate(fitness_scores):
        current += score
        if current >= pick:
            return population[idx]


def crossover(parent1, parent2):
    midpoint = len(parent1) // 2
    child1 = parent1[:midpoint] + parent2[midpoint:]
    child2 = parent2[:midpoint] + parent1[midpoint:]
    return child1, child2


def mutate(chromosome):
    mutation_point = random.randint(0, len(chromosome) - 1)
    mutated = list(chromosome)
    mutated[mutation_point] = '0' if mutated[mutation_point] == '1' else '1'
    return ''.join(mutated)


def user_preferences():
    user_prefs = {
        "knowledge area": "",
        "attractiveness": "",
        "over_300": "",
        "project importance": "",
        "author importance": ""
    }
    print("Enter your preferences for the following:")
    user_prefs["knowledge area"] = input(
        "Knowledge area (history, poetry, education, religion, human development, novel, computer science): ")
    user_prefs["attractiveness"] = input("Do you want an attractive book? (yes/no): ")
    user_prefs["over_300"] = input("Do you want it to be over 300 pages? (yes/no): ")
    user_prefs["project importance"] = input("Should it be important for your project? (yes/no): ")
    user_prefs["author importance"] = input("Do you want the author to be unknown, slightly famous, or famous? ")
    return user_prefs


def transform_userprefs(user_prefs):
    knowledge_mapping = {
        "history": "001",
        "poetry": "010",
        "education": "011",
        "religion": "100",
        "human development": "101",
        "novel": "110",
        "computer science": "111"
    }
    user_prefs["knowledge area"] = knowledge_mapping.get(user_prefs["knowledge area"].lower(), "")
    user_prefs["attractiveness"] = "1" if user_prefs["attractiveness"].lower() == "yes" else "0"
    user_prefs["over_300"] = "1" if user_prefs["over_300"].lower() == "yes" else "0"
    user_prefs["project importance"] = "1" if user_prefs["project importance"].lower() == "yes" else "0"
    author_mapping = {
        "unknown": "00",
        "slightly famous": "01",
        "famous": "10"
    }
    user_prefs["author importance"] = author_mapping.get(user_prefs["author importance"].lower(), "")
    return ''.join(user_prefs.values())


def main():
    user_prefs = user_preferences()
    user_chromosome = transform_userprefs(user_prefs)

    population = [book["attributes"] for book in geneticalgo_books.books]
    generations = 10
    best_books = []

    for generation in range(generations):
        fitness_scores = [calculate_fitness(chromosome, user_chromosome) for chromosome in population]

        # Select best book in current population for reference
        best_index = fitness_scores.index(max(fitness_scores))
        best_books.append(geneticalgo_books.books[best_index])

        # Create new generation
        new_population = []
        while len(new_population) < len(population):
            parent1 = roulette_wheel_selection(population, fitness_scores)
            parent2 = roulette_wheel_selection(population, fitness_scores)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            new_population.append(mutate(child2))

        population = new_population


    print("Best book recommendation based on your preferences:")
    for book in best_books[-1:]:
        print(f"{book['name']} by {book['author']} with attributes {book['attributes']}")


if __name__ == "__main__":
    main()
