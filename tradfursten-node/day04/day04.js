const fs = require('fs')

const data = fs.readFileSync(process.argv[2], 'utf8').trim()

const part1 = data.split('\n').map(line => {
    const [winning, numbers] = line.split(":")[1].trim().split('|')

    const winningArray = winning.trim().split(/\s+/)

    const numbersArray = numbers.trim().split(/\s+/)

    const matches = winningArray.filter( it => numbersArray.includes(it)).length
    return matches ? 2 ** (matches - 1): 0
}).reduce((acc, curr) => acc + curr, 0)


const cards = []

data.split('\n')
    .reverse()
    .forEach(line => {
        const [winning, numbers] = line.split(":")[1].trim().split('|')

        const winningArray = winning.trim().split(/\s+/)
    
        const numbersArray = numbers.trim().split(/\s+/)
    
        const matches = winningArray.filter( it => numbersArray.includes(it)).length
        if (matches) {
            cards.push(cards.slice(-matches).reduce((a, c) => a + c, 0) + 1)
        } else {
            cards.push(1)
        }
    })


console.log('Part 1', part1)

console.log('Part 2', cards.reduce((acc, curr) => acc + curr, 0))