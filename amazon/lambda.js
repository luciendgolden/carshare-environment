/* *
 * This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK (v2).
 * Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
 * session persistence, api calls, and more.
 * */
const Alexa = require('ask-sdk-core');
const axios = require('axios');

/**
 * TBD: Change to respective api-gateway backend URL 
 */
const BACKEND_API_GATEWAY = 'https://b98b-2001-62a-4-40e-4043-5574-3efe-dabf.ngrok-free.app'


const LaunchRequestHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'LaunchRequest';
    },
    async handle(handlerInput) {
        const userId = handlerInput.requestEnvelope.session.user.userId;

        const result = await launchRequest(userId);

        if (result.success) {
            const speakOutput = result.message;
            handlerInput.attributesManager.setSessionAttributes({ isUserAuthenticated: true });
            return handlerInput.responseBuilder
                .speak(speakOutput)
                .getResponse();
        } else {
            const speakOutput = "I'm sorry, I couldn't find your account. Please register first.";
            handlerInput.attributesManager.setSessionAttributes({ isUserAuthenticated: false });
            return handlerInput.responseBuilder 
                .speak(speakOutput)
                .getResponse();
        }
    }
};

async function launchRequest(userId) {
    const url = `${BACKEND_API_GATEWAY}/alexa/intent`;
    const payload = {
        intentName: 'LaunchRequest',
        userId: userId
    };

    try {
        const res = await axios.post(url, payload);
        return res.data;
    } catch (error) {
        console.error("Error checking user:", error);
        return { success: false, message: "Internal Server Error" };
    }
}


const RequestRideIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'RequestRide';
    },
    async handle(handlerInput) {
        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();

        if (!sessionAttributes.isUserAuthenticated) {
            const speakOutput = "You are not authorized to use this service. Please register first.";
            return handlerInput.responseBuilder
                .speak(speakOutput)
                .getResponse();
        }
        
        const pickupLocation = Alexa.getSlotValue(handlerInput.requestEnvelope, 'PickupLocation');
        const destinationLocation = Alexa.getSlotValue(handlerInput.requestEnvelope, 'DestinationLocation');
        
        const userId = handlerInput.requestEnvelope.session.user.userId;

        const response = await requestRide(pickupLocation, destinationLocation, userId);
        return handlerInput.responseBuilder
            .speak(response)
            .reprompt(response)
            .getResponse();
    }
};

async function requestRide(pickupLocation, destinationLocation, userId) {
    const url = `${BACKEND_API_GATEWAY}/alexa/intent`;
    const payload = {
        intentName: 'RequestRide',
        userId: userId,
        slots: {
            PickupLocation: pickupLocation,
            DestinationLocation: destinationLocation
        }
    };

    try {
        const res = await axios.post(url, payload);
        const result = res.data;

        if (result.success) {
            return result.message;
        } else {
            return `I'm sorry, I couldn't process your ride request at the moment. ${result.message}`;
        }
    } catch (error) {
        console.error("Error making request:", error);
        return "I'm sorry, I couldn't process your ride request at the moment.";
    }
}

const ConfirmRideIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'ConfirmRide';
    },
    async handle(handlerInput) {
        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();

        if (!sessionAttributes.isUserAuthenticated) {
            const speakOutput = "You are not authorized to use this service. Please register first.";
            return handlerInput.responseBuilder
                .speak(speakOutput)
                .getResponse();
        }
        
        const userId = handlerInput.requestEnvelope.session.user.userId;
        
        const response = await confirmRide(userId);
        return handlerInput.responseBuilder
            .speak(response)
            .getResponse();
    }
};

async function confirmRide(userId) {
    const url = `${BACKEND_API_GATEWAY}/alexa/intent`;
    const payload = {
        intentName: 'ConfirmRide',
        userId: userId 
    };

    try {
        const res = await axios.post(url, payload);
        const result = res.data;

        if (result.success) {
            return result.message;
        } else {
            return `I'm sorry, I couldn't confirm your ride. ${result.message}`;
        }
    } catch (error) {
        console.error("Error making request:", error);
        return "I'm sorry, I couldn't confirm your ride at the moment.";
    }
}

const SearchQueryIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'SearchQueryIntent';
    },
    async handle(handlerInput) {
        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();
        const userId = handlerInput.requestEnvelope.session.user.userId;
        const query = Alexa.getSlotValue(handlerInput.requestEnvelope, 'query');

        if (!sessionAttributes.isUserAuthenticated) {
            const speakOutput = "You are not authorized to use this service. Please register first.";
            return handlerInput.responseBuilder
                .speak(speakOutput)
                .getResponse();
        }

        const response = await handleSearchQuery(userId, query);

        return handlerInput.responseBuilder
            .speak(response)
            .getResponse();
    }
};

async function handleSearchQuery(userId, query) {
    const url = `${BACKEND_API_GATEWAY}/alexa/intent`;
    const payload = {
        intentName: 'SearchQueryIntent',
        userId: userId,
        slots: {
            query: query
        }
    };

    try {
        const res = await axios.post(url, payload);
        const result = res.data;

        if (result.success) {
            return result.message;
        } else {
            return `I'm sorry, I couldn't find information on ${query}. ${result.message}`;
        }
    } catch (error) {
        console.error("Error processing search query:", error);
        return `I'm sorry, I couldn't process your request for ${query} at the moment.`;
    }
}

const GlobalSearchIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'GlobalSearchIntent';
    },
    async handle(handlerInput) {
        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();
        const userId = handlerInput.requestEnvelope.session.user.userId;
        const query = Alexa.getSlotValue(handlerInput.requestEnvelope, 'query');

        if (!sessionAttributes.isUserAuthenticated) {
            const speakOutput = "You are not authorized to use this service. Please register first.";
            return handlerInput.responseBuilder
                .speak(speakOutput)
                .getResponse();
        }

        const response = await handleGlobalSearchQuery(query);

        return handlerInput.responseBuilder
            .speak(response)
            .getResponse();
    }
};

async function handleGlobalSearchQuery(query) {
    const url = `${BACKEND_API_GATEWAY}/alexa/intent`;
    const payload = {
        intentName: 'GlobalSearchIntent',
        slots: {
            query: query
        }
    };

    try {
        const res = await axios.post(url, payload);
        const result = res.data;

        if (result.success) {
            return result.message;
        } else {
            return `I'm sorry, I couldn't find information on ${query}. ${result.message}`;
        }
    } catch (error) {
        console.error("Error processing global search query:", error);
        return `I'm sorry, I couldn't process your request for ${query} at the moment.`;
    }
}

const UpdatePositionIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'UpdatePositionIntent';
    },
    async handle(handlerInput) {
        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();

        if (!sessionAttributes.isUserAuthenticated) {
            const speakOutput = "You are not authorized to use this service. Please register first.";
            return handlerInput.responseBuilder
                .speak(speakOutput)
                .getResponse();
        }
        
        const newPosition = Alexa.getSlotValue(handlerInput.requestEnvelope, 'NewPosition');
        const userId = handlerInput.requestEnvelope.session.user.userId;

        const response = await updatePosition(newPosition, userId);
        return handlerInput.responseBuilder
            .speak(response)
            .getResponse();
    }
};

async function updatePosition(newPosition, userId) {
    const url = `${BACKEND_API_GATEWAY}/alexa/intent`;
    const payload = {
        intentName: 'UpdatePositionIntent',
        userId: userId,
        slots: {
            NewPosition: newPosition
        }
    };

    try {
        const res = await axios.post(url, payload);
        const result = res.data;

        if (result.success) {
            return result.message;
        } else {
            return `I'm sorry, I couldn't update your position at the moment. ${result.message}`;
        }
    } catch (error) {
        console.error("Error updating position:", error);
        return "I'm sorry, I couldn't update your position at the moment.";
    }
}

const CancelRideIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'CancelRideIntent';
    },
    async handle(handlerInput) {
        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();

        if (!sessionAttributes.isUserAuthenticated) {
            const speakOutput = "You are not authorized to use this service. Please register first.";
            return handlerInput.responseBuilder
                .speak(speakOutput)
                .getResponse();
        }

        const userId = handlerInput.requestEnvelope.session.user.userId;

        const response = await cancelCurrentRide(userId);
        return handlerInput.responseBuilder
            .speak(response)
            .getResponse();
    }
};

