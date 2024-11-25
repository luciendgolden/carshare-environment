// app/helpers/responseServiceHelper.js
import axios from 'axios';

const RESPONSE_SERVICE_URL = '/api/response-service';

const sendSparqlRequest = async ({ query, update }) => {
    try {
        let data;
        const headers = {};

        if (query) {
            data = new URLSearchParams({ q: query }).toString();
        } else if (update) {
            data = new URLSearchParams({ u: update }).toString();
        } else {
            throw new Error('Either query or update must be provided');
        }

        const response = await axios.post(`${RESPONSE_SERVICE_URL}/db/sparql`, data, { headers });
        console.log(`sendSparqlRequest - ${response.status}`);
        //console.dir(response.data, { depth: null });

        if (update) {
            return { success: response.status >= 200 && response.status < 300, data: response.data };
        } else {
            return response.data;
        }
    } catch (error) {
        console.log(`Error executing SPARQL request: ${error.message}`);
        if (error.response) {
            console.log(`Response status: ${error.response.status}`);
            console.log(`Response data: ${JSON.stringify(error.response.data)}`);
        }
        throw new Error('Failed to execute SPARQL request');
    }
};

const queryVehiclePositions = async () => {
    const sparqlQuery = `
        PREFIX carshare: <http://example.org/carshare#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?vehicleID ?vehiclePosition
        WHERE {
            ?vehicle a carshare:Vehicle ;
                    carshare:vehicleID ?vehicleID ;
                    carshare:vehiclePosition ?vehiclePosition .
        }
    `;

    try {
        const response = await sendSparqlRequest({ query: sparqlQuery });

        return response;
    } catch (error) {
        console.log(`Error querying vehicle positions: ${error.message}`);
        throw new Error('Failed to query vehicle positions');
    }
};

const queryRoadConstructions = async () => {
    const sparqlQuery = `
        PREFIX carshare: <http://example.org/carshare#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?constructionID ?constructionLocation
        WHERE {
        ?construction a carshare:RoadConstruction ;
                        carshare:constructionID ?constructionID ;
                        carshare:constructionLocation ?constructionLocation .
        }
    `;

    try {
        const response = await sendSparqlRequest({ query: sparqlQuery });

        return response;
    } catch (error) {
        console.log(`Error querying road constructions: ${error.message}`);
        throw new Error('Failed to query road constructions');
    }
};

const queryRoadConstructionsByLocation = async (location) => {
    const sparqlQuery = `
        PREFIX carshare: <http://example.org/carshare#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?construction ?constructionID
        WHERE {
        ?construction a carshare:RoadConstruction ;
                        carshare:constructionID ?constructionID ;
                        carshare:constructionLocation "${location}" .
        }
    `;

    try {
        const response = await sendSparqlRequest({ query: sparqlQuery });

        if (response.results.bindings.length > 0) {
            const construction = response.results.bindings[0];
            return {
                construction: construction.construction.value.split('#')[1],
                id: construction.constructionID.value
            }
        } else {
            return null;
        }
    } catch (error) {
        console.log(`Error querying road constructions by location: ${error.message}`);
        throw new Error('Failed to query road constructions by location');
    }
};

const updateVehiclePositionInGraphDB = async ({ vehicleID, vehiclePosition }) => {
    const sparqlUpdate = `
        PREFIX carshare: <http://example.org/carshare#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        DELETE {
            ?vehicle carshare:vehiclePosition ?oldPosition .
        }
        INSERT {
            ?vehicle carshare:vehiclePosition "${vehiclePosition}" .
        }
        WHERE {
            ?vehicle a carshare:Vehicle ;
                    carshare:vehicleID "${vehicleID}" ;
                    carshare:vehiclePosition ?oldPosition .
        }
    `;

    try {
        const { success } = await sendSparqlRequest({ update: sparqlUpdate });

        if (!success) {
            throw new Error('SPARQL update failed');
        }

        console.log(`Updated vehicle position for ${vehicleID} to ${vehiclePosition}`);
    } catch (error) {
        console.log(`Error updating vehicle position: ${error.message}`);
        throw new Error('Failed sparql to update vehicle position');
    }
};

