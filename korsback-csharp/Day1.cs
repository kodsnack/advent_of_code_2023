namespace aoc2023 
{
    public class Day1
    {
        public static void A()
        {
            var input = Utils.GetData(1);
            int sum = 0;

            foreach (var item in input)
            {
                var numbers = item.ToCharArray().Where(x => char.IsNumber(x));
                var number1 = numbers.First().ToString();
                var number2 = numbers.Last().ToString();
                sum += int.Parse(number1 + number2);
            }

            Console.WriteLine(sum);
        }

        public static void B()
        {
            var textRepresentations = new List<KeyValuePair<string, int>>()
            {
                new ("one", 1),
                new ("two", 2),
                new ("three", 3),
                new ("four", 4),
                new ("five", 5),
                new ("six", 6),
                new ("seven", 7),
                new ("eight", 8),
                new ("nine", 9),
            };

            var input = Utils.GetData(1);
            int sum = 0;

            foreach (var inputString in input)
            {
                var foundNumbers = new List<KeyValuePair<int, int>>();

                textRepresentations.ForEach(x => {

                    foundNumbers.Add(new(inputString.IndexOf(x.Key), x.Value));
                    foundNumbers.Add(new(inputString.IndexOf(x.Value.ToString()), x.Value));

                    foundNumbers.Add(new(inputString.LastIndexOf(x.Key), x.Value));
                    foundNumbers.Add(new(inputString.LastIndexOf(x.Value.ToString()), x.Value));
                });

                foundNumbers = [.. foundNumbers.Where(x => x.Key >= 0).Distinct().OrderBy(x => x.Key)];
                
                var number1 = foundNumbers.First().Value.ToString();
                var number2 = foundNumbers.Last().Value.ToString();
                sum += int.Parse(number1 + number2);
            }

            Console.WriteLine(sum);
        }
    }
}