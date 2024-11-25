const getCurrentTime = () => {
    const now = new Date();
    return now.toISOString().slice(11, 16);
};

const getRandomInt = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};

const getPoiByCity = (city) => {
    const cityPoiMap = {
        'Vienna': 0.7,
        'Paris': 0.9,
        'New York': 0.8,
        'Tokyo': 0.85,
        'Berlin': 0.6,
        'Sydney': 0.75,
        'London': 0.88,
        'Barcelona': 0.8,
    };

    return cityPoiMap[city] || 0.5;
};

const getTripMetrics = (determinePickUpRes) => {
   const { weather, weather_location, traffic } = determinePickUpRes.parameters_used;

   let temperature = 20;
   let visibility = 100;

   if (weather === 'sunny') {
       temperature = getRandomInt(20, 30);
       visibility = 150;
   } else if (weather === 'rainy') {
       temperature = getRandomInt(10, 18);
       visibility = 50;
   } else {
       temperature = getRandomInt(15, 25);
       visibility = 80;
   }

   const rideTime = determinePickUpRes['car route'].length * 10;
   const fuel = determinePickUpRes['distance to destination'] * 2;
   const trafficCongestion = traffic === 'no' ? 10 : 30;
   const poi = getPoiByCity(weather_location);
   const carMaintenanceHistory = getRandomInt(1, 5);
   const daytime = getCurrentTime();

    return {
        temperature: temperature,
        ride_time: rideTime,
        fuel: fuel,
        traffic_congestion: trafficCongestion,
        visibility: visibility,
        poi: poi,
        car_maintenance_history: carMaintenanceHistory,
        daytime: daytime
    };
}

const extractIncentives = (actions) => {
    return actions.filter(action => action.incentive);
}

const extractActions = (actions) => {
    return actions.filter(action => !action.incentive);
}

export default {
    getTripMetrics,
    extractIncentives,
    extractActions
}