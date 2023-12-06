fn part1(input :String) -> i32 {
    let mut time :Vec<i32> = Vec::new();
    let mut dist :Vec<i32> = Vec::new();
    for line in input.lines() {
        let split :Vec<_>= line.split(':').collect();
        if split.len() > 1 {
            match split[0] {
                "Time" => {
                    for numb in split[1].trim().split(' ') {
                        match numb.parse::<i32>() {
                            Ok(n) => {time.push(n);},
                            Err(_e) => {}
                        }
                    }    
                },
                "Distance" => {
                    for numb in split[1].trim().split(' ') {
                        match numb.parse::<i32>() {
                            Ok(n) => {dist.push(n);},
                            Err(_e) => {}
                        }
                    } 
                },
                _ => {}
            }
        }
    }
    println!("time {}, dist {}", time.len(), dist.len());

    let mut sum = 1;
    for i in 0..time.len() {
        for x in 1..(time[i] as i32)/2 {
            if (x * (time[i] - x)) > dist[i] {
                sum *= time[i] - ((x*2)-1);
                break;
            }
        }
    }
    sum
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
        let input = "Time:      7  15   30
Distance:  9  40  200".to_string();
        let output = part1(input);
        assert_eq!(output,  288);
    }
}
