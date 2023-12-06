fn part2(input :String) -> i64 {
    let mut time :i64 = 0;
    let mut dist :i64 = 0;
    for line in input.lines() {
        let split :Vec<_>= line.split(':').collect();
        if split.len() > 1 {
            match split[0] {
                "Time" => {
                    let number = split[1].trim().split(' ').collect::<Vec<_>>().join("");

                    match number.parse::<i64>() {
                            Ok(n) => {time = n;},
                            Err(_e) => {}
                    }
                        
                },
                "Distance" => {
                    let number = split[1].trim().split(' ').collect::<Vec<_>>().join("");
                    match number.parse::<i64>() {
                        Ok(n) => {dist = n;},
                        Err(_e) => {}
                    } 
                },
                _ => {}
            }
        }
    }

    let mut sum = 1;
    for x in 0..time/2 {
        if (x * (time - x)) > dist {
            sum = time - ((x*2)-1);
            break;
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
        let input = "Time:      7  15   30
Distance:  9  40  200".to_string();
        let output = part2(input);
        assert_eq!(output,  71503);
    }
}
