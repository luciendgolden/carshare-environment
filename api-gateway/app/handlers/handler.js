import services from '../services/index.js';
import responseServiceHelper from '../helpers/responseServiceHelper.js';
import proposeCarActionHelper from '../helpers/proposeCarActionHelper.js';
import acceptanceServiceHelper from '../helpers/acceptanceServiceHelper.js';
import adaptProposalHelper from '../helpers/adaptProposalHelper.js';
import optimizePriceHelper from '../helpers/optimizePriceHelper.js';


const carVehicleMap = {
  'Car 1': 'Vehicle1',
  'Car 2': 'Vehicle2',
  'Car 3': 'Vehicle3',
};

const movementMap = {
  's': 'sl',
  'r': 'sl,rl,sl',
  'l': 'sl,ll,sl'
};

const mBotMap = {
  'Car 1': 'mbot/1/commands',
  'Car 2': 'mbot/2/commands',
  'Car 3': 'mbot/3/commands',
}

export const launchRequestHandler = async ({ userId }) => {
  try {
    const client = await responseServiceHelper.queryClientByUserId(userId);

    if (!client) {
      throw new Error('Client not found');
    }

    console.log(`Client found: ${JSON.stringify(client)}`);

    const message = `Welcome back. You are a ${client.age}-year-old ${client.gender} with a ${client.accountType} account. Your current position is ${client.position}. How can I assist you today?`;
    return message;
  } catch (error) {
    throw new Error(error);
  }
};

export const requestRideIntentHandler = async ({ PickupLocation, DestinationLocation, userId }, redisClient, mqttclient) => {
  try {
    const cacheKey = `ride:${userId}`;
    const rideData = await redisClient.get(cacheKey);

    // check if the user has an active ride
    if (rideData) {
      return 'You already have an active ride. Please confirm or cancel the current ride.';
    }

    // Query client data
    const client = await responseServiceHelper.queryClientByUserId(userId);

    // Determine the optimal pickup location g4_determinepickup
    let determinePickUpRes = await services.determinePickUp(PickupLocation, DestinationLocation, userId);
    const { optimal_pickup, parameters_used } = determinePickUpRes;

    // check if car movements is not empty
    if (determinePickUpRes['car route'].length === 0) {
      return `Ride is currently not possible. ${determinePickUpRes['Rule']}`;
    }

    // Decide on requested ride acceptance g7_decideonrequestacceptance
    const inputParams = {
      rating: acceptanceServiceHelper.determineRating(parameters_used),
      demand: acceptanceServiceHelper.determineDemand(parameters_used),
      weather: acceptanceServiceHelper.determineWeather(parameters_used),
    };

    // Call the decideAcceptance service
    const payload = acceptanceServiceHelper.mapInputParamsToPayload(inputParams);
    let acceptanceResult = await services.decideAcceptance(payload);

    // TODO: if acceptanceResult.decision is false, mock the decision to true
    acceptanceResult.decision = true;

    if (!acceptanceResult.decision) {
      return 'Ride request was not accepted due to current conditions.';
    }

    // map from determinePickUpRes 'car movements' object values {A_B: 's'} to movementMap values {A_B: 'sl'}
    let mappedCarmovements = {};
    for (const [key, value] of Object.entries(determinePickUpRes['car movements'])) {
      mappedCarmovements[key] = movementMap[value];
    }

    let mappedCustomermovements = {};
    for (const [key, value] of Object.entries(determinePickUpRes['customer movements'])) {
      mappedCustomermovements[key] = movementMap[value];
    }

    // add to determinePickRes
    determinePickUpRes = {
      ...determinePickUpRes,
      'mapped car movements': mappedCarmovements,
      'mapped customer movements': mappedCustomermovements,
    };

    // get mbot address from determinePickUpRes optimal_pickup
    const mBotAddress = mBotMap[optimal_pickup];

    // Trigger the IoT device to move to the customer location
    for (const [, value] of Object.entries(mappedCarmovements)) {
      mqttclient.publish(mBotAddress, value);
      mqttclient.publish(mBotAddress, 'j');
    }

    // Add the trip request to the database GraphDB
    let tripRequestId = await responseServiceHelper.addTripRequest(userId, determinePickUpRes);

    determinePickUpRes = {
      ...determinePickUpRes,
      tripRequestId
    };

    const tripMetrics = proposeCarActionHelper.getTripMetrics(determinePickUpRes);
    await responseServiceHelper.addTripMetrics(tripRequestId, tripMetrics);

    // Cal the adaptProposalService g8_adaptproposal
    const adaptProposalPayload = adaptProposalHelper.mapClientDataToProposalPayload(client);
    const { predicted_car } = await services.adaptProposal(adaptProposalPayload);

    // Call the proposeCarActions service g5_proposecaraction
    const actionsResponse = await services.proposeCarActions(tripMetrics);
    const incentives = proposeCarActionHelper.extractIncentives(actionsResponse.actions);

    // Call optimize price service g9_optimizeprice
    const optimizePricePayload = optimizePriceHelper.mapParamsToPayload(client, determinePickUpRes);
    const { best_price } = await services.optimizePrice(optimizePricePayload);

    determinePickUpRes = { ...determinePickUpRes, tripMetrics, actionsResponse }

    await redisClient.set(cacheKey, JSON.stringify(determinePickUpRes), {
      EX: 3600,
    });

    await responseServiceHelper.updateVehiclePosition(carVehicleMap, determinePickUpRes, 'car route');

    let responseMessage = `Ride requested from ${PickupLocation} to ${DestinationLocation}. Your optimal pickup will be ${optimal_pickup} a ${predicted_car}. The vehicle is on its way, please confirm once it arrives.`;

    
    if(best_price > 0) {
      responseMessage += ` The estimated price for the ride per minute is ${best_price}`;
    }
    

    if (incentives.length > 0) {
      const incentivesText = await responseServiceHelper.queryResponseServiceFromJson({ 'rideIncentives': incentives });
      responseMessage += ` We have some incentives for you ${incentivesText}.`;
    }

    // vehicle honk
    mqttclient.publish(mBotAddress, 'h');

    return responseMessage;
  } catch (error) {
    throw new Error(error);
  }
};