const updateVehiclePosition = async (carVehicleMap, determinePickUpRes, pathType) => {
    const { optimal_pickup } = determinePickUpRes;
    const vehicleID = carVehicleMap[optimal_pickup];
    const vehiclePosition = determinePickUpRes[pathType].slice(-1)[0];

    await updateVehiclePositionInGraphDB({ vehicleID, vehiclePosition });
};

const updateClientPosition = async (userId, position) => {
    const sparqlUpdate = `
        PREFIX carshare: <http://example.org/carshare#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        DELETE {
            ?client carshare:position ?oldPosition .
        }
        INSERT {
            ?client carshare:position "${position}" .
        }
        WHERE {
            ?client a carshare:Client ;
                    carshare:clientID "${userId}" ;
                    carshare:position ?oldPosition .
        }
    `;

    try {
        const { success } = await sendSparqlRequest({ update: sparqlUpdate });

        if (!success) {
            throw new Error('SPARQL update failed');
        }

        console.log(`Updated client position for ${userId} to ${position}`);
    } catch (error) {
        console.log(`Error updating client position: ${error.message}`);
        throw new Error('Failed sparql to update client position');
    }
}

const queryClientByUserId = async (userId) => {
    const sparqlQuery = `
        PREFIX carshare: <http://example.org/carshare#>
        SELECT ?client ?clientID ?clientPosition ?clientAge ?clientGender ?clientAccountType
               ?comfortImportance ?drivingProficiency ?drivingSickness ?familyFriendlyFeatures
               ?fuelTypePreference ?offRoadCapability ?passengerAmount ?policeRecord
               ?preferredRouteType ?preferredSpeed ?safetyImportance ?transmissionReference
        WHERE {
          ?client a carshare:Client ;
                  carshare:clientID "${userId}" ;
                  carshare:clientID ?clientID ;
                  carshare:position ?clientPosition ;
                  carshare:age ?clientAge ;
                  carshare:gender ?clientGender ;
                  carshare:accountType ?clientAccountType ;
                  carshare:comfortImportance ?comfortImportance ;
                  carshare:drivingProficiency ?drivingProficiency ;
                  carshare:drivingSickness ?drivingSickness ;
                  carshare:familyFriendlyFeatures ?familyFriendlyFeatures ;
                  carshare:fuelTypePreference ?fuelTypePreference ;
                  carshare:offRoadCapability ?offRoadCapability ;
                  carshare:passengerAmount ?passengerAmount ;
                  carshare:policeRecord ?policeRecord ;
                  carshare:preferredRouteType ?preferredRouteType ;
                  carshare:preferredSpeed ?preferredSpeed ;
                  carshare:safetyImportance ?safetyImportance ;
                  carshare:transmissionReference ?transmissionReference .
        }
        LIMIT 1
    `;

    try {
        const response = await sendSparqlRequest({ query: sparqlQuery });

        if (response.results.bindings.length === 0) {
            return null;
        }
        
        const client = response.results.bindings[0];
        return {
            client: client.client.value.split('#')[1],
            id: client.clientID.value,
            position: client.clientPosition.value,
            age: client.clientAge.value,
            gender: client.clientGender.value,
            accountType: client.clientAccountType.value,
            comfortImportance: client.comfortImportance.value,
            drivingProficiency: client.drivingProficiency.value,
            drivingSickness: client.drivingSickness.value,
            familyFriendlyFeatures: client.familyFriendlyFeatures.value,
            fuelTypePreference: client.fuelTypePreference.value,
            offRoadCapability: client.offRoadCapability.value,
            passengerAmount: parseInt(client.passengerAmount.value),
            policeRecord: client.policeRecord.value,
            preferredRouteType: client.preferredRouteType.value,
            preferredSpeed: client.preferredSpeed.value,
            safetyImportance: client.safetyImportance.value,
            transmissionReference: client.transmissionReference.value
        };
    } catch (error) {
        console.log(`Error querying client by userId: ${error.message}`);
        throw new Error('Failed to query client by userId');
    }
};

