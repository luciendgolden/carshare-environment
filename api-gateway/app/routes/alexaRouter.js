import express from 'express';
import intentHandlers from '../handlers/intentHandler.js';

const router = express.Router();

router.post('/intent', async (req, res) => {
    console.log(req.body);

    const intentName = req.body.intentName;
    const slots = req.body.slots || {};
    const userId = req.body.userId || null;
    const redisClient = req.redisClient;
    const mqttclient = req.mqttclient;

    if (intentHandlers[intentName]) {
      try {
        const response = await intentHandlers[intentName]({ ...slots, userId }, redisClient,mqttclient);
        res.json({
          success: true,
          message: response,
        });
      } catch (error) {
        console.log('Error handling request:', error);
        
        res.status(500).json({
          success: false,
          message: 'Internal Server Error',
        });
      }
    } else {
      res.status(400).json({
        success: false,
        message: 'Unknown intent',
      });
    }
  });

export default router;