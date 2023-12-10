use std::collections::HashMap;

fn euclid(i1 :i64, i2 :i64) -> i64 { // gcd / lcm
    let mut a = i1;
    let mut b = i2;
    while a != b {
        if a > b {
            a -= b;
        } else {
            b -= a;
        }
    }
    a
}

fn part1(input :&str) -> i64 {
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

    let nodes = lines[2..].iter()
        .map(|line| {
            let s :Vec<_>= line.split(' ').collect();
            if s.len() < 1 {
                return None;
            }
            if s[0].ends_with("A") {
                return Some(s[0].to_string());
            }
            return None;
        })
        .flatten()
        .collect::<Vec<_>>(); 

    let mut total_steps :i64 = 1;
    for node in nodes {
        let mut n :&str= &node;
        let mut steps = 0;
        while !n.ends_with("Z") {
            n = &map[n][turns[(steps as usize) % turns.len()]];
            steps += 1;
        }
        total_steps *= steps / euclid(total_steps, steps);
    }
    total_steps
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
    fn test_example() {
        let input = "LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)";
        let output = part1(input);
        assert_eq!(output, 6);
    }
}
