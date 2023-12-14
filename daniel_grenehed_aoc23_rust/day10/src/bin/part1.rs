use std::fmt;

fn get_char(pos :(i32, i32), map :&Vec<Vec<char>>) -> Option<char> {
    let (x, y) = pos;
    if x < 0 || y < 0 || y as usize >= map.len() || x as usize >= map[y as usize].len() {
        return None;
    }
    Some(map[y as usize][x as usize])
}

#[derive(PartialEq, Clone, Copy)]
enum Dir {
    Left,
    Right,
    Up,
    Down
}

impl std::fmt::Display for Dir {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Dir::Left => write!(f,"(Left)"),
            Dir::Right => write!(f,"(Right)"),
            Dir::Up => write!(f,"(Up)"),
            Dir::Down => write!(f,"(Down)")
        }
    }
}

fn matching(dir :Dir) -> Dir {
    match dir {
        Dir::Left => Dir::Right,
        Dir::Right => Dir::Left,
        Dir::Up => Dir::Down,
        Dir::Down => Dir::Up
    }
}

fn get_dir(c :char, from :Dir) -> Option<Dir> {
    let vec :Vec<Dir>;
    match c {
        '|' => {vec = vec![Dir::Up, Dir::Down];},
        '-' => {vec = vec![Dir::Left, Dir::Right];},
        'L' => {vec = vec![Dir::Up, Dir::Right];},
        'J' => {vec = vec![Dir::Up, Dir::Left];},
        'F' => {vec = vec![Dir::Down, Dir::Right];},
        '7' => {vec = vec![Dir::Left, Dir::Down];}
        _ => {vec = vec![];}
    }
    let m = matching(from);
    if vec.contains(&m) {
        for d in vec {
            if d != m {
                return Some(d);
            }
        }
    }
    None
}

fn next_pos(x :i32, y :i32, d :Dir) -> (i32, i32) {
    match d {
        Dir::Up => (x, y-1),
        Dir::Down => (x, y+1),
        Dir::Left => (x-1, y),
        Dir::Right => (x+1, y)
    }
}

fn path_continue(p :(i32, i32, Dir), map : &Vec<Vec<char>>) -> Option<(i32, i32, Dir)> { 
    let (x, y, d) = p;
    let (nx, ny) = next_pos(x, y, d);
    match get_char((nx, ny), map) {
        Some(c) => match get_dir(c, d) {
                Some(nd) => Some((nx, ny, nd)),
                None => None
            },
        None => None
    }
}


fn part1(input :&str) -> i64 {
    let map = input.lines().map(|line| line.chars().collect()).collect::<Vec<Vec<char>>>();
     
    let (sx, sy) = map
        .iter()
        .enumerate()
        .map(|(y,v)| 
            match v.iter().position(|c| *c == 'S') { Some(x) => Some((x,y)), None => None })
        .flatten()
        .fold( (0,0),|_a,e| e);
    assert_eq!(map[sy][sx], 'S');
    println!("({}, {})", sx, sy);

    let mut paths :Vec<(i32, i32, Dir)> = Vec::new();
    paths.push((sx as i32, sy as i32, Dir::Left));
    paths.push((sx as i32, sy as i32, Dir::Right));
    paths.push((sx as i32, sy as i32, Dir::Up));
    paths.push((sx as i32, sy as i32, Dir::Down));

    let mut step :i64= 0;
    while paths.len() > 0 {
        let mut rvec = Vec::new();
        for i in 0..paths.len() {
            match path_continue(paths[i], &map) {
                Some((x, y, d)) => {
                    if paths.iter().any(|&(ox, oy, _od)| ox == x && oy == y) {
                        return step + 1;
                    } 
                    paths[i] = (x, y, d);
                },
                None => {
                    rvec.insert(0, i);
                }
            }
        } 
        for r in rvec {
            paths.remove(r);
        }
        step += 1;
    }
    println!("paths empty!");
    0
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
        let input = "7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ";
        let output = part1(input);
        assert_eq!(output, 8);
    }
    #[test]
    fn test_example_2() {
        let input = "-L|F7
7S-7|
L|7||
-L-J|
L|-JF";
        let output = part1(input);
        assert_eq!(output, 4);
    }
}
