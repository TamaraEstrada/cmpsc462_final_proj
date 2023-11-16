import networkx as nx
import matplotlib.pyplot as plt


class CourseGraph:
    def __init__(self, courses):
        self.graph = self.create_course_graph(courses)

    # create a graph representing the relationship between courses and their prerequisites using NetworkX
    def create_course_graph(self, courses):
        G = nx.Graph()
        # iterates over each course in the dictionary.
        # for each course it adds a node
        # the courses dict is expected to have course names as keys and their information as values
        # each key in the dict is a course name and the associated value is another dictionary containing information about that course (mainly trying to focus on the prerequisites)
        for course, info in courses.items():
            G.add_node(course)

            # iterates over prereq. list.
            # for each prereq it adds an edge from prereq to course and vise versa
            # treating it as a biodirectional relationship
            for prereq in info["prerequisites"]:
                # creates edge from the prereq. course to the current course, saying
                # 'to take this course, you shouldve complete all the following prereq.'
                G.add_edge(prereq, course)

                # this completes the biodirectional relationship(concurrent courses)
                # creates the edge in the opposite direction
                G.add_edge(course, prereq)
        print("REPRESENTATION OF NODES AND EDGES: ", G)
        return G

    def draw_graph(self):
        plt.figure(figsize=(12, 12))  # Increase figure size

        # Use spring_layout with an increased distance parameter 'k'
        pos = nx.spring_layout(self.graph, k=0.15, iterations=20)

        nx.draw(
            self.graph,
            pos,
            with_labels=True,
            node_color="lightblue",
            font_weight="bold",
            node_size=1400,  # Adjust node size
            font_size=8,  # Adjust font size
        )
        plt.show()

    # start: the starting node in the graph
    # end: the ending node in the graph
    # path: optional parameter that holds the current path being explored
    def get_paths(self, start, end, path=[]):
        # ensures that the method can work even if path is not provided when the method is called
        if path is None:
            path = []

        # Ensure that the graph contains the start and end nodes
        # indicates NO path can be found
        if start not in self.graph or end not in self.graph:
            return []

        # the current start node is added to the path, plays a role in the recursion progress
        path = path + [start]

        # base case for recursion
        # if the start == end then it means a complete path has been found. the path is returned in a list
        if start == end:
            return [path]

        # stores all paths that will be found
        paths = []
        # itertation over neighbors of the start node.
        # retrieves all the nodes that are directly connected to the start node
        # basically these are the nodes that can be reached from the start node by traversing one edge
        for node in self.graph.neighbors(start):
            # if the neighboor has not been visited yet, the method will recursivly #call itself with the neighbor as the NEW start node
            # finding all paths from this neighbot node to the end node AND considering the current path so far
            if node not in path:
                new_paths = self.get_paths(node, end, path)
                # returns a list of the paths found
                # each path is returned from the recursive call is to the paths list.
                for new_path in new_paths:
                    paths.append(new_path)
        return paths
