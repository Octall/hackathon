const app = require('express')();
const express = require('express');
const { type } = require('os');
const path = require('path');
const http = require('http').createServer(app);
const { spawn } = require('child_process');

var bodyParser = require('body-parser');

var currentYaw = 0;
var currentPitch = 0;

const pyProcess = spawn('python3', ['MotorControl/main.py']);



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

app.use(bodyParser.json());

app.post('/control', (req, res) => {
    const { angle, direction } = req.body;
    console.log("hit")
    console.log(direction);
    console.log(angle);

    
    if (typeof direction === 'undefined') {
        return res.status(400).send('Missing angle parameter');
    }


    switch(direction){
        case "up":
            currentPitch += angle;
            break;
        case "down":
            currentPitch -= angle;
            break;
        case "right":
            currentYaw += angle;
            break;
        case "left":
            currentYaw -= angle;
            break;
        default:
            throw(undefined);
    }
    

    pyProcess.stdin.write(JSON.stringify({yaw: currentYaw, pitch: currentPitch}) + "\n");

    res.send("good");
})

app.use('/src', express.static(path.join(__dirname, 'src')));

http.listen('8080', () => {
    console.log('listening on 8080');
});

