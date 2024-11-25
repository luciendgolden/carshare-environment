/**
 * 
* @param {"client":"clientBob","id":"amzn1.ask.account.AMA6XG6DRTXSJ7Z5WBWTDOYUEBW4YC4VT2ZXXVDSZEGSSRFSXLG5SK5A3RMCQRAO72VSU7YWSRY3QCX2I4MNUHP6VUJBVVF5VWXQQMIPROGWL56WMF36SLU7U5G2C66523PPM2TS3ULRQP5NOVQXTTDCYGMYIZAWAMF7MPO6JAA63WQZNYAY7Q4SHIVVGJMAOQC2XQURXFX7ZD7LYUMK6XFZRS643W5GVT6SXOVPPU","position":"H","age":"93","gender":"male","accountType":"standard","comfortImportance":"High","drivingProficiency":"Inexperienced","drivingSickness":"Rarely","familyFriendlyFeatures":"Yes","fuelTypePreference":"Gasoline","offRoadCapability":"Yes","passengerAmount":5,"policeRecord":"Clean","preferredRouteType":"Mixed","preferredSpeed":"Fast","safetyImportance":"Top Priority","transmissionReference":"Automatic"} client 
 * @param {"optimal_pickup":"Car 3","car route":["H"],"car movements":{},"distance to nearest car":0,"distance to destination":2,"customer to destination path":["H","I","J"],"customer movements":{"H_I":"r","I_J":"s"},"Rule":"Nearest car without road constructions","parameters_used":{"customer_position":"H","destination_position":"J","car1_position":"A","car2_position":"C","car3_position":"H","weather_location":"Vienna","weather":"rainy","traffic":"no","local_events":"no","road_constructions":"B","time_of_day":"morning","day_of_week":"monday","age":"93","gender":"male","account_type":"standard","customer_destination_distance":2,"car_destination_distances":{"Car 1":5,"Car 2":6,"Car 3":2},"car_destination_paths":{"Car 1":["A","B","G","H","I","J"],"Car 2":["C","D","E","F","H","I","J"],"Car 3":["H","I","J"]},"nearest_car":"Car 3","second_nearest_car":"Car 1","third_nearest_car":"Car 2"},"mapped car movements":{},"mapped customer movements":{"H_I":"sl,rl,sl","I_J":"sl"},"tripRequestId":1725882786496,"tripMetrics":{"temperature":13,"ride_time":10,"fuel":4,"traffic_congestion":10,"visibility":50,"poi":0.7,"car_maintenance_history":1,"daytime":"11:53"},"actionsResponse":{"actions":[{"name":"route_recalculation","value":49.95},{"name":"headlight_intensity","unit":"%","value":89.94},{"name":"speed_adjustment","unit":"km/h","value":4.52}]}} params 
 * @returns {"options":{"central_point":{"lat":48.20849,"lon":16.37208},"threshold_km":10},"parameters":{"base_price":0.3,"customer_loyalty":1,"weather_condition":"moderate","day_of_week":3,"remoteness":"True","loyalty_discount":0.1,"weather_surcharge":1.2,"weekend_surcharge":1.1,"remoteness_surcharge":1.15},"trip":{"start":{"lat":48.22011,"lon":16.35612},"end":{"lat":48.21302,"lon":16.36076}}}
 */
const mapParamsToPayload = (client, params) => {
    // TODO: Think about more dynamically generating the payload..
    const options = {
        central_point: {
            lat: 48.20849,
            lon: 16.37208
        },
        threshold_km: 10
    };

    const parameters = {
        base_price: 0.3,
        customer_loyalty: client.familyFriendlyFeatures === 'Yes' ? 1 : 0,
        weather_condition: params.parameters_used.weather,
        day_of_week: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].indexOf(params.parameters_used.day_of_week.toLowerCase()),
        remoteness: params['customer to destination path'].length > 2,
        loyalty_discount: 0.1,
        weather_surcharge: 1.2,
        weekend_surcharge: 1.1,
        remoteness_surcharge: 1.15
    };

    const trip = {
        start: {
            lat: 48.22011,
            lon: 16.35612
        },
        end: {
            lat: 48.21302,
            lon: 16.36076
        }
    };

    const payload = {
        options: options,
        parameters: parameters,
        trip: trip
    };

    return payload;
};

export default {
    mapParamsToPayload
};