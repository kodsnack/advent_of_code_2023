const fs = require('fs')

const data = fs.readFileSync(process.argv[2], 'utf8').trim()

const part1 = data.split('\n')
    .map(it => it.trim())
    .map(line => {
        const integers = line.split('')
            .filter(c => c >= '0' && c <= '9')
        
        return parseInt(integers[0]+integers[integers.length-1])
            
    })
    .reduce((acc, curr) => acc + curr, 0)




const part2 = data.split('\n')
    .map(it => it.trim())
    .map(line => {
        const numbers = {
            'one':  1,
            'two':  2,
            'three': 3,
            'four':  4,
            'five':  5,
            'six':  6,
            'seven':  7,
            'eight':  8,
            'nine': 9
        }

        const m = []
        for(let i = 0; i < line.length; i++) {
            Object.keys(numbers).forEach(number => {
                if(line.slice(i).startsWith(number)) m.push(numbers[number])
            })
            if (!isNaN(line[i])) m.push(parseInt(line[i]))
        }
        return m[0]*10+m[m.length-1]
            
    })
    .reduce((acc, curr) => acc + curr, 0)

    console.log("Part 1: ", part1)
    console.log("Part 2: ", part2)