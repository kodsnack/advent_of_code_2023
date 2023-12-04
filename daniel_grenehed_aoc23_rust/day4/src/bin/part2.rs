fn part2(input :String) -> i32 {
    let mut sum :i32= 0;
    let lines :Vec<&str> = input.lines().collect();
    let mut mult :Vec<usize>= vec![1; lines.len()];
    for i in 0..lines.len() {
        let s1 :Vec<_>= lines[i].split(':').collect();
        if s1.len() < 2 {
            continue;
        }
        let s2 :Vec<_>= s1[1].split('|').collect();
        if s2.len() < 2 {
            continue;
        }
        let mut winning_numbers :Vec<i32> = Vec::new();
        for ss in s2[0].split(' ') {
            match ss.parse::<i32>() {
                Ok(n) => {winning_numbers.push(n);},
                Err(_e) => {}
            }
        }
        let mut points :usize= 0;
        for ss in s2[1].split(' ') {
            match ss.parse::<i32>() {
                Ok(n) => {
                    if winning_numbers.contains(&n) {
                        points += 1;
                    }
                },
                Err(_e) => {}
            }
        }
        sum += mult[i] as i32;
        for c in i+1..i+points+1 {
            mult[c] += mult[i];
        }
    }
    sum
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
        let input = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11".to_string();
        let output = part2(input);
        assert_eq!(output, 30);
    }
}
