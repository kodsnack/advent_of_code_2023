namespace aoc2023;

public class Utils
{
    public static List<string> GetData(int day, string delimiter = "\r\n")
    {
        var fileData = System.IO.File.ReadAllText($"day{day}.txt");
        var data = fileData.Split(delimiter).ToList();

        return data;
    }
}