# Car Decision on Meeting Points

## Operation: determinePickUp

### Topic: Car determines optimal place to pick up customer from

### Description:

This microservice finds an optimal place where a car should pick up the customer based on various parameters. It uses rules and logic statements to determine the best pickup locations considering factors such as weather, traffic, local events, road constructions, time of day, and customer attributes.

### Guiding Question/s:
- How can we determine the optimal pickup location for a customer in a dynamic urban environment?
- What are the critical factors influencing the decision of pickup locations?

### Technology:
- **First-Order Logic**
- **Rule-Based Systems**

### Tools:
- **SWI-Prolog**
- **CLIPS**
- **Drools**

# Test Cases for Prolog Rules

This document provides test cases to validate the behavior of the `optimal_pickup` Prolog rules defined in `rules.pl`. Each test case includes the input data, expected outcomes, and the specific rule being tested.

## Rule 1: All Cars Blocked by Road Constructions

```json
{
  "customer_position": "J",
  "destination_position": "L",
  "car1_position": "A",
  "car2_position": "C",
  "car3_position": "E",
  "traffic": "no",
  "local_events": "no",
  "road_constructions": "B,D,F",
  "age": 27,
  "gender": "male",
  "account_type": "regular"
}
```

## Rule 2: Customer Should Walk

```json
{
  "customer_position": "J",
  "destination_position": "K",
  "car1_position": "A",
  "car2_position": "C",
  "car3_position": "E",
  "traffic": "no",
  "local_events": "no",
  "road_constructions": "no",
  "age": 27,
  "gender": "male",
  "account_type": "regular"
}
```

## Rule 3: Nearest Car Without Road Constructions (Roadconstructions)

```json
{
  "customer_position": "J",
  "destination_position": "L",
  "car1_position": "A",
  "car2_position": "C",
  "car3_position": "E",
  "traffic": "no",
  "local_events": "no",
  "road_constructions": "B,D",
  "age": 27,
  "gender": "male",
  "account_type": "regular"
}
```

## Rule 4: Nearest Car Without Road Constructions (No Roadconstructions)

```json
{
  "customer_position": "J",
  "destination_position": "L",
  "car1_position": "A",
  "car2_position": "C",
  "car3_position": "E",
  "traffic": "no",
  "local_events": "no",
  "road_constructions": "no",
  "age": 27,
  "gender": "male",
  "account_type": "regular"
}
```

## Rule 5: Weather Is Sunny and It’s Noon

```json
{
  "customer_position": "J",
  "destination_position": "L",
  "car1_position": "A",
  "car2_position": "C",
  "car3_position": "E",
  "traffic": "no",
  "local_events": "no",
  "road_constructions": "no",
  "age": 27,
  "gender": "male",
  "account_type": "regular",
  "time_of_day": "noon",
  "weather": "sunny"
}
```

## Rule 6: Premium Account with Senior/Child Customer

```json
{
  "customer_position": "J",
  "destination_position": "L",
  "car1_position": "A",
  "car2_position": "C",
  "car3_position": "E",
  "traffic": "no",
  "local_events": "no",
  "road_constructions": "B,D",
  "age": 70,
  "gender": "male",
  "account_type": "premium"
}
```

## Rule 7: Rainy Weather and a Close Car

```json
{
  "customer_position": "J",
  "destination_position": "L",
  "car1_position": "A",
  "car2_position": "C",
  "car3_position": "E",
  "traffic": "no",
  "local_events": "no",
  "road_constructions": "no",
  "age": 27,
  "gender": "male",
  "account_type": "regular",
  "weather": "rainy"
}
```

## Rule 8: Premium Account, Far Destination, and Halfway Pickup

```json
{
  "customer_position": "J",
  "destination_position": "M",
  "car1_position": "A",
  "car2_position": "C",
  "car3_position": "E",
  "traffic": "no",
  "local_events": "no",
  "road_constructions": "no",
  "age": 27,
  "gender": "male",
  "account_type": "premium"
}
```

## Rule 9: Default Case

```json
{
  "customer_position": "J",
  "destination_position": "L",
  "car1_position": "A",
  "car2_position": "C",
  "car3_position": "E",
  "traffic": "no",
  "local_events": "no",
  "road_constructions": "",
  "age": 27,
  "gender": "male",
  "account_type": "regular"
}
```