const fs = require('fs')

const data = fs.readFileSync(process.argv[2], 'utf8').trim()


const parsed = data.split("\n").map(line => {
    const sets = line.split(":")
    const game_number = sets[0].split(" ")[1]

    const subsets = sets[1].split(";").map(sub => {
        const one_subset = sub.split(",").map(c => {
            [number, color] = c.trim().split(" ")
            return {[color]:  parseInt(number)}
        })

        return Object.assign({red: 0, green: 0, blue: 0}, ...one_subset)
    })

    return {game: parseInt(game_number), subsets: subsets}
})

let part1 = parsed.filter(it => {
    const ok = it.subsets.reduce((acc, curr) => {
        return (curr.red <= 12 && curr.green <= 13 && curr.blue <= 14) && acc
    }, true)
    return ok
})

part1 = part1.reduce((acc, curr) => acc + curr.game, 0)


let part2 = parsed.map(game => {
    const max = game.subsets.reduce((acc, curr) => {
        acc.red = Math.max(acc.red, curr.red)
        acc.green = Math.max(acc.green, curr.green)
        acc.blue = Math.max(acc.blue, curr.blue)
        return acc
    }, {red: 0, green: 0, blue: 0})
    return max.red*max.green*max.blue
}).reduce((acc, curr) => acc + curr, 0)

console.log("Part 1: ", part1)
console.log("Part 2: ", part2)