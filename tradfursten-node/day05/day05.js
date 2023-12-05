const fs = require('fs')
const { isUndefined } = require('util')

const data = fs.readFileSync(process.argv[2], 'utf8').trim()

const NUMBER = 'number',
        SOIL = 'soil',
        FERTILIZER = 'fertilizer',
        WATER = 'water',
        LIGHT = 'light',
        TEMP = 'temperature',
        HUMIDITY = 'humidity',
        LOCATION = 'location'

let seeds

let step = null

function populate_missing(seeds, to_category, from_category) {
    return seeds.map(seed => {
        if (!seed[to_category]) {
            seed[to_category] = seed[from_category]
        }
        return seed
    })
}

function populate_by_line(seeds, line, to_category, from_category) {
    const from_to = line.split(' ').map(it => parseInt(it))
    return seeds.map(seed => {
        const steps = seed[from_category] - from_to[1]
        if (steps >= 0 && steps < from_to[2]) {
            seed[to_category] = from_to[0] + steps
        }
        return seed
    }) 
}



function parseLine(line, part) {
    if (line.startsWith('seeds:')) {
        if (part === 'part1') {
            seeds = line.match(/(\d+)/g)?.map(it => parseInt(it)).map(it => {return {number: it}} )
        } else if (part === 'part2' ) {
            const seeds_ranges = line.match(/(\d+)/g)?.map(it => parseInt(it))
            seeds = []
            for(let i = 0; i < seeds_ranges.length; i+=2) {
                for(let x = seeds_ranges[i]; x <= seeds_ranges[i]+seeds_ranges[i+1]; x++) {
                    seeds.push({number: x})
                }
            }
        }
    }
    switch (step) {
        case 'seeds_to_soil':
            seeds = populate_by_line(seeds, line, SOIL, NUMBER)
            break;
        case 'soil_to_fertilizer':
            seeds = populate_by_line(seeds, line, FERTILIZER, SOIL)
            break;
        case 'fertilizer_to_water':
            seeds = populate_by_line(seeds, line, WATER, FERTILIZER)
            break;
        case 'water_to_ligth':
            seeds = populate_by_line(seeds, line, LIGHT, WATER)
            break;
        case 'light_to_temperature':
            seeds = populate_by_line(seeds, line, TEMP, LIGHT)
            break;
        case 'temperature_to_humidity':
            seeds = populate_by_line(seeds, line, HUMIDITY, TEMP)
            break;
        case 'humidity_to_location':
            seeds = populate_by_line(seeds, line, LOCATION, HUMIDITY)
            break;
    }
    switch (line) {
        case "seed-to-soil map:":
            step = 'seeds_to_soil'
            break;
            
        case "soil-to-fertilizer map:":
            seeds = populate_missing(seeds, SOIL, NUMBER)
            step = 'soil_to_fertilizer'
            break;
        case "fertilizer-to-water map:":
            seeds = populate_missing(seeds, FERTILIZER, SOIL)
            step = 'fertilizer_to_water'
            break;
        case "water-to-light map:":
            seeds = populate_missing(seeds, WATER, FERTILIZER)
            step = 'water_to_ligth'
            break;
        case "light-to-temperature map:":
            seeds = populate_missing(seeds, LIGHT, WATER)
            step = 'light_to_temperature'
            break;
        case "temperature-to-humidity map:":
            seeds = populate_missing(seeds, TEMP, LIGHT)
            step = 'temperature_to_humidity'
            break;
        case "humidity-to-location map:":
            seeds = populate_missing(seeds, HUMIDITY, TEMP)
            step = 'humidity_to_location'
            break;
    }    
}

data.split('\n')
    .forEach(line => {
        parseLine(line, 'part1')
    })

populate_missing(seeds, LOCATION, HUMIDITY)

const part1 = seeds.reduce((min, curr) => {
    if (curr[LOCATION] < min[LOCATION]) {
        return curr
    } else {
        return min
    }
}, seeds[0])

