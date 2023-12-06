use std::str::FromStr;

#[derive(Debug)]
struct Range {
    destination: i64,
    source: i64,
    length: i64
}

#[derive(Debug, PartialEq, Eq)]
struct ParseRangeError;

impl FromStr for Range {
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

impl Range {
    fn map(&self, n :i64) -> Option<i64> {
        if n >= self.source && n < (self.source + self.length) {
            return Some((n-self.source)+self.destination);
        }
        None
    }
}

fn map_seeds(seeds :&Vec<i64>, map :&Vec<Range>) -> Vec<i64> {
    let mut out :Vec<i64> = Vec::new();
    for s in 0..seeds.len() {
        let mut mapped = false;
        for r in map {
            
            match r.map(seeds[s]) {
                Some(n) => {
                    mapped = true;
                    out.push(n);
                    break;
                },
                None => {} 
            }
        }
        if !mapped {
            out.push(seeds[s]);
        }
    }
    out
}


fn part1(input :String) -> i64 {
   
    let lines :Vec<_>= input.lines().collect();
    let mut seeds :Vec<i64> = Vec::new();
    // get seeds
    for seed in lines[0].split(' ') {
        match seed.parse::<i64>() {
            Ok(n) => {
                seeds.push(n);
            },
            Err(_e) => {}
        }
    }
    let mut map :Vec<Range> = Vec::new();
    for i in 1..lines.len() {
        if lines[i].contains(':') {
            seeds = map_seeds(&seeds, &map);
            map = Vec::new();
        } else {
            match lines[i].parse::<Range>() {
                Ok(r) => {map.push(r);},
                Err(_e) => {}
            } 
        }
    }
    seeds = map_seeds(&seeds, &map);
    let mut smallest :i64= seeds[0].clone();
    for seed in seeds {
        if seed < smallest {
            smallest = seed;
        }
    }
    smallest
}

fn main() {
    let input = include_str!("./part1.txt");
    let output = part1(input.to_string());
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
        let output = part1(input);
        assert_eq!(output, 35);
    }
}
