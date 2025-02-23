const app = require('express')();
const express = require('express');
const path = require('path');
const http = require('http').createServer(app);
console.log('hi');

app.get('/', (req, res) => {
    res.sendFile(__dirname + "/src/index.html");
});

app.

app.use('/src', express.static(path.join(__dirname, 'src')));

http.listen('8080', () => {
    console.log('listening on 8080');
});

