import axios from 'axios';
import express from 'express';

import path from 'path';
import { fileURLToPath } from 'url';

import cors from 'cors';
import cookieParser from 'cookie-parser';
import logger from 'morgan';
import indexRouter from './app/routes/index.js';
import apiRouter from './app/routes/apiRouter.js';
import alexaRouter from './app/routes/alexaRouter.js';
import { createClient } from 'redis';
import mqtt from 'mqtt';

const app = express();

// Set Axios default base URL
axios.defaults.baseURL = process.env.DEFAULT_BASE_URL;

const redisHost = process.env.REDIS_HOST || 'localhost';
const redisPort = process.env.REDIS_PORT || 6379;

const mqttBrokerUrl = process.env.MQTT_BROKER_URL || 'mqtt://192.168.0.101';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// API Router
app.use('/api', apiRouter);

// Middleware
app.use(logger('dev'));
app.use(cors());
app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// Static files
app.use(express.static(path.join(__dirname, '/public/')))

// View engine setup
app.set('views', path.join(__dirname, '/app/views'));
app.set('view engine', 'ejs');


(async () => {
    try {
        // Connect to MQTT
        const mqttclient = mqtt.connect(mqttBrokerUrl);

        // Connect to Redis
        const redisClient = createClient({
            url: `redis://${redisHost}:${redisPort}`, // Use URL format for Redis connection
        });

        redisClient.on('error', (err) => console.log('Redis Client Error', err));
        await redisClient.connect();

        // Index Router
        app.use('/', indexRouter);

        // Alexa Router with Redis Client
        app.use('/alexa', (req, res, next) => {
            req.redisClient = redisClient;
            req.mqttclient = mqttclient;
            next();
        }, alexaRouter);
    } catch (err) {
        console.error('Error starting the app:', err);
    }
})();

export default app;