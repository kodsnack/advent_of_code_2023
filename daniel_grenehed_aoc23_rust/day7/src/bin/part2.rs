use std::str::FromStr;
use std::cmp::Ordering;
use std::fmt;

const CARDS: &[char] = &['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'];

#[derive(PartialEq)]
enum HandTypes {
    FiveOfAKind,
    FourOfAKind,
    FullHouse,
    ThreeOfAKind,
    TwoPair,
    OnePair,
    HighCard
}

#[derive(PartialEq)]
struct HandType {
    hand_type : HandTypes
}

#[derive(Debug, PartialEq, Eq)]
struct ParseHandTypeError;

impl FromStr for HandType {
    type Err = ParseHandTypeError;
    fn from_str(s :&str) -> Result<Self, Self::Err> {
        let mut map = std::collections::HashMap::new();
        for c in s.trim().chars() {
            map.entry(c).and_modify(|i| *i+=1).or_insert(1);
        }
        
        let j :i32 = match map.get(&'J') { Some(v) => *v, None => 0};
        if j == 5 {
            return Ok(Self{hand_type:HandTypes::FiveOfAKind});
        }
        map.remove(&'J');
        
        let mut vec = map.values().cloned().collect::<Vec<_>>();
        
        let iom = vec.iter().enumerate().max_by(|(_, a),(_, b)| a.cmp(b)).map(|(index, _)| index);
        match iom {
            Some(i) => {vec[i]+=j;},
            None => {}
        }

        match vec.len() {
            1 => {return Ok(Self{hand_type:HandTypes::FiveOfAKind});},
            2 => {return if vec.contains(&1) {Ok(Self{hand_type:HandTypes::FourOfAKind})} else {Ok(Self{hand_type:HandTypes::FullHouse})};},
            3 => {return if vec.contains(&3) {Ok(Self{hand_type:HandTypes::ThreeOfAKind})} else {Ok(Self{hand_type:HandTypes::TwoPair})};},
            4 => {return Ok(Self{hand_type:HandTypes::OnePair});},
            5 => {return Ok(Self{hand_type:HandTypes::HighCard});},
            _ => {
                println!("HandType fail({}), vec.len() = {}", s, vec.len());
                return Err(ParseHandTypeError);}
        }
    }
}

impl std::fmt::Display for HandType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self.hand_type {
             HandTypes::FiveOfAKind => write!(f,"FiveOfAKind"),
            HandTypes::FourOfAKind => write!(f,"FourOfAKind"),
            HandTypes::FullHouse => write!(f,"FullHouse"),
            HandTypes::ThreeOfAKind => write!(f,"ThreeOfAKind"),
            HandTypes::TwoPair => write!(f,"TwoPair"),
            HandTypes::OnePair => write!(f,"OnePair"),
            HandTypes::HighCard => write!(f,"HighCard")

        }
    }
}

impl HandType {
    fn to_number(&self) -> i32 {
        match self.hand_type {
            HandTypes::FiveOfAKind => {return 0;},
            HandTypes::FourOfAKind => {return 1;},
            HandTypes::FullHouse => {return 2;},
            HandTypes::ThreeOfAKind => {return 3;},
            HandTypes::TwoPair => {return 4;},
            HandTypes::OnePair => {return 5;},
            HandTypes::HighCard => {return 6;}
        }
    }
}

struct Play {
    hand : Vec<char>,
    hand_type : HandType,
    bid : i32,
}

#[derive(Debug, PartialEq, Eq)]
struct ParsePlayError;

impl FromStr for Play {
    type Err = ParsePlayError;
    fn from_str(s :&str) -> Result<Self, Self::Err> {
        let split = s.trim().split(' ').collect::<Vec<_>>();
        if split.len() != 2 {
            return Err(ParsePlayError);
        }
        return Ok(Self{
            hand:       split[0].trim().chars().collect::<Vec<_>>(), 
            hand_type:  split[0].parse().unwrap(), 
            bid:        split[1].parse().unwrap()
        });
    }
}

impl std::fmt::Display for Play {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Play('{}', bid:{}, type:{})", self.hand.clone().into_iter().collect::<String>(), self.bid, self.hand_type)
    }
}

impl Play {
    fn compare(&self, p :&Play) -> Ordering {
        if self.hand_type.hand_type == p.hand_type.hand_type {
            for i in 0..self.hand.len() {
                if self.hand[i] != p.hand[i] {
                    for c in CARDS {
                        if p.hand[i] == *c {
                            return Ordering::Greater;
                        }
                        if self.hand[i] == *c {
                            return Ordering::Less;
                        }
                    }
                }
            }
            
        }
        if self.hand_type.to_number() < p.hand_type.to_number() {
            return Ordering::Less;
        }
        Ordering::Equal
    }
}

fn part2(input :String) -> i64 {
    let mut plays :Vec<Play> = input.lines().map(|s| match s.parse::<Play>() {Ok(p) => Some(p), Err(_e) => None} ).flatten().collect();
    plays.sort_by(|a, b| a.compare(b));
    let mut i = 0;
    let mut sum :i64 = 0;
    for play in plays.into_iter().rev() {
        i += 1;
        sum += (play.bid as i64) * i;
    }
    sum
}

fn main() {
    let input = include_str!("./input.txt").to_string();
    let output = part2(input);
    println!("{}", output);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let input = "32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483".to_string();
        let output = part2(input);
        assert_eq!(output, 5905);
    }
}
