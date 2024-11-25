const mapClientDataToProposalPayload = (clientData) => {
    return {
        age: clientData.age,
        comfort_importance: clientData.comfortImportance,
        driving_proficiency: clientData.drivingProficiency,
        driving_sickness: clientData.drivingSickness,
        family_friendly_features: clientData.familyFriendlyFeatures,
        fuel_type_preference: clientData.fuelTypePreference,
        off_road_capability: clientData.offRoadCapability,
        passenger_amount: clientData.passengerAmount,
        police_record: clientData.policeRecord,
        preferred_route_type: clientData.preferredRouteType,
        preferred_speed: clientData.preferredSpeed,
        safety_importance: clientData.safetyImportance,
        transmission_reference: clientData.transmissionReference
    };
}

export default {
    mapClientDataToProposalPayload
};