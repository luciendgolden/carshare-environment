import express from 'express';
import proxy from '../proxies/proxy.js';

const router = express.Router();

router.use('/semantic-network', proxy.semNetProxy);
router.use('/response-service', proxy.responseProxy);
router.use('/determine-pickup-service', proxy.determinePickupProxy);
router.use('/propose-action-service', proxy.proposeActionProxy);
router.use('/acceptance-service', proxy.acceptanceProxy);
router.use('/proposal-service', proxy.proposalProxy);
router.use('/pricing-service', proxy.optimizePriceProxy);

export default router;
