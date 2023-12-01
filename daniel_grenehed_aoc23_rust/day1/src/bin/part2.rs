fn is_digit(c :char) -> bool {
    if c >= '0' && c <= '9' {
        return true;
    }
    false
}

const DIGITS :[&'static str; 9] = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine"
];

fn parse_digit(input :String) -> Option<i32> {
    for i in 0..DIGITS.len() {
        if input.contains(&DIGITS[i]) {
            return Some((i+1).try_into().unwrap());
        }
    }
    None
}

fn part2(input :String) -> i32 {
    let mut sum :i32 = 0;
    for line in input.lines() {
        let l = line.chars().count(); 
        let mut a :i32 = -1;
        let mut b :i32 = -1;

        for i in 0..l {
            if a == -1 {
                let left = parse_digit((&line[..i]).to_string());
                match left {
                    Some(n) => {a = n},
                    None => {
                        let nth = line.chars().nth(i).unwrap();
                        if is_digit(nth) {
                            a = nth.to_digit(10).unwrap() as i32;
                        }
                    }
                }
            }
            
            if b == -1 {
                let n = l-(i+1);
                let r_str = (&line[n..l]).to_string();
                let right = parse_digit(r_str.clone());
                match right {
                    Some(d) => {b = d},
                    None => {
                        let nth = line.chars().nth(n).unwrap();
                        if is_digit(nth) {
                            b = nth.to_digit(10).unwrap() as i32;
                        }
                    }
                }
                
            }
            if a != -1 && b != -1 {
                break;
            }
        }
        sum += a*10 + b;
    }
    sum
}

fn main() {
    let input = include_str!("./part1.txt");
    println!("{}", part2(input.to_string()));
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let input = "two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen".to_string();
        let output: i32 = part2(input);
        assert_eq!(output, 281);
    }
}
