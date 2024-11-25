from deap import base, creator, tools, algorithms
import random
import math
from datetime import datetime

class CustomerService:

    def __init__(self):

        # https://deap.readthedocs.io/en/master/api/algo.html
        # https://deap.readthedocs.io/en/master/tutorials/basic/part2.html

        # Delete existing classes
        if "FitnessMin" in creator.__dict__:
            del creator.FitnessMin
        if "Individual" in creator.__dict__:
            del creator.Individual

        # Create Fitnessclass and Individualclass
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        # Create Toolbox for operation and function
        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_float", random.uniform, 0.8, 1.2)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual,self.toolbox.attr_float, n=4)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.evaluate)
        self.toolbox.register("mate", tools.cxBlend, alpha=0.3)
        self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.3)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

# Base price based on time
    def get_dynamic_base_fare(self):
        current_hour = datetime.now().hour
        if 6 <= current_hour < 21:
            return 4.0
        else:
            return 6.0

    def get_car_class_factor(self,car_class):
        if car_class == "standard":
            return 1.0
        elif car_class == "premium":
            return 1.5
        elif car_class == "luxury":
            return 2
        else:
            return 1.0


    def calculate_distance(self, start, destination):
        lat1, lon1 = map(math.radians, start)
        lat2, lon2 = map(math.radians, destination)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        R = 6371.0
        distance = R * c

        return distance

    def get_travel_cost(self, distance, cost_per_km_multiplier):
        base_fare = self.get_dynamic_base_fare()
        cost_per_km = 3 * cost_per_km_multiplier
        if distance <= 10:
            return base_fare + (distance * cost_per_km)
        else:
            cost_for_first_10_km = 10 * cost_per_km
            remaining_distance = distance - 10
            reduced_cost_per_km = cost_per_km * 2.5
            cost_for_remaining_km = remaining_distance * reduced_cost_per_km
            return base_fare + cost_for_first_10_km + cost_for_remaining_km

    def get_remoteness_cost(self, distance):
        return 10 if distance > 10 else 0

    def get_loyalty_discount(self, total_km):
        if total_km > 5000:
            return 0.15
        elif total_km > 2500:
            return 0.10
        elif total_km > 1000:
            return 0.05
        elif total_km > 500:
            return 0.025
        else:
            return 0


    # rate fitness of the individuals
    def evaluate(self, individual, start, destination, car_class, total_km):

        cost_per_km_multiplier = max(individual[0], 0.5)
        remoteness_cost_multiplier = individual[1]
        car_class_multiplier = max(individual[2], 0.8)
        loyalty_discount_multiplier = individual[3]


        distance = self.calculate_distance(start, destination)
        remoteness_cost = self.get_remoteness_cost(distance) * remoteness_cost_multiplier
        loyalty_discount = self.get_loyalty_discount(total_km + distance) * loyalty_discount_multiplier
        car_class_factor = self.get_car_class_factor(car_class) * car_class_multiplier
        travel_cost = self.get_travel_cost (distance, cost_per_km_multiplier)
        cost1 = (travel_cost + remoteness_cost)
        cost2 = cost1 +  cost1 * car_class_factor
        total_cost = cost2 - cost2 * loyalty_discount

        return total_cost,

    def setup_evaluate(self, start, destination, car_class, total_km):
        self.toolbox.register("evaluate", self.evaluate, start=start, destination=destination, car_class=car_class, total_km=total_km)


    def calculate_total_cost_for_individual(self, individual, start, destination, car_class, total_km):
        return self.evaluate(individual, start, destination, car_class, total_km)

    def run_ga(self,start, destination, car_class, total_km):
        self.setup_evaluate(start, destination, car_class, total_km)

        population = self.toolbox.population(n=200)
        num_generations = 100

        for gen in range(num_generations):
            # Selection of parents
            offspring = self.toolbox.select(population, len(population))

            # Applying crossover and mutation to the offspring
            offspring = algorithms.varAnd(offspring, self.toolbox, cxpb=0.5, mutpb=0.2)

            # Calculating the fitness of the new offspring
            fits = [self.toolbox.evaluate(ind) for ind in offspring]
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit

            # Replacing the old population with the new offspring
            population = offspring

        return tools.selBest(population, k=1)[0]

    def run_optimization(self, start, destination, car_class, total_km):
        best_individual = self.run_ga(start, destination, car_class, total_km)
        lowest_cost = self.calculate_total_cost_for_individual(best_individual, start, destination, car_class, total_km)
        return best_individual, lowest_cost
