from deap import base, creator, tools, algorithms
import random

# https://deap.readthedocs.io/en/master/index.html
class PricingGAService:
    def __init__(self, customer_loyalty, weather_condition, day_of_week, remoteness, base_price, loyalty_discount, weather_surcharge, weekend_surcharge, remoteness_surcharge):
        # Dynamic parameters
        self.customer_loyalty = customer_loyalty
        self.weather_condition = weather_condition
        self.day_of_week = day_of_week
        self.remoteness = remoteness

        # static constants provide baseline
        self.BASE_PRICE = base_price
        self.LOYALTY_DISCOUNT = loyalty_discount
        self.WEATHER_SURCHARGE = weather_surcharge
        self.WEEKEND_SURCHARGE = weekend_surcharge
        self.REMOTENESS_SURCHARGE = remoteness_surcharge

        self.setup_ga()

    def setup_ga(self):
        # Clear existing classes if they exist
        if "FitnessMax" in creator.__dict__:
            del creator.FitnessMax
        if "Individual" in creator.__dict__:
            del creator.Individual

        # random.seed(43)

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_float", random.uniform, 0.8, 1.2)  # Modifiers between 80% and 120%
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_float, n=5)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("evaluate", self.calculate_price)
        self.toolbox.register("mate", tools.cxBlend, alpha=0.1)
        self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.1, indpb=0.1)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    # dynamic modifiers
    def calculate_price(self, individual):
        price = self.BASE_PRICE
        price *= individual[0]
        
        if self.customer_loyalty:
            price -= price * individual[1] * self.LOYALTY_DISCOUNT
        else:
            price *= individual[1]

        price *= individual[2] * self.WEATHER_SURCHARGE if self.weather_condition == "bad" else 1
        price *= individual[3] * self.WEEKEND_SURCHARGE if self.day_of_week >= 5 else 1
        price *= individual[4] * self.REMOTENESS_SURCHARGE if self.remoteness else 1
        
        return price,

    def enforce_bounds(self, individual):
        for i in range(len(individual)):
            individual[i] = max(0.8, min(1.2, individual[i]))
        return individual

    # https://github.com/betterenvi/XGBoost-Homework/blob/master/MyGA.py
    def run(self):
        population_size = 100
        num_generations = 50

        population = self.toolbox.population(n=population_size)

        for gen in range(num_generations):
            offspring = self.toolbox.select(population, len(population))
            offspring = list(map(self.toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < 0.5:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < 0.2:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

            for individual in offspring:
                self.enforce_bounds(individual)

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            population[:] = offspring

        best_ind = tools.selBest(population, 1)[0]
        best_price = self.calculate_price(best_ind)[0]

        return best_ind, best_price
