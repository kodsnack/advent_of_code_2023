const fs = require('fs');
const { isUndefined } = require('util');

const data = fs.readFileSync(process.argv[2], 'utf8').trim();

function compareCards(a, b, i) {
  if (a.hand[i] === b.hand[i]) return compareCards(a, b, i + 1);
  return a.hand[i] - b.hand[i];
}

function compareHands(a, b) {
  if (a.value > b.value) return 1;
  else if (b.value > a.value) return -1;
  else return compareCards(a, b, 0);
}

function parse_part1(line) {
  let [hand, bet] = line.trim().split(' ');
  const mapped_hand = hand.split('').map((it) => {
    switch (it) {
      case 'A':
        return 14;
      case 'K':
        return 13;
      case 'Q':
        return 12;
      case 'J':
        return 11;
      case 'T':
        return 10;
      default:
        return parseInt(it);
    }
  });
  hand = mapped_hand.reduce((a, c) => {
    if (!a[c]) {
      a[c] = 0;
    }
    a[c] += 1;
    return a;
  }, {});

  hand = Object.entries(hand).sort(([k1, v1], [k2, v2]) => {
    if (v1 == v2) {
      return k2 - k1;
    }
    return v2 - v1;
  });
  const value = hand.reduce((a, [k, c]) => {
    if (a == 0 && c == 2) return 1;
    else if (a == 1 && c == 2) return 2;
    else if (a == 0 && c == 3) return 3;
    else if (a == 3 && c == 2) return 4;
    else if (a == 0 && c == 4) return 5;
    else if (a == 0 && c == 5) return 6;
    return a;
  }, 0);

  return { hand: mapped_hand, bet: parseInt(bet), value: value };
}

function parse_part2(line) {
  let [hand, bet] = line.trim().split(' ');
  const mapped_hand = hand.split('').map((it) => {
    switch (it) {
      case 'A':
        return 14;
      case 'K':
        return 13;
      case 'Q':
        return 12;
      case 'J':
        return 1;
      case 'T':
        return 10;
      default:
        return parseInt(it);
    }
  });
  hand = mapped_hand.reduce((a, c) => {
    if (!a[c]) {
      a[c] = 0;
    }
    a[c] += 1;
    return a;
  }, {});
  const jokers = hand['1'] ? hand['1'] : 0;

  hand = Object.entries(hand).sort(([k1, v1], [k2, v2]) => {
    if (v1 == v2) {
      return k2 - k1;
    }
    return v2 - v1;
  });
  const value = hand.reduce((a, [k, c]) => {
    if (k === '1' && c != 5) return a;
    else if (k === '1' && c === 5) return 6;
    if (a == 0 && c + jokers == 2) return 1;
    else if (a == 1 && c == 2) return 2;
    else if (a == 0 && c + jokers == 3) return 3;
    else if (a == 3 && c == 2) return 4;
    else if (a == 0 && c + jokers == 4) return 5;
    else if (a == 0 && c + jokers == 5) return 6;
    return a;
  }, 0);

  if(line === 'JJJJJ') console.log(mapped_hand, bet, value)
  return { hand: mapped_hand, bet: parseInt(bet), value: value };
}
const part1 = data
  .split('\n')
  .map(parse_part1)
  .sort(compareHands)
  .map((hand, i) => hand.bet * (i + 1))
  .reduce((a, c) => a + c);

console.log('Part 1', part1);

const part2 = data
  .split('\n')
  .map(parse_part2)
  .sort(compareHands)
  .map((hand, i) => hand.bet * (i + 1))
  .reduce((a, c) => a + c);

console.log('Part 2', part2);
