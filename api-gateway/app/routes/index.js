import { Router } from 'express';

const router = Router();

router.get('/', (req, res) => {
  res.status(200).json({
    message: 'API Gateway',
    endpoints: {
      semanticNetwork: '/api/semantic-network',
      responseService: '/api/response-service',
      determinePickUp: '/api/determine-pickup-service',
      proposeAction: '/api/propose-action-service',
      acceptanceService: '/api/acceptance-service',
      proposalService: '/api/proposal-service',
      pricingService: '/api/pricing-service',
    },
    cityMap: '/images/city.svg',
  });
});

export default router;
