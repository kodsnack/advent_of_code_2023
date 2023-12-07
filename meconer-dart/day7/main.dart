import '../util/util.dart';

// const String inputFile = 'day7/example.txt';
const String inputFile = 'day7/input.txt';

Future<void> main(List<String> args) async {
  var input = await readInputAsString(inputFile);

  test();
  print('Part 1:');
  final resultP1 = calcResultP1(input);
  print(resultP1);

  // print('Part 2:');
  // final resultP2 = calcResultP2(input);
  // print(resultP2);
}

void test() {
  Hand hand1 = Hand.fromString('33332 1');
  Hand hand2 = Hand.fromString('2AAAA 1');
  assert(hand1.compare(hand2) == 1);
  hand1 = Hand.fromString('77888 1');
  hand2 = Hand.fromString('77788 1');
  assert(hand1.compare(hand2) == 1);
}

int calcResultP1(String input) {
  List<Hand> hands = [];
  for (final line in input.split('\n')) {
    hands.add(Hand.fromString(line));
  }

  hands.sort((a, b) => a.compare(b));

  int result = 0;

  for (int idx = 0; idx < hands.length; idx++) {
    result += (idx + 1) * hands[idx].bid;
  }
  return result;
}

class Hand {
  static const List<String> cardOrder = [
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'T',
    'J',
    'Q',
    'K',
    'A',
  ];

  List<String> cards = [];
  late int bid;
  Hand.fromString(String s) {
    cards = s.split(' ')[0].split('');
    bid = int.parse(s.split(' ')[1]);
  }

  static int compareCard(String a, String b) {
    int idxa = cardOrder.indexWhere((element) => element == a);
    int idxb = cardOrder.indexWhere((element) => element == b);
    return idxa.compareTo(idxb);
  }

  int compare(Hand other) {
    final thisHandType = getHandType(cards);
    final otherHandType = getHandType(other.cards);

    final cmp = thisHandType.rank.compareTo(otherHandType.rank);
    if (cmp == 0) {
      // Same rank. Then we compare the cards from start
      for (int idx = 0; idx < cards.length; idx++) {
        final cmp2 = compareCard(cards[idx], other.cards[idx]);
        if (cmp2 != 0) return cmp2;
      }
      return 0;
    }
    return cmp;
  }

  HandType getHandType(List<String> cards) {
    Map<String, int> cardCount = {};
    for (final card in cards) {
      cardCount[card] = cardCount.containsKey(card) ? cardCount[card]! + 1 : 1;
    }
    List<int> cardCountList = cardCount.values.toList();
    cardCountList.sort();

    switch (cardCountList) {
      case [5]:
        return HandType.fiveOfAKind;
      case [1, 4]:
        return HandType.fourOfAKind;
      case [2, 3]:
        return HandType.fullHouse;
      case [1, 1, 3]:
        return HandType.threeOfAKind;
      case [1, 2, 2]:
        return HandType.twoPair;
      case [1, 1, 1, 2]:
        return HandType.onePair;
      default:
        return HandType.highCard;
    }
  }
}

enum HandType {
  highCard(1),
  onePair(2),
  twoPair(3),
  threeOfAKind(4),
  fullHouse(5),
  fourOfAKind(6),
  fiveOfAKind(7);

  const HandType(this.rank);

  final int rank;
}
