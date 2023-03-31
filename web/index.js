"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var express_1 = require("express");
var app = (0, express_1.default)();
app.post('/api/prompt', function (req, res) {
    res.send('Hello word');
});
app.listen(3000, function () {
    console.log('Janus is listening on port 3000. Ready to serve web traffic.');
});
