const fs = require('fs')
const zip = (a, b) => a.map((k, i) => [k, b[i]]);

const data = fs.readFileSync(process.argv[2], 'utf8').trim().split('\n')

const time = data[0].match(/(\d+)/gm)?.map(it => parseInt(it))
const distance = data[1].match(/(\d+)/gm)?.map(it => parseInt(it))

const races = zip(time, distance)


function race([t, d]) {
    return Math.floor(0.5 * (t + Math.sqrt(t*t - 4 * (d+1)))) -  Math.ceil(0.5 * (t - Math.sqrt(t*t - 4 * (d+1)))) + 1
}

console.log('Part 1', races.map(it=>race(it)).reduce((a, c) => a*c, 1))
const part2 = races.map(it => [`${it[0]}`, `${it[1]}`]).reduce((a,c) => [a[0] + c[0], a[1]+ c[1]], ["", ""]).map(it => parseInt(it))

console.log('Part 2', race(part2))
