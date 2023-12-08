use std::str::FromStr;
use std::fmt;

#[derive(Clone, Copy)]
struct Range {
    start   :i64,
    length  :i64
}

#[derive(Debug, Clone, Copy)]
struct RangeMap {
    destination: i64,
    source: i64,
    length: i64
}

#[derive(Debug, PartialEq, Eq)]
struct ParseRangeError;
 
impl FromStr for RangeMap {
    type Err = ParseRangeError;
    fn from_str(s :&str) -> Result<Self, Self::Err> {
        let mut nums :Vec<i64> = Vec::new();
        for num in s.trim().split(' ') {
            match num.parse::<i64>() {
                Ok(n) => {nums.push(n);},
                Err(_e) => {}
            }
        }
        if nums.len() < 3 {
            return Err(ParseRangeError);
        }
        return Ok(Self {destination:nums[0], source:nums[1], length:nums[2]});
    }
}

impl std::fmt::Display for RangeMap {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "RangeMap(dest: {}, src: {},  len: {})", self.destination, self.source, self.length)
    }
}

impl RangeMap {
    fn intersects(&self, r: Range) -> bool {
        if self.contains(r) {
            return true;
        }
        if r.last() >= self.source && r.last() <= self.last() {
            return true;
        } 
        if r.start <= self.source && r.last() >= self.last() {
            return true;
        }
        if r.start >= self.source && r.start <= self.last() {
            return true;
        }
        return false;
    }
    fn contains(&self, r: Range) -> bool {
        if r.start >= self.source && r.last() <= self.last() {
            return true;
        }
        return false;
    }
    fn last(&self) -> i64 {
        return self.source + self.length -1;
    }
}

impl std::fmt::Display for Range {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Range(start: {}, length: {})", self.start, self.length)
    }
}

impl Range {
    fn contains(&self, rm: RangeMap) -> bool {
        if rm.source >= self.start && rm.source + rm.length <= self.start + self.length {
            return true;
        }
        return false;
    }
    fn last(&self) -> i64 {
        return self.start + self.length -1;
    }
}

fn map_seeds(seeds :&mut Vec<Range>, map :&Vec<RangeMap>) -> Vec<Range> {
    let mut out = Vec::new();

    for m in map {
        let mut i = 0;
        while i < seeds.len() {
            let mut removed = false;
            let r = seeds[i];
            if m.intersects(r) {
                seeds.remove(i);
                removed = true;
                if m.contains(r) {
                    // remap the whole range
                    let po = Range{start: (r.start - m.source) + m.destination, length: r.length};
                    out.push(po);
                } else if r.contains(*m) {
                    // remap for the whole RangeMap
                    let start_diff = m.source - r.start;
                    if start_diff > 0 {
                        let sds = Range {start:r.start, length:start_diff};
                        seeds.push(sds);
                    }
                    let end_diff = r.last() - m.last();
                    if end_diff > 0 {
                        let eds = Range {start:m.last()+1, length:end_diff};
                        seeds.push(eds);
                    }
                    let po = Range{start:m.destination, length: m.length};
                    out.push(po);
                    assert_eq!(start_diff + end_diff + m.length, r.length);
                } else {
                    if r.start < m.source { // range starts outside RangeMap then enters it
                        let start_diff = m.source - r.start;
                        let sds = Range {start:r.start, length:start_diff};
                        let po = Range {start:m.destination, length:r.length - start_diff};
                        seeds.push(sds);
                        out.push(po);
                    } else { // range starts in RangeMap but continues
                        let end_diff = r.last() - m.last();
                        let start_diff = r.start - m.source;
                        let eds = Range {start:m.last()+1, length:end_diff};
                        let po = Range {start:m.destination + start_diff, length:r.length - end_diff};
                        seeds.push(eds);
                        out.push(po);
                    }
                }

            } 
            if !removed {
                i+=1;
            }
        }
    }
    for r in seeds {
        out.push(r.clone());
    }
    out
}

fn part2(input :String) -> i64 {
    let lines :Vec<&str>= input.lines().collect();
    let mut seeds :Vec<Range>= Vec::new();

    let mut start = true;
    let mut r_start = 0;
    // get seeds
    for seed in lines[0].split(' ') {
        match seed.parse::<i64>() {
            Ok(n) => {
                if start {
                   r_start = n;
                   start = false;
                } else {
                    seeds.push(Range {start:r_start, length:n});
                    start = true;
                }
            },
            Err(_e) => {}
        }
    }

    let mut map :Vec<RangeMap> = Vec::new();
    for i in 1..lines.len() {
        if lines[i].contains(':') {
            seeds = map_seeds(&mut seeds, &map);
            map = Vec::new();
        } else {
            match lines[i].parse::<RangeMap>() {
                Ok(r) => {map.push(r);},
                Err(_e) => {}
            } 
        }
    }
    seeds = map_seeds(&mut seeds, &map);
    
    let mut smallest :i64 = seeds[0].start;
    for seed in seeds {
        if seed.start < smallest {
            smallest = seed.start;
        }
    }
    smallest
}

fn main() {
    let input = include_str!("./part1.txt");
    let output = part2(input.to_string());
    println!("{}", output);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let input = "seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4".to_string();
        let output = part2(input);
        assert_eq!(output, 46);
    }
}
