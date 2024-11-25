% Definition of the optimal_pickup rule with various conditions
optimal_pickup(
    CustomerDestinationDistance, Car1DestinationDistance, Car1DestinationPath, Car2DestinationDistance, Car2DestinationPath, Car3DestinationDistance, Car3DestinationPath,
    NearestPath, NearestDistance, SecondNearestPath, SecondNearestDistance, ThirdNearestPath, ThirdNearestDistance,
    weather(Weather), traffic(_), local_events(_), road_constructions(Constructions), time_of_day(Time), day_of_week(_),
    Age, gender(_), account_type(Account_type), Customer, _, NearestCar, _, _,
    Location, Rule) :- 

    % Rule 0: If all cars have road constructions on their paths to customer, return none
    (contains_construction_node(NearestPath, Constructions),
     contains_construction_node(SecondNearestPath, Constructions),
     contains_construction_node(ThirdNearestPath, Constructions) -> 
        Location = 'None', Rule = "No car can reach the customer due to road constructions"
    );
    
    % Rule 1: If all cars have road constructions on their paths from customer to destination, return none
    (contains_construction_node(Car1DestinationPath, Constructions),
     contains_construction_node(Car2DestinationPath, Constructions),
     contains_construction_node(Car3DestinationPath, Constructions) -> 
        Location = 'None', Rule = "No car can reach the destination due to road constructions"
    );

    % Rule 2: If the customer does not have a Premium Account and the destination is closer to the customer than the nearest car, and the destination is less than 2 units away, the customer should walk.
    (Account_type == regular, CustomerDestinationDistance < NearestDistance, CustomerDestinationDistance < 2 -> 
        Location = 'Walk!', Rule = "If you don't have a premium account and the destination is closer to the customer than the nearest car, and the destination is less than 2 units away, the customer should make the journey on foot."
    );

    % Rule 3: Prioritize the nearest car if it has no road constructions on its path
    (\+ contains_construction_node(NearestPath, Constructions) ->
        Location = NearestCar, Rule = "Nearest car without road constructions"
    );

    % Rule 4: Choose the first car without road constructions
    (\+ contains_construction_node(Car1DestinationPath, Constructions) ->
        Location = "Car 1", Rule = "Car 1 selected because it has no road constructions.";
    \+ contains_construction_node(Car2DestinationPath, Constructions) ->
        Location = "Car 2", Rule = "Car 2 selected because it has no road constructions.";
    \+ contains_construction_node(Car3DestinationPath, Constructions) ->
        Location = "Car 3", Rule = "Car 3 selected because it has no road constructions."
    );

    % Rule 5: Handle sunny weather at noon condition
    (Weather = sunny, Time == noon, CustomerDestinationDistance < 30, 
     NearestDistance < CustomerDestinationDistance, SecondNearestDistance < CustomerDestinationDistance, ThirdNearestDistance < CustomerDestinationDistance ->
        min_member(MinDistance, [Car1DestinationDistance, Car2DestinationDistance, Car3DestinationDistance]),
        (MinDistance == Car1DestinationDistance ->
            Location = "Car 1", Rule = "If the weather is sunny and it is midday, the car should be chosen to take the shortest route to the destination because the customer prefers to walk.";
        MinDistance == Car2DestinationDistance ->
            Location = "Car 2", Rule = "If the weather is sunny and it is midday, the car should be chosen to take the shortest route to the destination because the customer prefers to walk.";
        MinDistance == Car3DestinationDistance ->
            Location = "Car 3", Rule = "If the weather is sunny and it is midday, the car should be chosen to take the shortest route to the destination because the customer prefers to walk.")
    );

    % Rule 6: Handle premium account and special cases (seniors, children)
    (Account_type == premium, (is_senior(Age); is_child(Age)) ->
        Location = Customer, Rule = "If the customer has a Premium Account and is a senior or minor, the customer will be picked up by the nearest car."
    );

    % Rule 7: Handle rainy weather scenario with a close car
    (Weather = rainy, is_near(NearestDistance) -> 
        Location = Customer, Rule = "If it is raining and the next car is close to the customer, the customer is picked up by the next car."
    );

    % Rule 8: Handle premium account, far destination, nearest car meeting halfway
    (Account_type == premium, NearestDistance > CustomerDestinationDistance, CustomerDestinationDistance > 30,
     \+ contains_construction_node(NearestPath, Constructions), find_median_node(NearestPath, MedianNode) -> 
        Location = MedianNode, Rule = "If you have a Premium account, the nearest car will meet the customer halfway, unless there are roadworks on the way."
    );

    % Rule 9: Default case
    (Location = NearestCar, Rule = "Default - nearest car").

% HELPER FUNCTIONS FOR RULES

is_senior(Age) :-
    Age >= 65.

is_child(Age) :-
    Age < 18.

is_near(Distance) :-
    Distance < 15.

contains_construction_node(Path, ConstructionNodes) :-
    intersection(Path, ConstructionNodes, Intersection),
    Intersection \= [].

% Function to determine the length of a list
list_length([], 0).
list_length([_|T], Length) :- list_length(T, N), Length is N + 1.

% Function to find the median of a list
find_median_node(List, Median) :-
    list_length(List, Length),
    MiddleIndex is Length // 2,
    nth0(MiddleIndex, List, Median).
