const app = require('express')();
const express = require('express');
const { type } = require('os');
const path = require('path');
const http = require('http').createServer(app);
const { spawn } = require('child_process');

const pyProcess = spawn('python3', ['MotorControl/main.py'])


console.log('hi :3');

pyProcess.stdout.on('data', (data) => {
    console.log('Data from Python:', data.toString());
});

// Handle errors
pyProcess.stderr.on('data', (data) => {
    console.error('Error from Python:', data.toString());
});

pyProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
});

app.get('/', (req, res) => {
    res.sendFile(__dirname + "/src/index.html");
});

app.post('/control', express.json(), (req, res) => {
    const { angle } = req.body;

    if(typeof(angle) == undefined) {
        console.error('Error executing python script: ${error}');
        return res.status(500).send('Error controlling servo motor.');
    }
    console.log(angle);
    pyProcess.stdin.write(JSON.stringify(angle));
    pyProcess.stdin.end();
})

app.use('/src', express.static(path.join(__dirname, 'src')));

http.listen('8080', () => {
    console.log('listening on 8080');
});

