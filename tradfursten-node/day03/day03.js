const fs = require('fs')

const data = fs.readFileSync(process.argv[2], 'utf8').trim()

function neighbours(x, y) {
    return [
        [x-1, y-1], [x, y - 1], [x + 1, y - 1],
        [x-1, y], [x, y], [x + 1, y],
        [x-1, y+1], [x, y + 1], [x +1, y + 1]
    ]
}

function get_neighbours(x, y, grid, type) {
    return neighbours(x, y).map(it => grid[it])
    .filter(it => it && it.type === type)
}

const grid = {}
let max_x = 0
let max_y = 0

data.split("\n").forEach((line, y) => {
    for(let x = 0; x < line.length; x++) {
        if(line[x] >= '0' && line[x] <= '9') {
            if(x != 0 && grid[[x-1, y]] && grid[[x-1, y]].type === 'part' ) {
                grid[[x-1, y]].value = grid[[x-1, y]].value * 10 + parseInt(line[x])
                grid[[x, y]] = grid[[x - 1, y]]
            } else {
                grid[[x,y]] = {type: 'part', value: parseInt(line[x]), id: Math.random()};
            }
        } else if(line[x] != '.') {
            grid[[x,y]] = {type: 'symbol', value: line[x], id: Math.random()}
        } 
        max_x = Math.max(max_x, x)
    }
    max_y = Math.max(max_y, y)
})

const set = new Set()

const next_to_symbol = new Set()

for(let y = 0; y <= max_y; y++) {
    for(let x = 0; x <= max_x; x++) {
        if(grid[[x, y]] && grid[[x,y]].type === 'part' && !next_to_symbol.has(grid[[x,y]]) &&  get_neighbours(x, y, grid, 'symbol').length == 0) {
            set.add(grid[[x,y]])
        }
        if(grid[[x, y]] && grid[[x,y]].type === 'part' &&  get_neighbours(x, y, grid, 'symbol').length > 0) {
            next_to_symbol.add(grid[[x,y]])
            set.delete(grid[[x, y]])
        }
    }
}

const part1 = [... next_to_symbol].reduce((acc, curr) => {
    return acc + curr.value
}, 0)

console.log('Part 1', part1)



let part2 = 0


for(let y = 0; y <= max_y; y++) {
    for(let x = 0; x <= max_x; x++) {
        if(grid[[x, y]] && grid[[x,y]].type === 'symbol' && grid[[x,y]].value === '*') {
            const parts = new Set(get_neighbours(x, y, grid, 'part'))
            if(parts.size === 2) {
                part2 += [... parts].reduce((acc, curr) => acc * curr.value, 1)
            }
        }
    }
}



console.log("Part 2", part2)

  
  