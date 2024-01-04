class Graph {
  int vertices;
  late List<List<Edge>> adjacencyList;

  Graph(this.vertices) {
    adjacencyList = List.generate(vertices, (index) => []);
  }

  void addEdge(int u, int v, int weight) {
    adjacencyList[u].add(Edge(v, weight));
    adjacencyList[v].add(Edge(u, weight)); // For undirected graph
  }
}

class Edge {
  int destination, weight;

  Edge(this.destination, this.weight);
}

class LongestPathResult {
  List<int> path;
  int length;

  LongestPathResult(this.path, this.length);
}

class LongestPathFinder {
  Graph graph;
  int start, end;
  List<bool> visited;
  LongestPathResult result;

  LongestPathFinder(Graph graph, int start, int end)
      : graph = graph,
        start = start,
        end = end,
        visited = List.filled(graph.vertices, false),
        result = LongestPathResult([], 0);

  LongestPathResult findLongestPath() {
    List<int> currentPath = [start];
    backtrack(start, currentPath, 0);

    return result;
  }

  void backtrack(int current, List<int> currentPath, int currentLength) {
    visited[current] = true;

    if (current == end) {
      if (currentLength > result.length) {
        result.length = currentLength;
        result.path = List.from(currentPath);
      }
    } else {
      for (Edge edge in graph.adjacencyList[current]) {
        if (!visited[edge.destination]) {
          currentPath.add(edge.destination);
          backtrack(edge.destination, currentPath, currentLength + edge.weight);
          currentPath.removeLast();
        }
      }
    }

    visited[current] = false;
  }
}

void main() {
  Graph graph = Graph(6);

  // Example graph with weighted edges
  graph.addEdge(0, 1, 2);
  graph.addEdge(0, 2, 3);
  graph.addEdge(1, 3, 5);
  graph.addEdge(1, 4, 1);
  graph.addEdge(2, 4, 2);
  graph.addEdge(3, 5, 4);
  graph.addEdge(4, 5, 3);

  int startNode = 0;
  int endNode = 5;

  LongestPathFinder longestPathFinder =
      LongestPathFinder(graph, startNode, endNode);
  LongestPathResult result = longestPathFinder.findLongestPath();

  print("Longest path between $startNode and $endNode:");
  print("Path: ${result.path}");
  print("Length: ${result.length}");
}
