
fn part1(input :&str) -> i32 {
    input.lines().map(|line| {
        let mut vects :Vec<Vec<i32>> = Vec::new();
        vects.push(line.split(' ').map(|n| n.parse::<i32>()).flatten().collect());
        let mut i = 0;
        // create tables
        while vects.last().unwrap().iter().any(|n| *n != 0) {
            vects.push(vects[i].windows(2).map(|v| v[1]-v[0]).collect::<Vec<i32>>());
            i += 1;
        }
        // predict value
        vects.iter().map(|v| v[v.len()-1]).fold(0, |a,v| a + v) 
    }).fold(0, |a,n| a+n)
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
        let input = "0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45";
        let output = part1(input);
        assert_eq!(output, 114);
    }
    #[test]
    fn test_neg() {
        let input = "3 2 1 0 -1 -2 -3";
        let output = part1(input);
        assert_eq!(output, -4);
    }
}
