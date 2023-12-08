namespace aoc2023
{
    internal class Day6
    {

        public static void A()
        {
            var input = Utils.GetData(6);
            var races = input.Select(x => { return x.Split(':')[1].Split(' ', StringSplitOptions.RemoveEmptyEntries); });

            var sum = 1;
            var times = races.ToList()[0];
            var distances = races.ToList()[1];

            for (int i = 0; i < times.Count(); i++)
            {
                var time = times[i];
                var distanceToBeat = distances[i];

                var amountWaysToBeat = 0;

                for(int j = 1; j < int.Parse(time); j++) 
                {
                    var result = int.Parse(time) * j - int.Parse(Math.Pow(j, 2).ToString());

                    if (result > int.Parse(distanceToBeat)) { amountWaysToBeat++; }
                }

                sum*=amountWaysToBeat;
            }
                Console.WriteLine(sum);
        }

        public static void B()
        {
            var input = Utils.GetData(6);
            var races = input.Select(x => { return x.Split(':')[1].Split(' ', StringSplitOptions.RemoveEmptyEntries); });

            var sum = 1;
            var times = races.ToList()[0];
            var distances = races.ToList()[1];

            var time = long.Parse(string.Join("", times));
            var distanceToBeat = long.Parse(string.Join("", distances));

            var amountWaysToBeat = 0;

            for (int j = 1; j < time; j++)
            {
                var result = time * j - long.Parse(Math.Pow(j, 2).ToString());

                if (result > distanceToBeat) { amountWaysToBeat++; }
            }

            sum *= amountWaysToBeat;
            Console.WriteLine(sum);
        }
    }
}
