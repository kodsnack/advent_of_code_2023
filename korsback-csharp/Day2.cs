namespace aoc2023
{
    internal class Day2
    {

        public static void A()
        {
            var input = Utils.GetData(2);
            int sum = 0;

            var colorLimits = new Dictionary<string, int>() { { "blue", 14 }, { "red", 12 }, { "green", 13 } };

            foreach (var game in input)
            {
                var gameSplit = game.Split(':');

                var id = int.Parse(gameSplit[0].Split(' ')[1]);

                var sets = gameSplit[1].Split(';');
                var invalidGameColors = new List<KeyValuePair<string, int>>();

                foreach (var set in sets)
                {
                    var colors = set.Split(',');
                    foreach (var color in colors)
                    {
                        var colorSplit = color.Split(' ');

                        var colorString = colorSplit[2];
                        var colorValue = int.Parse(colorSplit[1]);

                        if (colorValue > colorLimits[colorString])

                            invalidGameColors.Add(new KeyValuePair<string, int>(colorString, colorValue));
                    }
                }

                if (!invalidGameColors.Any()) sum += id;
            }

            Console.WriteLine(sum);
        }


        public static void B()
        {
            var input = Utils.GetData(2);
            int sum = 0;

            foreach (var game in input)
            {
                var gameSplit = game.Split(':');

                var id = int.Parse(gameSplit[0].Split(' ')[1]);

                var sets = gameSplit[1].Split(';');

                int maxRed = 0;
                int maxBlue = 0;
                int maxGreen = 0;

                foreach (var set in sets)
                {
                    var colors = set.Split(',');

                    foreach (var color in colors)
                    {
                        var colorSplit = color.Split(' ');

                        var colorString = colorSplit[2];
                        var colorValue = int.Parse(colorSplit[1]);

                        if(colorString == "red") maxRed = maxRed > colorValue ? maxRed : colorValue;
                        if(colorString == "green") maxGreen= maxGreen > colorValue ? maxGreen : colorValue;
                        if(colorString == "blue") maxBlue = maxBlue > colorValue ? maxBlue : colorValue;
                    }
                }

                sum += maxRed * maxGreen * maxBlue;

            }

            Console.WriteLine(sum);
        }

    }
}