const queryResponseServiceFromNlp = async (question, userId) => {
    const url = `${RESPONSE_SERVICE_URL}/request/from/nlp`;

    let payload = {
        question: question,
    };

    if (userId) {
        payload.userId = userId;
    }

    try {
        const res = await axios.post(url, payload);
        const data = res.data;

        console.log(`${RESPONSE_SERVICE_URL}/request/from/nlp response: ${JSON.stringify(data)}`);

        return data;
    } catch (error) {
        console.log('Error querying response service:', error);
        throw new Error('Failed to query response service from NLP');
    }
};

const queryResponseServiceFromJson = async (json) => {
    const url = `${RESPONSE_SERVICE_URL}/request/from/json`;

    try {
        const res = await axios.post(url, json);
        const data = res.data;

        return data.summary;
    } catch (error) {
        console.log('Error querying response service:', error);
        throw new Error('Failed to query response service from JSON');
    }
};

const queryTripRequestById = async (tripRequestId) => {
    const sparqlQuery = `
        PREFIX carshare: <http://example.org/carshare#>
        SELECT ?tripRequest ?tripRequestId ?requestedBy ?startTime ?endTime ?weather ?traffic ?localEvents ?timeOfDay ?dayOfWeek ?roadConstructions ?tripMetrics
        WHERE {
            ?tripRequest a carshare:TripRequest ;
                carshare:requestID "${tripRequestId}" ;
                carshare:requestID ?tripRequestId ;
                carshare:requestedBy ?requestedBy ;
                carshare:startTime ?startTime ;
                carshare:endTime ?endTime ;
                carshare:weather ?weather ;
                carshare:traffic ?traffic ;
                carshare:localEvents ?localEvents ;
                carshare:timeOfDay ?timeOfDay ;
                carshare:dayOfWeek ?dayOfWeek ;
                carshare:roadConstructions ?roadConstructions ;
                carshare:tripMetrics ?tripMetrics .
        }
    `;

    try {
        const response = await sendSparqlRequest({ query: sparqlQuery });

        if (response.results.bindings.length > 0) {
            const tripRequest = response.results.bindings[0];
            return {
                tripRequest: tripRequest.tripRequest.value.split('#')[1],
                id: tripRequest.tripRequestId.value,
                requestedBy: tripRequest.requestedBy.value.split('#')[1],
                startTime: tripRequest.startTime.value,
                endTime: tripRequest.endTime.value,
                weather: tripRequest.weather.value,
                traffic: tripRequest.traffic.value,
                localEvents: tripRequest.localEvents.value,
                timeOfDay: tripRequest.timeOfDay.value,
                dayOfWeek: tripRequest.dayOfWeek.value,
                roadConstructions: tripRequest.roadConstructions.value,
                tripMetrics: tripRequest.tripMetrics.value?.split('#')[1] || null
            };
        } else {
            return null;
        }
    } catch (error) {
        console.log(`Error querying trip request by ID: ${error.message}`);
        throw new Error('Failed to query trip request by ID');
    }
};

const addTripMetrics = async (tripRequestId, tripMetrics) => {
    const tripMetricsId = `metrics_${tripRequestId}`;

    const insertQuery = `
        PREFIX carshare: <http://example.org/carshare#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        INSERT DATA {
            # Trip Metrics
            carshare:${tripMetricsId} a carshare:TripMetrics ;
                carshare:temperature "${tripMetrics.temperature}"^^xsd:integer ;
                carshare:rideTime "${tripMetrics.ride_time}"^^xsd:integer ;
                carshare:fuel "${tripMetrics.fuel}"^^xsd:float ;
                carshare:trafficCongestion "${tripMetrics.traffic_congestion}"^^xsd:integer ;
                carshare:visibility "${tripMetrics.visibility}"^^xsd:integer ;
                carshare:poi "${tripMetrics.poi}"^^xsd:integer ;
                carshare:carMaintenanceHistory "${tripMetrics.car_maintenance_history}"^^xsd:integer ;
                carshare:daytime "${tripMetrics.daytime}"^^xsd:time .
        }
    `;

    try {
        const { success } = await sendSparqlRequest({ update: insertQuery });

        if (!success) {
            throw new Error('SPARQL update failed');
        }

        await updateMetricTripRequest(tripRequestId, tripMetricsId);

        console.log(`Inserted trip metrics for Trip Request ID ${tripRequestId}`);
    } catch (error) {
        console.log(`Error inserting trip metrics: ${error.message}`);
        throw new Error('Failed to insert trip metrics');
    }
}