async function cancelCurrentRide(userId) {
    const url = `${BACKEND_API_GATEWAY}/alexa/intent`;
    const payload = {
        intentName: 'CancelRideIntent',
        userId: userId
    };

    try {
        const res = await axios.post(url, payload);
        const result = res.data;

        if (result.success) {
            return result.message;
        } else {
            return `I'm sorry, I couldn't cancel your ride. ${result.message}`;
        }
    } catch (error) {
        console.error("Error cancelling ride:", error);
        return "I'm sorry, I couldn't cancel your ride at the moment.";
    }
}


const HelloWorldIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'HelloWorldIntent';
    },
    handle(handlerInput) {
        const speakOutput = 'Hello World!';

        return handlerInput.responseBuilder
            .speak(speakOutput)
            //.reprompt('add a reprompt if you want to keep the session open for the user to respond')
            .getResponse();
    }
};

const HelpIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.HelpIntent';
    },
    handle(handlerInput) {
        const speakOutput = 'You can say hello to me! How can I help?';

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};

const CancelAndStopIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && (Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.CancelIntent'
                || Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.StopIntent');
    },
    handle(handlerInput) {
        const speakOutput = 'Goodbye!';

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .getResponse();
    }
};
/* *
 * FallbackIntent triggers when a customer says something that doesn’t map to any intents in your skill
 * It must also be defined in the language model (if the locale supports it)
 * This handler can be safely added but will be ingnored in locales that do not support it yet 
 * */
const FallbackIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.FallbackIntent';
    },
    handle(handlerInput) {
        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();

        if (!sessionAttributes.isUserAuthenticated) {
            const speakOutput = "You are not authorized to use this service. Please register first.";
            return handlerInput.responseBuilder
                .speak(speakOutput)
                .getResponse();
        }

        const speakOutput = 'Sorry, I don\'t know about that. Please try again.';

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};
/* *
 * SessionEndedRequest notifies that a session was ended. This handler will be triggered when a currently open 
 * session is closed for one of the following reasons: 1) The user says "exit" or "quit". 2) The user does not 
 * respond or says something that does not match an intent defined in your voice model. 3) An error occurs 
 * */
const SessionEndedRequestHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'SessionEndedRequest';
    },
    handle(handlerInput) {
        console.log(`~~~~ Session ended: ${JSON.stringify(handlerInput.requestEnvelope)}`);
        // Any cleanup logic goes here.
        return handlerInput.responseBuilder.getResponse(); // notice we send an empty response
    }
};
/* *
 * The intent reflector is used for interaction model testing and debugging.
 * It will simply repeat the intent the user said. You can create custom handlers for your intents 
 * by defining them above, then also adding them to the request handler chain below 
 * */
const IntentReflectorHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest';
    },
    handle(handlerInput) {
        const intentName = Alexa.getIntentName(handlerInput.requestEnvelope);
        const speakOutput = `You just triggered ${intentName}`;

        return handlerInput.responseBuilder
            .speak(speakOutput)
            //.reprompt('add a reprompt if you want to keep the session open for the user to respond')
            .getResponse();
    }
};
/**
 * Generic error handling to capture any syntax or routing errors. If you receive an error
 * stating the request handler chain is not found, you have not implemented a handler for
 * the intent being invoked or included it in the skill builder below 
 * */
const ErrorHandler = {
    canHandle() {
        return true;
    },
    handle(handlerInput, error) {
        const speakOutput = 'Sorry, I had trouble doing what you asked. Please try again.';
        console.log(`~~~~ Error handled: ${JSON.stringify(error)}`);

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};

/**
 * This handler acts as the entry point for your skill, routing all request and response
 * payloads to the handlers above. Make sure any new handlers or interceptors you've
 * defined are included below. The order matters - they're processed top to bottom 
 * */
exports.handler = Alexa.SkillBuilders.custom()
    .addRequestHandlers(
        RequestRideIntentHandler,
        ConfirmRideIntentHandler,
        SearchQueryIntentHandler,
        GlobalSearchIntentHandler,
        LaunchRequestHandler,
        UpdatePositionIntentHandler,
        CancelRideIntentHandler,
        HelloWorldIntentHandler,
        HelpIntentHandler,
        CancelAndStopIntentHandler,
        FallbackIntentHandler,
        SessionEndedRequestHandler,
        IntentReflectorHandler)
    .addErrorHandlers(
        ErrorHandler)
    .withCustomUserAgent('sample/hello-world/v1.2')
    .lambda();