import axios from 'axios';
import responseServiceHelper from '../helpers/responseServiceHelper.js';


const determinePickUp = async (PickupLocation, DestinationLocation, userId) => {
  try {
    const customerPosition = PickupLocation.toUpperCase();
    const destinationPosition = DestinationLocation.toUpperCase();

    const rawVehicles = await responseServiceHelper.queryVehiclePositions();

    const mapedVehicles = rawVehicles.results.bindings.map(vehicle => ({
      vehicleID: vehicle.vehicleID.value,
      vehiclePosition: vehicle.vehiclePosition.value,
    }));

    const rawRoadConstructions = await responseServiceHelper.queryRoadConstructions();

    const mapedRoadConstructions = rawRoadConstructions.results.bindings.map(construction => ({
      constructionID: construction.constructionID.value,
      constructionLocation: construction.constructionLocation.value,
    }));

    let roadConstructions = mapedRoadConstructions.map(construction => construction.constructionLocation).join(',');

    if (roadConstructions.length === 0) {
      roadConstructions = 'no';
    }

    const client = await responseServiceHelper.queryClientByUserId(userId);

    if (!client) {
      throw new Error('Client not found while determining pickup location');
    }

    const payload = {
      customer_position: customerPosition,
      destination_position: destinationPosition,
      car1_position: mapedVehicles[0].vehiclePosition,
      car2_position: mapedVehicles[1].vehiclePosition,
      car3_position: mapedVehicles[2].vehiclePosition,
      traffic: 'no',
      local_events: 'no',
      road_constructions: roadConstructions,
      age: client.age,
      gender: client.gender,
      account_type: client.accountType,
    };

    console.log('app:determinePickUp payload', payload);

    const determinePickUpDataRes = await axios.post('/api/determine-pickup-service/determinePickUp', payload, {
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });

    const determinePickUpData = determinePickUpDataRes.data;

    console.log('app:determinePickUp response');
    console.dir(determinePickUpData, { depth: null });

    return determinePickUpData;
  } catch (error) {
    console.log('Error calling determinePickUp:', error);
    throw new Error('Failed to determine the optimal pickup location.');
  }
};

const proposeCarActions = async (tripMetrics) => {
  console.log('app:proposeCarActions payload', tripMetrics);

  try {
    const proposeCarActionsRes = await axios.post('/api/propose-action-service/car-actions', tripMetrics, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });

    const proposeCarActionsData = proposeCarActionsRes.data;

    console.log('app:proposeCarActions response');
    console.dir(proposeCarActionsData, { depth: null });

    return proposeCarActionsData;
  } catch (error) {
    console.error('Error calling proposeCarActions service:', error);
    return { actions: [] };
  }
};

const decideAcceptance = async (payload) => {
  console.log('app:decideAcceptance payload', payload);

  try {
    const decideAcceptanceRes = await axios.post('/api/acceptance-service/decide-on-request-acceptance', payload,
      {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        }
      });
    const decideAcceptanceData = decideAcceptanceRes.data;

    console.log('app:decideAcceptance response');
    console.dir(decideAcceptanceData, { depth: null });

    return decideAcceptanceData;
  } catch (error) {
    console.error('Error calling acceptance-service', error.message);
    throw new Error('Failed to call g7-service');
  }
}

const adaptProposal = async (payload) => {
  console.log('app:adaptProposal payload', payload);

  try {
    const adaptProposalRes = await axios.post('/api/proposal-service/predict', payload,
      {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        }
      });
    const adaptProposalData = adaptProposalRes.data;

    console.log('app:adaptProposal response');
    console.dir(adaptProposalData, { depth: null });

    return adaptProposalData;
  } catch (error) {
    console.error('Error calling adapt-proposal-service', error.message);
    throw new Error('Failed to call g8-service');
  }
}

const optimizePrice = async (payload) => {
  console.log('app:optimizePrice payload', payload);

  try {
    const optimizePriceRes = await axios.post('/api/pricing-service/api/pricing/company', payload,
      {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        }
      });
    const optimizePriceData = optimizePriceRes.data;

    console.log('app:optimizePrice response');
    console.dir(optimizePriceData, { depth: null });

    return optimizePriceData;
  } catch (error) {
    console.error('Error calling optimize-price-service', error.message);
    throw new Error('Failed to call g9-service');
  }
}


export default {
  determinePickUp,
  proposeCarActions,
  decideAcceptance,
  adaptProposal,
  optimizePrice,
};