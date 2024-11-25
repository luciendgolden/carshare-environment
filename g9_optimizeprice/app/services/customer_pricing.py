
from deap import base, creator, tools, algorithms
import random
import math
import requests
from bs4 import BeautifulSoup
import re
from datetime import date
import googlemaps

class CustomerPricingService:

############Constructor############
    def __init__(self, customer_rate, car_class, base_price, car_location, customer_location, destination_location):
        self.customer_rate = customer_rate
        self.car_class = car_class
        self.base_price = base_price
        self.car_location = car_location
        self.customer_location = customer_location
        self.destination_location = destination_location


    def run(self):
        import requests
        from bs4 import BeautifulSoup
        import re
        from datetime import date

        today = date.today()
        date = today.strftime('%Y-%m-%d')
        url = "https://events.wien.info/de/?df="+date+"&dt="+date+"&c=31&c=32&c=33&c=34&c=35&c=36&c=37&c=38&c=39&c=40&c=41&c=42&c=43&lt=-1"

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        number_of_events = soup.select_one('.event_searchresult-report span').text

        def demand_rate_calculation(number_of_events):
          if number_of_events >= 0 and number_of_events <= 40:
            return 1
          elif number_of_events > 40 and number_of_events <= 80:
            return 2
          elif number_of_events > 80 and number_of_events <= 100:
            return 3
          elif number_of_events > 100 and number_of_events <= 150:
            return 4
          elif number_of_events > 150:
            return 5
          else:
            return 3

        ####################### Distanse and Duration collection ################################################

        gmaps = googlemaps.Client(key='AIzaSyBjAuldPohbUgrGpr-A5r1U2w7g84dGXQY')

        def customer_distanation_distanse_calculation():
          trip_dist = gmaps.distance_matrix(self.customer_location, self.destination_location)['rows'][0]['elements'][0]

          distance_text = trip_dist['distance']['text']

          distance_text = distance_text.rstrip()

          distance_text = distance_text.split(" ")[0]

          distance_float = float(distance_text)
          return distance_float

        def customer_distanation_time_calculation():
          trip_dist = gmaps.distance_matrix(self.customer_location, self.destination_location)['rows'][0]['elements'][0]

          duration_text = trip_dist['duration']['text']

          duration_text = duration_text.rstrip()

          duration_text = duration_text.split(" ")[0]

          duration_float = float(duration_text)
          return duration_float

        def waiting_time_calculation():
          waiting_time_dist = gmaps.distance_matrix(self.car_location, self.customer_location)['rows'][0]['elements'][0]

          waiting_time_text = waiting_time_dist['duration']['text']

          waiting_time_text = waiting_time_text.rstrip()

          waiting_time_text = waiting_time_text.split(" ")[0]

          waiting_time_float = float(waiting_time_text)

          return waiting_time_float

        #Knowledge Based Data (Google)
        NUMBER_OF_EVENTS = int(number_of_events)
        DEMAND_RATE = demand_rate_calculation(NUMBER_OF_EVENTS) #integer between 1 and 5, based on NUMBER_OF_EVENTS

        REMOTENESS_KM = customer_distanation_distanse_calculation()
        TIME_MINUTES = customer_distanation_time_calculation()
        WAITING_TIME_MINUTES = waiting_time_calculation()

        ####################### End Real Data collection ################################################

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()

        REMOTENESS_ENUM = ""    # "close", "average", "remote"
        WAITING_TIME_ENUM = ""  # "short", "average", "long"

        ##################### Attributes generation Function #################################################
        def customer_rate_discount_calculation(customer_rate):
                if customer_rate == 1:
                    toolbox.register("customer_rate_discount", random.uniform, 5, 10)
                if customer_rate ==  2:
                    toolbox.register("customer_rate_discount", random.uniform, 1, 5)
                if customer_rate ==  3:
                    toolbox.register("customer_rate_discount", random.uniform, 0, 1)
                if customer_rate ==  4:
                    toolbox.register("customer_rate_discount", random.uniform, -3, -1)
                if customer_rate ==  5:
                    toolbox.register("customer_rate_discount", random.uniform, -5, -3)
                else:
                    toolbox.register("customer_rate_discount", random.uniform, 0, 0)

        def demand_extra_pricing_calculation(demand_rate):
                if demand_rate == 1:
                    toolbox.register("demand_extra_pricing", random.uniform, 0, 1)
                if demand_rate ==  2:
                    toolbox.register("demand_extra_pricing", random.uniform, 1, 5)
                if demand_rate ==  3:
                    toolbox.register("demand_extra_pricing", random.uniform, 5, 50)
                if demand_rate ==  4:
                    toolbox.register("demand_extra_pricing", random.uniform, 50, 100)
                if demand_rate ==  5:
                    toolbox.register("demand_extra_pricing", random.uniform, 100, 300)
                else:
                    toolbox.register("demand_extra_pricing", random.uniform, 0, 0)

        def remoteness_extra_pricing_calculation(remoteness_km):
          if remoteness_km >= 0 and remoteness_km <= 6:
            toolbox.register("remoteness_extra_pricing", random.uniform, 0, 1)
            REMOTENESS_ENUM = "close"
          elif remoteness_km > 6 and remoteness_km <= 20:
            toolbox.register("remoteness_extra_pricing", random.uniform, 1, 5)
            REMOTENESS_ENUM = "average"
          elif remoteness_km > 20:
            toolbox.register("remoteness_extra_pricing", random.uniform, 5, 10)
            REMOTENESS_ENUM = "remote"
          else:
            toolbox.register("remoteness_extra_pricing", random.uniform, 0, 0)

        def time_extra_pricing_calculation(time_minutes):
          if time_minutes >= 0 and time_minutes <= 35:
            toolbox.register("time_extra_pricing", random.uniform, 0, 1)
          elif time_minutes > 35:
            toolbox.register("time_extra_pricing", random.uniform, 1, 5)
          else:
            toolbox.register("time_extra_pricing", random.uniform, 0, 0)

        def waiting_time_discount_calculation(waiting_time_minutes):
          if waiting_time_minutes >= 0 and waiting_time_minutes <= 5:
            toolbox.register("waiting_time_discount", random.uniform, -1, 0)
            WAITING_TIME_ENUM = "short"
          elif waiting_time_minutes > 5 and waiting_time_minutes <= 15:
            toolbox.register("waiting_time_discount", random.uniform, -5, -1)
            WAITING_TIME_ENUM = "average"
          elif waiting_time_minutes > 15:
            toolbox.register("waiting_time_discount", random.uniform, -10, -5)
            WAITING_TIME_ENUM = "long"
          else:
            toolbox.register("waiting_time_discount", random.uniform, 0, 0)

        def car_rate_extra_pricing_calculation(car_class):
                if car_class == "economy":
                    toolbox.register("car_rate_extra_pricing", random.uniform, -10, -1)
                if car_class == "business":
                    toolbox.register("car_rate_extra_pricing", random.uniform, -1, 0)
                if car_class == "luxus":
                    toolbox.register("car_rate_extra_pricing", random.uniform, 0, 5)
                else:
                    toolbox.register("car_rate_extra_pricing", random.uniform, 0, 0)


        customer_rate_discount_calculation(self.customer_rate)
        demand_extra_pricing_calculation(DEMAND_RATE)
        remoteness_extra_pricing_calculation(REMOTENESS_KM)
        time_extra_pricing_calculation(TIME_MINUTES)
        waiting_time_discount_calculation(WAITING_TIME_MINUTES)
        car_rate_extra_pricing_calculation(self.car_class)
        toolbox.register("promotion_discount", random.uniform, -5, 0)

        ##################### End Attributes generation Function #################################################

        # define 'individual' with 7 attribute elements ('genes')
        toolbox.register("individual", tools.initCycle, creator.Individual,
                        (toolbox.customer_rate_discount, toolbox.demand_extra_pricing, toolbox.remoteness_extra_pricing,
                        toolbox.time_extra_pricing, toolbox.waiting_time_discount, toolbox.car_rate_extra_pricing, toolbox.promotion_discount), 1)

        # define the population to be a list of individuals
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        ##################### Fitness Function #################################################
        def car_class_satisfaction(car_class):
                if car_class == "economy":
                    return 0
                if car_class == "business":
                    return 1
                if car_class == "luxus":
                    return 2
                else:
                    return 0

        def waiting_time_satisfaction(time_discount, waiting_time_class):
                if waiting_time_class == "short": #discount 0-1%, 5 min
                    return time_discount/-1
                if waiting_time_class == "average":#5-15 min, discount 1-5%
                    return time_discount/-5
                if waiting_time_class == "long":#15, discount 5-10%
                    return time_discount/-10
                else:
                    return 0

        def fair_remoteness_pricing(remoteness_extra, remoteness_class):
                if remoteness_class == "close":#0-6 km, discount 0
                    return 0
                if remoteness_class ==  "average":#6-20 km, pricing +1 - +5%
                    return 1/remoteness_extra
                if remoteness_class ==  "remote":#20 km, pricing +5 - +10%
                    return 5/remoteness_extra
                else:
                    return 0

        def fair_demand_pricing(demand_extra):
          if demand_extra > 200:
            return -2
          else:
            return 0

        def evalMin(individual):
            discount = sum(individual)
            fitness = (-discount)
            fitness += car_class_satisfaction(self.car_class)
            fitness += waiting_time_satisfaction(individual[4], WAITING_TIME_ENUM) # input data waiting time
            fitness += fair_remoteness_pricing(individual[2], REMOTENESS_ENUM) # input data remoteness
            fitness += fair_demand_pricing(individual[1])
            return fitness,

        ##################### Fitness Function End #################################################

        #***************************************************************************************/
        #    Title: DEAP Documentation OneMax Problem Example
        #    Author: DEAP Documentation
        #    Availability: https://github.com/DEAP/deap/blob/60913c5543abf8318ddce0492e8ffcdf37974d86/examples/ga/onemax.py
        #
        #**************************************************************************************/

        #----------
        # Operator registration
        #----------

        toolbox.register("evaluate", evalMin)

        toolbox.register("mate", tools.cxTwoPoint)

        toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

        toolbox.register("select", tools.selTournament, tournsize=3)
        pop = toolbox.population(n=300)

        CXPB, MUTPB = 0.5, 0.2

        #print("Start of evolution")

        # Evaluate the population
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        #print("  Evaluated %i individuals" % len(pop))

        fits = [ind.fitness.values[0] for ind in pop]
        data = {"evaluated_individuals": len(pop)}
        g = 0
        while g < 100:
            g = g + 1
            #print("-- Generation %i --" % g)

            offspring = toolbox.select(pop, len(pop))
            offspring = list(map(toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):

                if random.random() < CXPB:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:

                if random.random() < MUTPB:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            #print("  Evaluated %i individuals" % len(invalid_ind))

            pop[:] = offspring

            fits = [sum(ind) for ind in pop]
            length = len(pop)
            mean = sum(fits) / length

            # print("  Min %s" % (max(fits)))
            # print("  Max %s" % (min(fits)))
            # print("  Avg %s" % (mean))

            # Data to save
            single_gen_data = {
              "generation"+str(g)+"_data" : {
                  "generation": g,
                  "evaluated_individuals": len(invalid_ind),
                  "min": (max(fits)),
                  "max" : (min(fits)),
                  "avg": mean
              }
            }
            data.update(single_gen_data)

        filename = "ga_all_indiviaduals_output_data.json"

        # with open(filename, "w") as outfile:
        #   json.dump(data, outfile, indent=4)

        #print("-- End of (successful) evolution --")

        best_ind = tools.selBest(pop, 1)[0]
        best_discount_percent = sum(best_ind)
        best_discount_value = (self.base_price/100)*best_discount_percent
        best_price = self.base_price + best_discount_value
        #print("Best individual is %s, %s" % (best_ind, best_price))

        # Data to save
        filename = "ga_best_individual_output_data.json"

        new_data = {
          "Best Price": best_price,
          "Best Discount Percent": best_discount_percent,
          "Customer Rate Discount" : best_ind[0],
          "Demand Extra Pricing": best_ind[1],
          "Remoteness Extra Pricing": best_ind[2],
          "Time Extra Pricing": best_ind[3],
          "Waiting Time Discount": best_ind[4],
          "Car Rate Pricing": best_ind[5],
          "Promotion Discount": best_ind[6]
        }

        return new_data

        # with open(filename, "w") as outfile:
        #       json.dump(new_data, outfile, indent=4)



