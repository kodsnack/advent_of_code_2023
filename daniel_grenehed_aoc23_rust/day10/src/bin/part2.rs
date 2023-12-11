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

fn neighbors(p :(usize, usize), max_x :usize, max_y :usize) -> Vec<(usize, usize)> {
    let (x, y) = p;
    let mut out = Vec::new();
    if x > 0 {
        out.push((x-1, y));
    }
    if x < max_x {
        out.push((x+1, y));
    }
    if y > 0 {
        out.push((x, y-1));
    }
    if y < max_y {
        out.push((x, y+1));
    }
    out
}

fn part2(input :&str) -> i64 {
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

    let mut path_steps :Vec<Vec<Dir>> = Vec::new();
    let mut paths :Vec<(i32, i32, Dir)> = Vec::new();
    paths.push((sx as i32, sy as i32, Dir::Left));
    paths.push((sx as i32, sy as i32, Dir::Right));
    paths.push((sx as i32, sy as i32, Dir::Up));
    paths.push((sx as i32, sy as i32, Dir::Down));
    
    for p in &paths {
        let (_x,_y,d) = *p;
        path_steps.push(vec![d]);
    }

    let mut joined = false;
    while paths.len() > 0 {
        let mut rvec = Vec::new();
        for i in 0..paths.len() {
            match path_continue(paths[i], &map) {
                Some((x, y, d)) => {
                    path_steps[i].push(d);
                    if paths.iter().any(|&(ox, oy, _od)| ox == x && oy == y) {
                        joined = true;
                    } 
                    paths[i] = (x, y, d);
                },
                None => {
                    rvec.insert(0, i);
                }
            }
            if joined {
                break;
            }
        } 
        for r in rvec {
            paths.remove(r);
            path_steps.remove(r);
        }
        if joined {
            break;
        }
    }
    assert!(joined);
    let mut expanded_map :Vec<Vec<char>> = Vec::new();
    for v in &map {
        expanded_map.push(vec!['.'; v.len()*2]);
        expanded_map.push(vec!['.'; v.len()*2]);
    }
    
    // create expanded path
    let mut pos :Vec<(i32, i32)> = vec![(sx as i32, sy as i32); path_steps.len()];
    for i in 0..path_steps.len() {
        for j in 0..path_steps[i].len() {
            let d = path_steps[i][j];
            let (x, y) = pos[i];
            let mut ex :usize = x as usize * 2;
            let mut ey :usize = y as usize * 2;
            expanded_map[ey][ex] = '#';
            match d {
                Dir::Left => {
                    pos[i] = (x-1, y);
                    ex -= 1;
                },
                Dir::Right => {
                    pos[i] = (x+1, y);
                    ex += 1;
                },
                Dir::Up => {
                    pos[i] = (x, y-1);
                    ey -= 1;
                },
                Dir::Down => {
                    pos[i] = (x, y+1);
                    ey += 1;
                }
            }
            expanded_map[ey][ex] = '#';
        }
    }
    
    println!("Expanded:");
    for v in &expanded_map {
        println!("{}", v.iter().collect::<String>());
    }
    
    /*  
     *  starting at each point in border
     *  if position contains '#', then remove point from list
     *  else set position char to '#', remove point from list
     *  and add its neighbors to list 
     *
     * */
    let mut flood_vec :Vec<(usize, usize)> = Vec::new();
    for i in 0..expanded_map.len() {
        if i == 0 || i == expanded_map[i].len()-1 {
            for j in 0..expanded_map[i].len() {
                flood_vec.push((j, i));
            }    
        } else {
            flood_vec.push((0, i));
            flood_vec.push((expanded_map[i].len()-1, i));
        }
    }
    
    let max_y = expanded_map.len()-1;
    while flood_vec.len() > 0 {
        let (x, y) = flood_vec.pop().unwrap();
        let c = expanded_map[y][x];
        if c != '#' {
            expanded_map[y][x] = '#';
            let mut nb = neighbors((x, y), expanded_map[y].len()-1, max_y);
            flood_vec.append(&mut nb);
        } 
    }
    
    println!("\nFLOOOD!!!");
    for v in &expanded_map {
        println!("{}", v.iter().collect::<String>());
    }

    /*
     *
     *  Count 2x2 squares containing only '.'
     *
     * */ 

    let mut squares :i64 = 0;
    for y in 0..map.len() {
        for x in 0..map[y].len() {
            let ex = x*2;
            let ey = y*2;
            if expanded_map[ey][ex] != '.' || 
                expanded_map[ey+1][ex] != '.' || 
                expanded_map[ey][ex+1] != '.' ||
                expanded_map[ey+1][ex+1] != '.' { 
                continue;
            }
            squares += 1;
        }
    }

    squares
}

fn main() { 
    let input = include_str!("./input.txt"); 
    let output = part2(input); 
    println!("{}", output); 
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example_1() {
        let input = "...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........";
        let output = part2(input);
        assert_eq!(output, 4);
    }
    #[test]
    fn test_example_2() {
        let input = "..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........";
        let output = part2(input);
        assert_eq!(output, 4);
    }

    #[test]
    fn test_example_3() {
        let input = ".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...";
        let output = part2(input);
        assert_eq!(output, 8);
    }
    #[test]
    fn test_example_4() {
        let input = "FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L";
        let output = part2(input);
        assert_eq!(output, 10);
    }
}
