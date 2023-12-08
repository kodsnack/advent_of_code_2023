const fs = require('fs')

exports.zip = (a, b) => a.map((k, i) => [k, b[i]]);

exports.readFile =(name) => fs.readFileSync(name, 'utf8').trim().split('\n')