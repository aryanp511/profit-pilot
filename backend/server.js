const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const PORT = 5000;
const AI_SERVICE_URL = 'http://127.0.0.1:8000';

// Middleware
app.use(cors());
app.use(express.json());

// Root Route
app.get('/', (req, res) => {
    res.send('Backend is running!');
});

// --- NEW ROUTE: Get General Market News ---
app.get('/api/news', async (req, res) => {
    try {
        // Call the new Python endpoint
        const response = await axios.get(`${AI_SERVICE_URL}/general-news`);
        res.json(response.data);
    } catch (error) {
        console.error("Error fetching general news:", error.message);
        // Return empty list on error instead of crashing frontend
        res.json({ news: [] });
    }
});

// The Smart Route (Analyze specific stock)
app.post('/api/stock', async (req, res) => {
    const { symbol } = req.body;

    if (!symbol) {
        return res.status(400).json({ error: "Stock symbol is required" });
    }

    try {
        console.log(`Analyzing request for: ${symbol}`);
        const response = await axios.post(`${AI_SERVICE_URL}/analyze`, {
            symbol: symbol
        });
        res.json(response.data);

    } catch (error) {
        console.error("Error connecting to AI service:", error.message);
        // Improve error message for frontend
        const status = error.response ? error.response.status : 500;
        res.status(status).json({ error: "Failed to analyze stock. Ensure AI service is running." });
    }
});

// Start Server
app.listen(PORT, () => {
    console.log(`Backend Server running on http://127.0.0.1:${PORT}`);
});