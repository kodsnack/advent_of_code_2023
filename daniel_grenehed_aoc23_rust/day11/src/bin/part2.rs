
fn part2(input :&str, expansion :usize) -> i64 {
    let map = input.lines().map(|l| l.chars().collect()).collect::<Vec<Vec<char>>>();
    
    // for each emty line, create 
    let horizontal_expansions :Vec<usize> = map.iter()
        .enumerate()
        .map(|(i,v)| 
            if !v.iter().any(|c| *c == '#') {Some(i)} 
            else {None})
        .flatten()
        .collect();
    
    let mut vertical_expansions :Vec<usize> = Vec::new();
    for i in 0..map[0].len() {
        if !map.iter().any(|v| v[i] == '#') {
            vertical_expansions.push(i);
        }
    }

    let mut stars = map.iter()
        .enumerate()
        .map(|(y, v)| v.iter()
            .enumerate()
            .map(|(x,c)| match c {'#' => Some((x, y)), _ => None })
            .flatten()
            .collect::<Vec<(usize, usize)>>())
        .fold(vec![],|mut av, mut nv| { av.append(&mut nv); av } );

    for i in 0..stars.len() {
        let (x, y) = stars[i];
        let mut ax = 0;
        let mut ay = 0;
        for he in &horizontal_expansions {
            if y > *he {
                ay += expansion-1;
            }
        }
        for ve in &vertical_expansions {
            if x > *ve {
                ax += expansion-1;
            }
        }
        stars[i] = (ax+x, ay+y);
    }
    

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
    let output = part2(input, 1000000);
    println!("{}", output);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example_1() {
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
        let output = part2(input, 10);
        assert_eq!(output, 1030);
    }

    #[test]
    fn test_example_2() {
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
        let output = part2(input, 100);
        assert_eq!(output, 8410);
    }
}
