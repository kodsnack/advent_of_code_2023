namespace aoc2023
{
    internal class Day4
    {
        public static void A()
        {
            var input = Utils.GetData(4);

            var sum = 0;

            foreach (var row in input)
            {
                var numbersRow = row.Split(": ")[1];

                var matchedNumbers = 0;

                var numberColumns = numbersRow.Split("|");
                var firstColumn = numberColumns[0].Split(' ', StringSplitOptions.RemoveEmptyEntries);
                var secondColumn = numberColumns[1].Split(' ', StringSplitOptions.RemoveEmptyEntries);

                foreach(var number in secondColumn)
                {
                    if(firstColumn.Contains(number)) matchedNumbers++;
                }
                
                if(matchedNumbers == 1) sum++;
                if (matchedNumbers == 2) sum += 2;
                if (matchedNumbers > 2) sum += int.Parse(Math.Pow(2, matchedNumbers - 1).ToString());
            }

            Console.WriteLine(sum);
        }

        public static void B()
        {
            var input = Utils.GetData(4);

            var copies = new List<int>();
            copies.AddRange(Enumerable.Range(1, input.Count()));

            foreach (var row in input)
            {
                var rowNumber = input.IndexOf(row) + 1;
                
                var loops = copies.Where(x => x == rowNumber).Count();

                var numbersRow = row.Split(": ")[1];

                var matchedNumbers = 0;

                var numberColumns = numbersRow.Split("|").ToList();
                var firstColumn = numberColumns[0].Split(' ', StringSplitOptions.RemoveEmptyEntries);
                var secondColumn = numberColumns[1].Split(' ', StringSplitOptions.RemoveEmptyEntries);

                for(int i = 0; i < loops; i++)
                {
                    foreach (var number in secondColumn)
                    {
                        if (firstColumn.Contains(number)) matchedNumbers++;
                    }
                    var range = Enumerable.Range(rowNumber + 1, matchedNumbers);
                    copies.AddRange(range);
                    matchedNumbers = 0;
                }
            }

            Console.WriteLine(copies.Count());
        }
    }
}
