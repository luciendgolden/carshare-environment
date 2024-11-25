import { createProxyMiddleware } from 'http-proxy-middleware';

const semNetProxy = createProxyMiddleware({
  target: process.env.SEMANTIC_NETWORK_URL,
  changeOrigin: true,
  pathRewrite: {
    '^/api/semnet-service': '',
  },
  logLevel: 'debug',
});

const responseProxy = createProxyMiddleware({
  target: process.env.RESPONSE_SERVICE_URL,
  changeOrigin: true,
  pathRewrite: {
    '^/api/response-service': '',
  },
  logLevel: 'debug',
});

const determinePickupProxy = createProxyMiddleware({
  target: process.env.DETERMINE_PICKUP_URL,
  changeOrigin: true,
  pathRewrite: {
    '^/api/determine-pickup-service': '',
  },
  logLevel: 'debug',
});

const proposeActionProxy = createProxyMiddleware({
  target: process.env.PROPOSE_ACTION_URL,
  changeOrigin: true,
  pathRewrite: {
    '^/api/propose-action-service': '',
  },
  logLevel: 'debug',
});

const acceptanceProxy = createProxyMiddleware({
  target: process.env.ACCEPTANCE_SERVICE_URL,
  changeOrigin: true,
  pathRewrite: {
    '^/api/acceptance-service': '',
  },
  logLevel: 'debug',
});

const proposalProxy = createProxyMiddleware({
  target: process.env.PROPOSAL_SERVICE_URL,
  changeOrigin: true,
  pathRewrite: {
    '^/api/proposal-service': '',
  },
  logLevel: 'debug',
});

const optimizePriceProxy = createProxyMiddleware({
  target: process.env.OPTIMIZE_PRICE_URL,
  changeOrigin: true,
  pathRewrite: {
    '^/api/pricing-service': '',
  },
  logLevel: 'debug',
});


export default {
  semNetProxy,
  responseProxy,
  determinePickupProxy,
  proposeActionProxy,
  acceptanceProxy,
  proposalProxy,
  optimizePriceProxy
};
