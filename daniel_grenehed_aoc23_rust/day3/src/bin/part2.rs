
fn get_number(line :String, start :usize) -> Option<i32> {
    let mut begin = start;
    let mut end = start+1;
    for i in end..line.len()+1 {
        match line[begin..i].parse::<i32>() {
            Ok(_n) => {end = i;},
            Err(_e) => {
                break;
            }
        }
    }
    for i in (0..begin).rev() {
        match line[i..end].parse::<i32>() {
            Ok(_n) => {begin = i;},
            Err(_e) => {
                break;
            }
        }
    }
    match line[begin..end].parse::<i32>() {
        Ok(n) => {
            return Some(n.abs());
        },
        Err(_e) => {return None;}
    }
}

fn part2(input :String) -> i32 {
    let mut sum = 0;
    let mut map :Vec<Vec<char>>= Vec::new();   
    let lines :Vec<_>= input.lines().collect();
    for line in input.lines() {
        map.push(line.chars().collect());
    }
    for y in 0..map.len() {
        for x in 0..map[y].len() {
            if map[y][x] == '*' {
                // symbol, add adjecent to sum
                let s = sum;
                let mut numbers : Vec<i32> = Vec::new();
                if y > 0 { // check line above
                    let line = lines[y-1].to_string();
                    match get_number(line.clone(), x) {
                        Some(n) => { numbers.push(n);},
                        None => { // check diagonals
                            if x > 0 {
                                match get_number(line.clone(), x-1) {
                                    Some(n) => { numbers.push(n);},
                                    None => {}
                                }
                            } 
                            if x < line.len() {
                                match get_number(line.clone(), x+1) {
                                    Some(n) => { numbers.push(n);},
                                    None => {}
                                }
                            }
                        }
                    }
                }
                
                // check current line
                if x > 0 {
                    match get_number(lines[y].to_string(), x-1) {
                        Some(n) => { numbers.push(n);},
                        None => {}
                    }
                }
                if x < lines[y].len() {
                    match get_number(lines[y].to_string(), x+1) {
                        Some(n) => { numbers.push(n);},
                        None => {}
                    }
                }

                if y < lines.len()-1 { // check line below 
                    let line = lines[y+1].to_string();
                    match get_number(line.clone(), x) {
                        Some(n) => { numbers.push(n);},
                        None => { // check diagonals
                            if x > 0 {
                                match get_number(line.clone(), x-1) {
                                    Some(n) => { numbers.push(n);},
                                    None => {}
                                }
                            }
                            if x < lines[y+1].len() {
                                match get_number(line.clone(), x+1) {
                                    Some(n) => { numbers.push(n);},
                                    None => {}
                                }
                            }
                        }
                    }
                }
                if numbers.len() == 2 {
                    sum += numbers[0]*numbers[1];
                }
            }
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
        let input = "467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..".to_string();
        let output = part2(input);
        assert_eq!(output, 467835);
    }
}
