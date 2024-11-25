const rideAcceptanceMapping = {
    "customerMapping": { 0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7 },
    "predDemandMapping": { 'high': 0, 'stable': 1, 'low': 2 },
    "weatherMapping": { 'rainy': 0, 'cloudy': 1, 'sunny': 2 },
}

const mapInputParamsToPayload = (inputParams) => {
    const payload = {
        customer_rating: 0,
        pred_demand: 0,
        weather: 0
    };

    if (inputParams.rating !== undefined) {
        payload.customer_rating = Math.min(Math.max(parseInt(inputParams.rating), 0), 7);
    }

    if (inputParams.demand !== undefined) {
        payload.pred_demand = Math.min(Math.max(parseInt(inputParams.demand), 0), 2);
    }

    if (inputParams.weather !== undefined) {
        payload.weather = Math.min(Math.max(parseInt(inputParams.weather), 0), 2);
    }

    return payload;
}

const determineRating = (parameters) => {
    const age = parameters.age;
    if (age < 25) return 4;
    else if (age < 40) return 5;
    else return 6;
}

const determineDemand = (parameters) => {
    const predDemandMapping = rideAcceptanceMapping.predDemandMapping;
    const traffic = parameters.traffic.toLowerCase();
    const localEvents = parameters.local_events.toLowerCase();

    if (traffic === 'high' || localEvents === 'yes') {
        return predDemandMapping['high'];
    } else if (traffic === 'medium' || localEvents === 'no') {
        return predDemandMapping['stable'];
    } else {
        return predDemandMapping['low'];
    }
}

const determineWeather = (parameters) => {
    const weather = parameters.weather.toLowerCase();
    const weatherMapping = rideAcceptanceMapping.weatherMapping;
    return weatherMapping[weather] !== undefined ? weatherMapping[weather] : 0;
}

export default {
    mapInputParamsToPayload,
    determineDemand,
    determineRating,
    determineWeather
}