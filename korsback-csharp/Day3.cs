using System.Text.RegularExpressions;

namespace aoc2023
{
    internal class Day3
    {
        public static void A()
        {
            int sum = 0;
            var input = Utils.GetData(3);

            var mappedSymbols = new HashSet<Tuple<int, int>>(); //index, row

            for (int i = 0; i < input.Count; i++)
            {
                Regex.Matches(input[i], "[^a-z.0-9]+").ToList().ForEach(match =>
                    mappedSymbols.Add(Tuple.Create(i, match.Index))
                );
            }

            for (int i = 0;i < input.Count; i++)
            {
                var matchedNumbers = Regex.Matches(input[i], "\\d+").ToList();

                foreach (var number in matchedNumbers)
                {
                    var range = Enumerable.Range(
                        number.Index > 0 ? number.Index - 1 : 0, 
                        number.Index > 0 ? number.Length + 2 : number.Length + 1);

                    var adjacent = mappedSymbols.Any(x =>
                    {
                        return range.Contains(x.Item2) &&
                        (
                            x.Item1 == i ||
                            x.Item1 - 1 == i ||
                            x.Item1 + 1 == i
                        );
                    });

                    if (adjacent) sum += int.Parse(number.Value);
                }
            }

            Console.WriteLine(sum);
        }

        public static void B()
        {
            int sum = 0;
            var input = Utils.GetData(3);

            var mappedSymbols = new HashSet<Tuple<int, int, Guid>>(); //index, row, symbol-id
            var numbersToSum = new HashSet<Tuple<int, Guid>>(); //value, symbol-id 

            for (int i = 0; i < input.Count; i++)
            {
                Regex.Matches(input[i], "[*]").ToList().ForEach(match =>
                    mappedSymbols.Add(Tuple.Create(i, match.Index, Guid.NewGuid()))
                );
            }

            for (int i = 0; i < input.Count; i++)
            {
                var numbers = Regex.Matches(input[i], "\\d+").ToList();

                foreach (var number in numbers)
                {
                    var range = Enumerable.Range(
                        number.Index > 0 ? number.Index - 1 : 0,
                        number.Index > 0 ? number.Length + 2 : number.Length + 1);

                    foreach (var symbol in mappedSymbols)
                    {
                        var adjacent = range.Contains(symbol.Item2) && (
                                                            symbol.Item1 == i ||
                                                            symbol.Item1 - 1 == i ||
                                                            symbol.Item1 + 1 == i);

                        if (adjacent)
                        {
                            var tuple = Tuple.Create(int.Parse(number.Value), symbol.Item3);
                            numbersToSum.Add(tuple);
                        }
                    }
                }
            }

            var symbolIds = numbersToSum.Select(x => x.Item2).Distinct();
            foreach(var id in symbolIds)
            {
                var values = numbersToSum.Where(pair => pair.Item2 == id).ToList();
                if (values.Count() == 2)
                {
                    sum += values[0].Item1 * values[1].Item1;
                }
            }

            Console.WriteLine(sum);
        }
    }
}
