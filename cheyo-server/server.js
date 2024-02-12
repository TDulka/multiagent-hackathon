const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;
const { v4: uuidv4 } = require('uuid');

const messageLog = {
    all: [],
}

const users = []
const secrets = ['SEC', 'RET', 'OTHER', 'AB', 'CD', 'EED', 'FGH', 'IJK', 'LMN', 'OPQ', 'RST', 'UVW', 'XYZ']
let gameStarted = false
let gameFinished = false


// Middleware to parse JSON bodies
app.use(express.json());

// POST /join route
app.post('/api/join', (req, res) => {
    // Implement join logic here
    userId = uuidv4()
    users.push(userId)

    res.status(200).send({ userId: userId, secret: secrets[users.length], gameStarted: false });
});

app.post('/api/check', (req, res) => {
    // Implement join logic here
    if (users.length > 2) {
        gameStarted = true
        gameFinished = false
        for (let i = 0; i < users.length; i++) {
            messageLog[users[i]] = {}
            for (let j = 0; j < users.length; j++) {
                if (i!= j) {
                    messageLog[users[i]][users[j]] = []
                }
            }
        }
    }
    res.status(200).send({ gameStarted, users: users });
});

// POST /guess route
app.post('/api/guess', (req, res) => {
    const { userId, guess } = req.body;
    // Implement guess logic here
    res.status(200).send({ userId, guess, message: 'Incorrect.' });
});

// POST /chat route
app.post('/api/chat', (req, res) => {
    const { userId, to, content } = req.body; 

    if (to == 'all') {
        messageLog['all'].push({ from: userId, content })
    }
    else {
        messageLog[to][userId].push({ from: userId, content })
        messageLog[userId][to].push({ from: userId, content })
    }

    res.status(200).send({ userId, to, content, message: 'Chat message sent.' });
});

// GET /chat route for retrieving chat history
app.get('/api/chat', (req, res) => {
    const { userId } = req.query;
    chat = {
        all: messageLog['all'],
        ...messageLog[userId]
    }
    // Implement chat history retrieval logic here
    res.status(200).send(chat);
});

app.get('/api/users', (req, res) => {
    // Implement chat history retrieval logic here
    res.status(200).send(users);
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
