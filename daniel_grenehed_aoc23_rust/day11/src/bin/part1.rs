
fn part1(input :&str) -> i64 {
    let mut map = input.lines().map(|l| l.chars().collect()).collect::<Vec<Vec<char>>>();
    
    // for each emty line, create 
    let mut horizontal_append :Vec<(usize, Vec<char>)> = Vec::new();
    for (i, v) in map.iter().enumerate() {
        if !v.iter().any(|c| *c == '#') {
            horizontal_append.insert(0, (i, v.to_vec()));
        }
    }
    for (i, v) in &horizontal_append {
        map.insert(*i, v.to_vec());
    }
    
    /*
    println!("added {} lines", horizontal_append.len());
    for v in &map {
        println!("{}", v.iter().collect::<String>());
    }*/

    let mut vertical_append :Vec<usize> = Vec::new();
    for i in 0..map[0].len() {
        if !map.iter().any(|v| v[i] == '#') {
            vertical_append.insert(0, i);
        }
    }

    for i in &vertical_append {
        for v in &mut map {
            v.insert(*i, '.');
        }
    }
    /*
    println!("added {} lines", vertical_append.len());
    for v in &map {
        println!("{}", v.iter().collect::<String>());
    }*/

    let stars = map.iter()
        .enumerate()
        .map(|(y, v)| v.iter()
            .enumerate()
            .map(|(x,c)| match c {'#' => Some((x, y)), _ => None })
            .flatten()
            .collect::<Vec<(usize, usize)>>())
        .fold(vec![],|mut av, mut nv| { av.append(&mut nv); av } );

    
    let mut sum :i64 = 0; 
    for i in 0..stars.len() {
        for j in i+1..stars.len() {
            let (x1, y1) = stars[i];
            let (x2, y2) = stars[j];
            sum += (x2 as i64 - x1 as i64).abs() + (y2 as i64 - y1 as i64).abs();
        }
    }
    sum
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
    fn test_example() {
        let input = "...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....";
        let output = part1(input);
        assert_eq!(output, 374);
    }
}
