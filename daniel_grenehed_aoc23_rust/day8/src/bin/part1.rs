use std::collections::HashMap;

fn part1(input :&str) -> i32 {
    let lines = input.lines().collect::<Vec<_>>();
    let turns :Vec<_>= lines[0].chars()
        .map(|c| match c { 'L' => Some(0), 'R' => Some(1), _ => None})
        .flatten()
        .collect();

    let map = lines[2..].iter()
        .map(|line| {
            let bind = line.replace(&['(',')','=',','][..],"");
            let s = bind.split(' ').filter(|p| p.len() > 0).collect::<Vec<_>>();
            if s.len() < 3 { 
                None 
            } else { 
                Some((s[0].to_string(), vec![s[1].to_string(), s[2].to_string()])) 
            }
        })
        .flatten()
        .collect::<HashMap<_,_>>();

    let mut step :u32 = 0;
    let mut node :&str = "AAA"; 
    while node != "ZZZ" {
        node = &map[node][turns[(step as usize) % turns.len()]];
        step += 1;
    }
    step as i32
}

fn main() {
    let input = include_str!("./input.txt");
    let output = part1(input);
    println!("{}", output);
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_example_1() {
        let input = "RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)";
        let output = part1(input);
        assert_eq!(output, 2);
    }
    
    #[test]
    fn test_example_2() {
        let input = "LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)";
        let output = part1(input);
        assert_eq!(output, 6);
    }
}
