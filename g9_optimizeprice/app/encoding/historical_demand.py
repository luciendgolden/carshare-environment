from deap import base, creator, tools, algorithms
import datetime
import random

class HistoricalDemandPredictor:
    def __init__(self, data):
        self.data = data
        self.avg_monthly_demand = data.groupby('month').size()
        self.avg_daily_demand = data.groupby('day_of_week').size()
        self.avg_hourly_demand = data.groupby('hour_of_day').size()

        # Clear existing classes if they exist
        if "FitnessMax" in creator.__dict__:
            del creator.FitnessMax
        if "Individual" in creator.__dict__:
            del creator.Individual

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", self.create_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.evaluate)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def create_individual(self):
        return creator.Individual([random.uniform(0.5, 1.5) for _ in range(3)])

    def evaluate(self, individual):
        mse = 0
        count = 0
        for _, row in self.data.iterrows():
            predicted_demand = (self.avg_monthly_demand[row['month']] * individual[0] +
                                self.avg_daily_demand[row['day_of_week']] * individual[1] +
                                self.avg_hourly_demand[row['hour_of_day']] * individual[2])
            actual_demand = actual_demand = (self.avg_monthly_demand[row['month']] +
                             self.avg_daily_demand[row['day_of_week']] +
                             self.avg_hourly_demand[row['hour_of_day']]) / 3
            mse += (actual_demand - predicted_demand) ** 2
            count += 1
        mse /= count
        return -mse,

    def run_ga(self):
        population = self.toolbox.population(n=50)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(key=lambda ind: ind.fitness.values)
        stats.register("avg", lambda x: max(x))
        stats.register("min", lambda x: min(x))
        stats.register("max", lambda x: max(x))
        algorithms.eaSimple(population, self.toolbox, 0.7, 0.2, 30, stats=stats, halloffame=hof, verbose=False)
        return hof.items[0]

    def get_predicted_demand(self):
        best_solution = self.run_ga()
        today = datetime.datetime.now()
        today_month = today.month
        today_day = today.weekday()
        today_hour = today.hour

        predicted_demand_today = (self.avg_monthly_demand[today_month - 1] * best_solution[0] +
                                  self.avg_daily_demand[today_day] * best_solution[1] +
                                  self.avg_hourly_demand[today_hour] * best_solution[2])
        return max(predicted_demand_today, 0)