//console.log(seeds)
console.log('Part 1', part1.location)

function populate_range_by_line(seeds, line, from, to) {
    if (line === "") return 
    const from_to = line.split(' ').map(it => parseInt(it))
    mappers[to].ranges.push(from_to)
    /*return seeds.flatMap(seed => {
        console.log(seed, from_to, line)
        if(seed[from][0]<= from_to[1] + from_to[2] && from_to[1] <= seed[from][1] ) {

            return [seed, seed]
        }
        return seed
    }) 
    */
}

function create_mapper(from, to, next) {
    const ranges = []
    return {
        from: NUMBER,
        to: SOIL,
        ranges: ranges,
        map: (seed) => {
            //console.log('Mapping', seed)
            for(let r of ranges) {
                const steps = seed - r[1]
                if(steps >= 0 && steps < r[2]) {
                    return next? next(r[0] + steps): r[0] + steps
                }
            }
            return next? next(seed): seed
        }
    }
}

seeds = []
mappers = {}
mappers[LOCATION] = create_mapper(HUMIDITY, LOCATION)
mappers[HUMIDITY] = create_mapper(TEMP, HUMIDITY, mappers[LOCATION].map)
mappers[TEMP] = create_mapper(LIGHT, TEMP, mappers[HUMIDITY].map)
mappers[LIGHT] = create_mapper(WATER, LIGHT, mappers[TEMP].map)
mappers[WATER] = create_mapper(FERTILIZER, WATER, mappers[LIGHT].map)
mappers[FERTILIZER] = create_mapper(SOIL, FERTILIZER, mappers[WATER].map)
mappers[SOIL] = create_mapper(NUMBER, SOIL, mappers[FERTILIZER].map)
step = null
data.split('\n')
    .forEach(line => {
    if (line.startsWith('seeds:')) {
        const seeds_ranges = line.match(/(\d+)/g)?.map(it => parseInt(it))
        seeds = []
        for(let i = 0; i < seeds_ranges.length; i+=2) {
            seeds.push([seeds_ranges[i], seeds_ranges[i]+seeds_ranges[i+1]])
        }
    }
    
        switch (step) {
            case 'seeds_to_soil':
                populate_range_by_line(seeds, line, NUMBER, SOIL)
                break;
            case 'soil_to_fertilizer':
                populate_range_by_line(seeds, line, SOIL, FERTILIZER)
                break;
            case 'fertilizer_to_water':
                populate_range_by_line(seeds, line, FERTILIZER, WATER)
                break;
            case 'water_to_ligth':
                populate_range_by_line(seeds, line, WATER, LIGHT)
                break;
            case 'light_to_temperature':
                populate_range_by_line(seeds, line, LIGHT, TEMP)
                break;
            case 'temperature_to_humidity':
                populate_range_by_line(seeds, line, TEMP, HUMIDITY)
                break;
            case 'humidity_to_location':
                populate_range_by_line(seeds, line, HUMIDITY, LOCATION)
                break;
        } 

        switch (line) {
            case "seed-to-soil map:":
                step = 'seeds_to_soil'
                break;
                
            case "soil-to-fertilizer map:":
                step = 'soil_to_fertilizer'
                break;
           case "fertilizer-to-water map:":
                step = 'fertilizer_to_water'
                break;
            case "water-to-light map:":
                step = 'water_to_ligth'
                break;
            case "light-to-temperature map:":
                step = 'light_to_temperature'
                break;
            case "temperature-to-humidity map:":
                step = 'temperature_to_humidity'
                break;
            case "humidity-to-location map:":
                step = 'humidity_to_location'
                break;
                
        } 
})



const part2 = seeds.reduce((min, curr) => {
    console.log(curr)
    for(let i = curr[0]; i <= curr[1]; i++) {
        const val = mappers[SOIL].map(i)
        if(val <= min) {
            console.log('New min', val)
            min = val
        }
    }
    return min
}, Infinity)
console.log('Part 2', part2)
