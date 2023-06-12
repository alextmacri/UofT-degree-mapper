"""This is a file for the university class."""
from __future__ import annotations
# from typing import Optional
from node import Node
from sample_data1z4 import sample_data_dict
from json_to_python import all_nodes, program_names


class University:
    """The university class.
    Instance Attribute:
    - departments: a dictionary of departments in the faculty of arts and science at the university of Toronto,
            with the department name as the key and the department object as the associated value
    - nodes_dict: a dictionary storing all courses and programs in that university.
    - edges: a list of tuples that contain all the connections between course/program nodes.
    """
    nodes_dict: dict[str, Node]
    edges: list[tuple]

    def __init__(self) -> None:
        self.nodes_dict = {}
        self.edges = []

    def breadth_str_to_num(self, breadth: str) -> int:
        """Turns the breadth requirement string into a number. Functions primarily as a
        helper function for translate data.

        The breadth is in one of these strings:
        {'Creative and Cultural Representations (1)', 'Thought, Belief and Behaviour (2)',
        'Society and its Institutions (3)', 'Living Things and Their Environment (4)',
        'The Physical and Mathematical Universes (5)'}

        This function takes the second last character of the input string and returns it as a node.
        """
        if isinstance(breadth, str) and len(breadth) > 2:
            breadth_number = int(breadth[-2])
        else:
            breadth_number = 0

            # try:
            #     breadth_number = int(breadth_number)
            # except ValueError:
            #     breadth_number = None
        return breadth_number

    # Get a credit value from the course code of a program
    def get_num_credits(self, course_name: str) -> float:
        """Return a number of credits for a course, based on the course code.
        A standard course name is of the format 'AAA111H0 - the name of the course'
        The first 3 characters are letters, the next 3 are numbers, the next character is Y or H and the next character
        is 0 or 1.

        If the course code contains a Y based on the artsci course code format, the returned credit is 1.00.
        If the course code contains a H based on the artsci format or doesn't satisfy the standard formatting
        conditions, the returned credit is 0.5"""
        # check if the course code is a standard Y course
        if len(course_name) >= 8:
            course_code = course_name[0:8]
            # check if the last char matches, and it is a Y course.
            if course_code[-2] == 'Y' and course_code[-1] in {'0', '1'}:
                # check the typing of the first 6 chars
                if (course_code[0:3].isalpha() and course_code[0:3].isupper()) and course_code[3:6].isdigit():
                    return 1.00
        # H course or non-standard case - return 0.50
        return 0.50

    # Turn Alex's output format for the data into the version that works for the translate_data function
    # note: this only currently works for courses
    def scrapy_to_valid_input(self, data: dict) -> dict:
        """This function takes in input as the dictionary of data returned after the scraping process, and turns it into
         a format which can be used as a valid input for the translate_data function.
        Note: in the returned output, postrequisits is always refers to an empty list

        The input format for this function:
        {
        name:
            {'type': 'course', 'breadth': 1,
            'prerequisites': ['ABC123','XYZ224'], 'exclusions': ['XXX111']}
        }

        The output format for this function:
        {
        name:
            {'type': 'course', 'breadth': 1, 'credits': 0.5,
            'prerequisits': ['ABC123','XYZ224'], 'postrequisites': [],
            'OR': [], 'exclusions': ['XXX111']}
        }

        """
        new_data = {}
        for course in data:
            credits_ = self.get_num_credits(course)
            new_dict = {'postrequisites': [], 'OR': [], 'credits': credits_}
            new_data[course] = new_dict | data[course]
            # putting data last insures that if both dicts share a same (which shouldn't happen),
            # it goes with the value from data[course]
        return new_data

    def get_code(self, name: str, type_: str) -> str:
        """Takes 2 strings, name and type, as input. Depending on the type (course or program) returns a course or
        program code. Here the returned course code is of the format 'ABC123' - note that this function doesn't return
        the final two letters of the course code format (ex. H1)
        This is the first 6 characters of the name
        The returned program code is of the format 'ASSPE1995' - This is the last 9 characters of name
        If the node does not have a valid type ('program' or 'course') it returns name as is

        Prerequisites:
        - type in {'program', 'course'}
        - name is a valid name depending on the type
        """
        if type_ == 'course':
            code = name[:8]
        elif type_ == 'program':
            code = name[-9:]
        else:
            code = name
        return code

    def translate_data(self, data: dict) -> None:
        """Takes the data supplied by scrapy and adapts it into Course/Program nodes.
        This function is in its infancy and will most likely change depending on how
        the dictionary is formed, but I thought a skeleton will work.

        >>> g = University()
        >>> g.translate_data(sample_data_dict)
        >>> g.nodes_dict['AST120'].breadth == 3
        True
        >>> 'AST120' in g.nodes_dict['MAG400'].prerequisites
        True
        >>> 'MAG400' in g.nodes_dict['AST120'].or_
        True
        >>> 'PHY131' in g.nodes_dict['AST120'].or_['MAG400']
        True
        >>> g2 = University()
        >>> g2.translate_data(all_nodes)
        """
        self.scrapy_to_valid_input(data)

        for node in data:
            new_c = Node(name=node, type_=data[node]['type'])
            if new_c.type_ == 'course':
                new_c.breadth = self.breadth_str_to_num(data[node]['breadth'])
                new_c.credits_ = self.get_num_credits(node)
                new_c.exclusions = data[node]['exclusions']
            self.nodes_dict[node] = new_c

        for node in data:
            new_c = self.nodes_dict[node]
            for i, prereqs in enumerate(data[node]['prerequisites']):
                prereq_list_for_curr_node = data[node]['prerequisites']
                if prereqs in self.nodes_dict:
                    new_c.prerequisites[prereqs] = self.nodes_dict[prereqs]
                elif prereqs == '/':
                    if data[node]['prerequisites'][i - 1] in self.nodes_dict and \
                            data[node]['prerequisites'][i + 1] in self.nodes_dict:
                        if node in self.nodes_dict[data[node]['prerequisites'][i - 1]].or_:
                            self.nodes_dict[prereq_list_for_curr_node[i - 1]].or_[node].append(
                                self.nodes_dict[prereq_list_for_curr_node[i + 1]].name)
                        else:
                            self.nodes_dict[prereq_list_for_curr_node[i - 1]].or_[node] = [
                                self.nodes_dict[prereq_list_for_curr_node[i + 1]].name]

                        if node in self.nodes_dict[data[node]['prerequisites'][i + 1]].or_:
                            self.nodes_dict[prereq_list_for_curr_node[i + 1]].or_[node].append(
                                self.nodes_dict[prereq_list_for_curr_node[i - 1]].name)
                        else:
                            self.nodes_dict[prereq_list_for_curr_node[i + 1]].or_[node] = [
                                self.nodes_dict[prereq_list_for_curr_node[i - 1]].name]

    def edges_to_tuple(self, node: str, connected: set) -> list[tuple[Node, Node]]:
        """Creates the edges between nodes that is then visualized by the creation of the
        graph.

        Preconditions:
        - program in self.nodes_dict
        >>> g = University()
        >>> g.translate_data(sample_data_dict)
        >>> g.edges_to_tuple('MAGIC 1111H')[1][0]
        'MAG400'
        >>> g.edges_to_tuple('MAGIC 1111H')[1][1]
        'AST120'
        """
        for prereq in self.nodes_dict[node].prerequisites:
            if prereq not in connected:
                connected.add(prereq)
                self.edges.append((self.nodes_dict[node], self.nodes_dict[prereq]))
            if prereq not in self.nodes_dict[prereq].prerequisites:
                self.edges_to_tuple(prereq, connected)
        return self.edges


UNI = University()
UNI.translate_data(all_nodes)


def get_program_edges(program: str) -> list[tuple[Node, Node]]:
    """A second version of edges_to_tuple that will be used for the GUI functions
    related to player input."""
    return UNI.edges_to_tuple(program, set())


def get_program_nodes(program: str) -> set:
    """Create a set of node names for a program."""
    _nodes = set()
    for edge in get_program_edges(program):
        _nodes.add(edge[0])
        _nodes.add(edge[1])
    return _nodes


# if __name__ == '__main__':
#     # When you are ready to check your work with python_ta, uncomment the following lines.
#     # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
#     # You can use "Run file in Python Console" to run PythonTA,
#     # and then also test your methods manually in the console.
#     import python_ta
#     python_ta.check_all(config={
#         'max-line-length': 120,
#         'extra-imports': ['node', 'json_to_python']
#     })
