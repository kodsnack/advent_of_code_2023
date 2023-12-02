use std::fmt;

enum Color {
    Red,
    Green,
    Blue
}
struct Set {
    count: i32,
    color: Color
}

struct Game {
    number: i32,
    sets: Vec<Set>
}
impl fmt::Display for Game {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut out : String = "Game ".to_owned();
        out.push_str(&self.number.to_string());
        out.push_str(":");
        for set in &self.sets {
            out.push_str(" ");
            out.push_str(&set.count.to_string());
            out.push_str(" ");
            match set.color {
                Color::Red => {out.push_str("red");},
                Color::Green => {out.push_str("green");},
                Color::Blue => {out.push_str("blue");}
            }
            out.push_str(",");
        }
        write!(f, "{}", out)
    }
}

fn create_game(line :String) -> Option<Game> {
    let mut game :Game;
    let s1 = line.split(':').collect::<Vec<&str>>();
    let s2 = s1[0].split(' ').collect::<Vec<&str>>();
    match s2[1].parse() {
        Ok(n) => {game = Game{number:n, sets:Vec::new()}},
        Err(_e) => {
            println!("Failed to parse game number (s2 length: {})", s2.len());
            return None; 
        } 
    }
    for set in s1[1].split(';').collect::<Vec<&str>>() {
        for pair in set.split(',').collect::<Vec<&str>>() {
            let cv = pair.trim().split(' ').collect::<Vec<&str>>();
            match cv[0].parse() {
                Ok(n) => {
                    let c :Color;
                    match cv[1] {
                        "red" => {c = Color::Red;},
                        "green" => {c = Color::Green;},
                        "blue" => {c = Color::Blue;},
                        &_ => {
                            println!("Failed to parse color from '{}'", cv[1]);
                            return None;
                        }
                    }
                    game.sets.push(Set{count:n, color:c});
                },
                Err(_e) => {
                    println!("Failed to parse cubes (cv length: {})", cv.len());
                    let mut i = 0;
                    for part in cv {
                        println!("cv[{}]: {}", i, part);
                        i+=1;
                    }
                    return None;
                }
            }
        }
    }
    return Some(game);
}

fn part1(input :String) -> i32 {
    let mut sum :i32= 0;
    for line in input.lines() {
        match create_game(line.to_string()) {
            Some(game) => {
                let mut include_game = true;
                for set in game.sets {
                    match set.color {
                        Color::Red => {
                            if set.count > 12 {
                                include_game = false;
                                break;
                            }
                        },
                        Color::Green => {
                            if set.count > 13 {
                                include_game = false;
                                break;
                            }
                        },
                        Color::Blue => {
                            if set.count > 14 {
                                include_game = false;
                                break;
                            }
                        }
                    }
                }
                if include_game {
                    sum += game.number;
                }
            },
            None => {
                println!("falied to create game from '{}'", line);
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
        let input :String = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green".to_string();
        let output = part1(input);
        println!("{}", output);
        assert_eq!(output, 8);
    }
}
