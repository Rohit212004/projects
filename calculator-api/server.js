const express = require('express');
const app = express();

app.use(express.json()); // for parsing JSON requests

// GET endpoint (e.g., /add?num1=5&num2=3)
app.get('/:operation', (req, res) => {
    const { num1, num2 } = req.query;
    const operation = req.params.operation;

    const a = parseFloat(num1);
    const b = parseFloat(num2);

    if (isNaN(a) || isNaN(b)) {
        return res.status(400).json({ error: "Invalid numbers" });
    }

    let result;
    switch (operation) {
        case 'add':
            result = a + b;
            break;
        case 'subtract':
            result = a - b;
            break;
        case 'multiply':
            result = a * b;
            break;
        case 'divide':
            if (b === 0) return res.status(400).json({ error: "Cannot divide by zero" });
            result = a / b;
            break;
        default:
            return res.status(400).json({ error: "Unknown operation" });
    }

    res.json({ operation, num1: a, num2: b, result });
});

// POST endpoint (send JSON body)
app.post('/:operation', (req, res) => {
    const { num1, num2 } = req.body;
    const operation = req.params.operation;

    const a = parseFloat(num1);
    const b = parseFloat(num2);

    if (isNaN(a) || isNaN(b)) {
        return res.status(400).json({ error: "Invalid numbers" });
    }

    let result;
    switch (operation) {
        case 'add':
            result = a + b;
            break;
        case 'subtract':
            result = a - b;
            break;
        case 'multiply':
            result = a * b;
            break;
        case 'divide':
            if (b === 0) return res.status(400).json({ error: "Cannot divide by zero" });
            result = a / b;
            break;
        default:
            return res.status(400).json({ error: "Unknown operation" });
    }

    res.json({ operation, num1: a, num2: b, result });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Calculator API is running on http://localhost:${PORT}`);
});
