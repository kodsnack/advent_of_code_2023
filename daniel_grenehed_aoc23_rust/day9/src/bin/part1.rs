
fn part1(input :&str) -> i32 {
    input.lines().map(|line| {
        let mut vects :Vec<Vec<i32>> = Vec::new();
        vects.push(line.split(' ').map(|n| n.parse::<i32>()).flatten().collect());
        let mut i = 0;
        // create tables
        while vects.last().unwrap().iter().fold(0, |a,n| a+n.abs()) != 0 {
            let mut vec :Vec<i32> = Vec::new();
            for n in 0..vects[i].len()-1 {
                vec.push(vects[i][n+1]-vects[i][n]);
            }
            vects.push(vec);
            i += 1;
        }
        i -= 1;
        // predict values
        while i > 0 {
            let vec_i_last = vects[i].len()-1;
            let vec_i1_last = vects[i+1].len()-1;
            let val = vects[i][vec_i_last] + vects[i+1][vec_i1_last];
            vects[i].push(val);
            i -= 1;
        } 
        let vec_0_last = vects[0].len()-1;
        let vec_1_last = vects[1].len()-1;
        vects[0][vec_0_last] + vects[1][vec_1_last]
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
