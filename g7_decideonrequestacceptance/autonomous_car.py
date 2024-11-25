# Import this class via:
# from autonomous_car import AutonomousCar

class AutonomousCar:
    def __init__(self, customer_rating_weight, weather_weight, demand_weight, acceptance_threshold):
        # Initialize the car with specific weights and a threshold.
        # These parameters allow each car to tailor its decision-making criteria based on its unique needs or strategies.
        self.customer_rating_weight = customer_rating_weight  # Weight for customer rating. Higher weight means more influence on the decision.
        self.weather_weight = weather_weight                  # Weight for weather conditions. Adjust based on how much weather should affect the decision.
        self.demand_weight = demand_weight                    # Weight for predicted demand. Helps the car decide based on expected demand levels.
        self.acceptance_threshold = acceptance_threshold      # Custom threshold for accepting a ride. Determines the minimum score required to accept a ride.

    def should_accept_ride(self, customer_rating, weather, predicted_demand):
        # Calculate a score based on the weighted sum of the parameters.
        # The function allows for flexible decision-making based on the weighted importance of each parameter.
        score = (customer_rating * self.customer_rating_weight +
                 weather * self.weather_weight +
                 predicted_demand * self.demand_weight)
        # The car decides to accept or reject the ride based on whether the score meets its custom threshold.
        return score >= self.acceptance_threshold  # Decision is made here based on the calculated score and the car's acceptance threshold