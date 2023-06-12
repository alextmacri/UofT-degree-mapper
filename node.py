"""This is a file for the course class."""
from __future__ import annotations
from typing import Optional
# CourseCollection = dict | list | set


class Node:
    """The Node class represents a program or a course in the University of Toronto, Faculty of Arts and Science.
    Relationship attributes are the attributes which contain connections to other Nodes.

    Instance Attributes:
    - name: name of the course or program
    - prerequisites: a dictionary of all the prerequisites where the key is the course name.
    - exclusions: a dictionary of all exclusions for the course, where the key is the course name
    - breadth: an integer between 1 to 5 representing the breadth requirement.
            If no breadth requirement exists, it is 0.
    - credits_: a float representing the how many credits the course is worth.
    - or_: a dict of corequisites with the key being the course name.
    - type_: labels it as either a 'course' or 'program'

    Representation Invariants:
    - self.type == 'program' or self.type == 'course'
    - if self.type == 'program', then self.breadth is None
    - TODO: ADD MORE
    """
    name: str
    type_: str
    breadth: Optional[int]
    credits_: Optional[float]
    prerequisites: dict[str, Node]  # Relationship Attribute
    exclusions: Optional[dict[str, Node]]  # Relationship Attribute
    or_: Optional[dict[str, list[Node]]]  # Relationship Attribute

    def __init__(self, name: str, type_: str = 'course', breadth: Optional[int] = None,
                 credits_: Optional[float] = None) -> None:
        """Initialize a new course or program.
        Precondition:
        - type == 'program' or type == 'course'
        """
        self.name = name
        self.type_ = type_
        if type_ == 'program':       # prerequisites are represented as the courses without any postrequites.
            self.prerequisites = {}
        elif type_ == 'course':
            self.prerequisites = {}
            self.exclusions = {}
            self.breadth = breadth
            self.credits_ = credits_
            self.or_ = {}  # For the 157-137 dilemma.
        else:
            raise ValueError

    def is_program(self) -> bool:
        """Return whether the given object is a course or a program."""
        # depending on how we define a program, this function may come in useful
        # especially if we decide to remove the type attribute
        if self.type_ == 'program':
            return True
        else:
            return False

    def check_connections(self, course: Node, query: Optional[Node], search: str) -> bool | dict | str:
        """Takes in one or two courses and returns either their connections, or if they are
        connected to another course.

        A connection here is defined as a postrequisite, a prerequisite, or an exclusion."""
        if search in 'or':
            s = course.or_
        elif search in 'prerequisites':
            s = course.prerequisites
        elif search in 'exclusions':
            s = course.exclusions
        else:
            return 'Search query not found.'

        if query in locals():
            return query in s
        else:
            return s


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