export const confirmRideIntentHandler = async ({ userId }, redisClient, mqttclient) => {
  try {
    const cacheKey = `ride:${userId}`;
    const rideData = await redisClient.get(cacheKey);

    if (!rideData) {
      throw new Error('Session data not found. Please request a new ride.');
    }

    const determinePickUpRes = JSON.parse(rideData);
    const { tripRequestId, actionsResponse } = determinePickUpRes;


    const mBotAddress = mBotMap[determinePickUpRes.optimal_pickup];

    for (const [, value] of Object.entries(determinePickUpRes['mapped customer movements'])) {
      mqttclient.publish(mBotAddress, value);
      mqttclient.publish(mBotAddress, 'j');
    }

    await responseServiceHelper.updateVehiclePosition(carVehicleMap, determinePickUpRes, 'customer to destination path');
    await responseServiceHelper.updateClientPosition(userId, determinePickUpRes['parameters_used']['destination_position']);

    await responseServiceHelper.updateEndTimeTripRequest(tripRequestId);

    await redisClient.del(cacheKey);

    const actions = proposeCarActionHelper.extractActions(actionsResponse.actions);

    let responseMessage = 'Ride confirmed. Let the journey begin!';

    if (actions.length > 0) {
      const actionsText = await responseServiceHelper.queryResponseServiceFromJson({ 'carActions': actions });
      responseMessage += ` During your ride, please consider the following actions ${actionsText}.`;
    }

    // vehicle honk
    mqttclient.publish(mBotAddress, 'h');

    return responseMessage;
  } catch (error) {
    throw new Error(error);
  }
};

export const searchQueryIntentHandler = async ({ query, userId }) => {
  try {
    let response;

    if (userId) {
      response = await responseServiceHelper.queryResponseServiceFromNlp(query, userId);
    } else {
      response = await responseServiceHelper.queryResponseServiceFromNlp(query);
    }

    if (!response.success) {
      throw new Error('Response not found');
    }

    return response.summary;
  } catch (error) {
    throw new Error(error);
  }
};

export const updatePositionIntentHandler = async ({ NewPosition, userId }) => {
  try {
    let position = NewPosition;
    // position should be uppercase
    position = position.toUpperCase();

    await responseServiceHelper.updateClientPosition(userId, position);

    return `Your position was updated to ${position}.`;
  } catch (error) {
    throw new Error(error);
  }
}

export const cancelCurrentRideIntentHandler = async ({ userId }, redisClient) => {
  try {
    const cacheKey = `ride:${userId}`;
    const rideData = await redisClient.get(cacheKey);

    if (!rideData) {
      throw new Error('Session data not found. Request a new ride.');
    }

    await redisClient.del(cacheKey);

    return 'Ride cancelled.';
  } catch (error) {
    throw new Error(error);
  }
}