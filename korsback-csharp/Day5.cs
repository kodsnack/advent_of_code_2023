namespace aoc2023
{
    internal class Day5
    {
        public static void A()
        {
            var input = Utils.GetData(5).Where(x => x != "").ToList();
            var originItems = input.First().Split(' ', StringSplitOptions.RemoveEmptyEntries).Skip(1);

            var maps = GetMaps(input);

            var valuesToMatch = originItems.Select(long.Parse).ToList();

            foreach (var map in maps)
            {
                var sourceRranges = new List<Tuple<long, long, int>>(); 
                var destinationRanges = new List<Tuple<long, long>>();

                int rowNumber = 0;
                foreach (var row in map)
                {
                    var sourceRange = Tuple.Create(row.Item2, row.Item2 + row.Item3-1, rowNumber);
                    var destinationRange = Tuple.Create(row.Item1, row.Item1 + row.Item3-1);

                    sourceRranges.Add(sourceRange);
                    destinationRanges.Add(destinationRange);

                    rowNumber++;
                }

                var newValuesToMatch = new List<long>();
                var matchedValues = new List<long>();

                foreach (var value in valuesToMatch)
                {
                    foreach (var sourceRange in sourceRranges)
                    {
                        var currentDestinationRange = destinationRanges[sourceRange.Item3];
                        if (value >= sourceRange.Item1 && value <= sourceRange.Item2)
                        {
                            var diff = sourceRange.Item1 - currentDestinationRange.Item1;
                            newValuesToMatch.Add(value - diff);
                            matchedValues.Add(value);    
                        }
                    }
                }
                var missingValues = valuesToMatch.Where(x => !matchedValues.Contains(x));
                newValuesToMatch.AddRange(missingValues);
                valuesToMatch = new List<long>(newValuesToMatch);
            }

            var result = valuesToMatch.OrderBy(x => x).First();

            Console.WriteLine(result);

        }

        private static List<Tuple<long, long, long>> CreateMap(IEnumerable<string> inputRows)
        {
            return inputRows.Select(x =>
            {
                var split = x.Split(' ', StringSplitOptions.RemoveEmptyEntries);
                return Tuple.Create(long.Parse(split[0]), long.Parse(split[1]), long.Parse(split[2]));
            }).ToList();
        }

        private static List<List<Tuple<long, long, long>>> GetMaps(List<string> input)
        {
            var soilFertilizerIndex = input.FindIndex(x => x.Contains("soil-to"));
            var fertilizerWaterIndex = input.FindIndex(x => x.Contains("fertilizer-to"));
            var waterToLightIndex = input.FindIndex(x => x.Contains("water-to"));
            var lightToTempIndex = input.FindIndex(x => x.Contains("light-to"));
            var tempToHumidIndex = input.FindIndex(x => x.Contains("temperature-to"));
            var humidToLocationIndex = input.FindIndex(x => x.Contains("humidity-to-"));

            var seedSoilMap = CreateMap(input.GetRange(2, soilFertilizerIndex - 2));
            var soilFertMap = CreateMap(input.GetRange(soilFertilizerIndex + 1, fertilizerWaterIndex - soilFertilizerIndex - 1));
            var fertWaterMap = CreateMap(input.GetRange(fertilizerWaterIndex + 1, waterToLightIndex - fertilizerWaterIndex - 1));
            var waterLightMap = CreateMap(input.GetRange(waterToLightIndex + 1, lightToTempIndex - waterToLightIndex - 1));
            var lightTempMap = CreateMap(input.GetRange(lightToTempIndex + 1, tempToHumidIndex - lightToTempIndex - 1));
            var tempHumidMap = CreateMap(input.GetRange(tempToHumidIndex + 1, humidToLocationIndex - tempToHumidIndex - 1));
            var humidLocationMap = CreateMap(input.GetRange(humidToLocationIndex + 1, input.Count - 1 - humidToLocationIndex));

            var maps = new List<List<Tuple<long, long, long>>>
            {
                seedSoilMap,
                soilFertMap,
                fertWaterMap,
                waterLightMap,
                lightTempMap,
                tempHumidMap,
                humidLocationMap
            };
            return maps;
        }

    }
}
