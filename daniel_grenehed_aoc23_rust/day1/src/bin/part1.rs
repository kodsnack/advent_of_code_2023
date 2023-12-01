fn is_digit(c :char) -> bool {
    if c >= '0' && c <= '9' {
        return true;
    }
    false
}

fn part1(input :String) -> i32 {
    let mut sum :i32 = 0;
    for line in input.lines() {
        let l = line.chars().count(); 
        let mut a :i32 = -1;
        let mut b :i32 = -1;

        for i in 0..l {
            if a == -1 && is_digit(line.chars().nth(i).unwrap()) {
                a = line.chars().nth(i).unwrap().to_digit(10).unwrap() as i32;
            }
            if b == -1 && is_digit(line.chars().nth(l-(i+1)).unwrap()) {
                b = line.chars().nth(l-(i+1)).unwrap().to_digit(10).unwrap() as i32;
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
    println!("{}", part1(input.to_string()));
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let input = "1abc2
            pqr3stu8vwx
            a1b2c3d4e5f
            treb7uchet".to_string();
        let output: i32 = part1(input);
        println!("{}", output);
        assert_eq!(output, 142);
    }
}
