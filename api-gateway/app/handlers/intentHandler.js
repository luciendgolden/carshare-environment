import {
  launchRequestHandler,
  requestRideIntentHandler,
  confirmRideIntentHandler,
  searchQueryIntentHandler,
  updatePositionIntentHandler,
  cancelCurrentRideIntentHandler
} from './handler.js';

const intentHandlers = {
  LaunchRequest: launchRequestHandler,
  RequestRide: requestRideIntentHandler,
  ConfirmRide: confirmRideIntentHandler,
  SearchQueryIntent: searchQueryIntentHandler,
  GlobalSearchIntent: searchQueryIntentHandler,
  UpdatePositionIntent: updatePositionIntentHandler,
  CancelRideIntent: cancelCurrentRideIntentHandler
};

export default intentHandlers;
