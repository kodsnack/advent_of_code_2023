
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

fn part1(input :String) -> i32 {
    let mut sum = 0;
    let mut map :Vec<Vec<char>>= Vec::new();   
    let lines :Vec<_>= input.lines().collect();
    for line in input.lines() {
        map.push(line.chars().collect());
    }
    for y in 0..map.len() {
        for x in 0..map[y].len() {
            if map[y][x].is_digit(10) {
            } else if map[y][x] == '.' {
            } else {
                // symbol, add adjecent to sum
                let s = sum;
                if y > 0 { // check line above
                    let line = lines[y-1].to_string();
                    match get_number(line.clone(), x) {
                        Some(n) => { sum += n;},
                        None => { // check diagonals
                            if x > 0 {
                                match get_number(line.clone(), x-1) {
                                    Some(n) => { sum += n;},
                                    None => {}
                                }
                            } 
                            if x < line.len() {
                                match get_number(line.clone(), x+1) {
                                    Some(n) => { sum += n;},
                                    None => {}
                                }
                            }
                        }
                    }
                }
                
                // check current line
                if x > 0 {
                    match get_number(lines[y].to_string(), x-1) {
                        Some(n) => { sum += n;},
                        None => {}
                    }
                }
                if x < lines[y].len() {
                    match get_number(lines[y].to_string(), x+1) {
                        Some(n) => { sum += n;},
                        None => {}
                    }
                }

                if y < lines.len()-1 { // check line below 
                    let line = lines[y+1].to_string();
                    match get_number(line.clone(), x) {
                        Some(n) => { sum += n;},
                        None => { // check diagonals
                            if x > 0 {
                                match get_number(line.clone(), x-1) {
                                    Some(n) => { sum += n;},
                                    None => {}
                                }
                            }
                            if x < lines[y+1].len() {
                                match get_number(line.clone(), x+1) {
                                    Some(n) => { sum += n;},
                                    None => {}
                                }
                            }
                        }
                    }
                }
                if s != sum {
                        println!("added {} around {} line {}", sum - s, map[y][x], y);
                }
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
        let output = part1(input);
        assert_eq!(output, 4361);
    }

    #[test]
    fn test_right_edge() {
        let input = "467..114..
...*......
..35...633
.......#..
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..".to_string();
        let output = part1(input);
        assert_eq!(output, 4361);
    }

    #[test]
    fn test_diagonal() {
        let input = "1.2
.*.
3.4".to_string();
        let output = part1(input);
        assert_eq!(output, 10);
    }

    #[test]
    fn test_sanity() {
        let input = "1#.".to_string();
        let output = part1(input);
        assert_eq!(output, 1);
    }

    #[test]
    fn test_same_row() {
        let input = "1.2..
34*56
".to_string();
        let output = part1(input);
        assert_eq!(output, 92);
    }

    #[test]
    fn test_around() {
        let input = "123
1#3
1.3".to_string();
        let output = part1(input);
        assert_eq!(output, 131);
    }

    #[test]
    fn test_center() {
        let input = "12..
1#3.
.21.".to_string();
        let output = part1(input);
        assert_eq!(output, 37);
    }
    #[test]
    fn test_sides() {
        let input = "123*123".to_string();
        let output = part1(input);
        assert_eq!(output, 246);
    }
    #[test]
    fn test_single() {
        let input = ".*.\n.5.".to_string();
        let output = part1(input);
        assert_eq!(output, 5);
    }
    #[test]
    fn test_padded() {
        let input = ".1...\n.2*3..\n..4..".to_string();
        let output = part1(input);
        assert_eq!(output, 10);
    }
    #[test]
    fn test_negative() {
        let input = "-1.".to_string();
        let output = part1(input);
        assert_eq!(output, 1);
    }
}