const updateMetricTripRequest = async (tripRequestId, tripMetricsId) => {
    const updateQuery = `
        PREFIX carshare: <http://example.org/carshare#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        DELETE {
            ?tripRequest carshare:tripMetrics ?oldTripMetrics .
        }
        INSERT {
            ?tripRequest carshare:tripMetrics carshare:${tripMetricsId} .
        }
        WHERE {
            ?tripRequest a carshare:TripRequest ;
                carshare:requestID "${tripRequestId}" ;
                carshare:tripMetrics ?oldTripMetrics .
        }
    `;
    try {
        const { success } = await sendSparqlRequest({ update: updateQuery });

        if (!success) {
            throw new Error('SPARQL update failed');
        }

        console.log(`Updated trip metrics for Trip Request ID ${tripRequestId}`);
    } catch (error) {
        console.log(`Error updating trip metrics for trip request: ${error.message}`);
        throw new Error('Failed to update trip metrics for trip request');
    }
}

const updateEndTimeTripRequest = async (tripRequestId) => {
    const updateQuery = `
        PREFIX carshare: <http://example.org/carshare#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        DELETE {
            ?tripRequest carshare:endTime ?oldEndTime .
        }
        INSERT {
            ?tripRequest carshare:endTime "${new Date().toISOString()}"^^xsd:dateTime .
        }
        WHERE {
            ?tripRequest a carshare:TripRequest ;
                carshare:requestID "${tripRequestId}" ;
                carshare:endTime ?oldEndTime .
        }
    `;

    try {
        const { success } = await sendSparqlRequest({ update: updateQuery });

        if (!success) {
            throw new Error('SPARQL update failed');
        }

        console.log(`Updated end time for Trip Request ID ${tripRequestId}`);
    } catch (error) {
        console.log(`Error updating end time for trip request: ${error.message}`);
        throw new Error('Failed to update end time for trip request');
    }
}

const addTripRequest = async (userId, determinePickUpRes) => {
    const clientData = await queryClientByUserId(userId);
    if (!clientData) {
        throw new Error('Client data not found for the provided userId.');
    }

    const tripRequestId = (new Date()).getTime();

    const insertQuery = `
        PREFIX carshare: <http://example.org/carshare#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        INSERT DATA {
            # Trip Request
            carshare:trip_${tripRequestId} a carshare:TripRequest ;
                carshare:requestID "${tripRequestId}" ;
                carshare:fromLocation "${determinePickUpRes.parameters_used.customer_position}" ;
                carshare:toLocation "${determinePickUpRes.parameters_used.destination_position}" ;
                carshare:requestedBy carshare:${clientData.client} ;
                carshare:startTime "${new Date().toISOString()}"^^xsd:dateTime ;
                carshare:endTime "" ;
                carshare:weather "${determinePickUpRes.parameters_used.weather}" ;
                carshare:traffic "${determinePickUpRes.parameters_used.traffic}" ;
                carshare:localEvents "${determinePickUpRes.parameters_used.local_events}" ;
                carshare:timeOfDay "${determinePickUpRes.parameters_used.time_of_day}" ;
                carshare:dayOfWeek "${determinePickUpRes.parameters_used.day_of_week}" ;
                carshare:roadConstructions "${determinePickUpRes.parameters_used.road_constructions}" ;
                carshare:tripMetrics "" .
        }
    `;

    try {
        const { success } = await sendSparqlRequest({ update: insertQuery });

        if (!success) {
            throw new Error('SPARQL update failed');
        }

        console.log(`Inserted trip request for ${userId} with Trip Request ID ${tripRequestId}`);

        return tripRequestId;
    } catch (error) {
        console.log(`Error inserting trip request: ${error.message}`);
        throw new Error('Failed to insert trip request');
    }
};


export default {
    queryClientByUserId,
    queryVehiclePositions,
    queryRoadConstructions,
    updateVehiclePosition,
    updateClientPosition,
    queryResponseServiceFromNlp,
    addTripRequest,
    addTripMetrics,
    queryRoadConstructionsByLocation,
    queryTripRequestById,
    updateEndTimeTripRequest,
    queryResponseServiceFromJson
};