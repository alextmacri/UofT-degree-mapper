"""This is the main file that you run, which generates the gui"""
from __future__ import annotations
import random
from tkinter import *
import networkx as nx
import matplotlib.pyplot as plt
import university
from json_to_python import program_names
from node import Node
from university import UNI

options = ["---"]


def rand_color(r: int, g: int, b: int) -> tuple:
    """..."""
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)

    return (r / 255, g / 255, b / 255)


def create_edge_color_list(colors_used: list[tuple], list_of_edges: list[tuple[Node, Node]]) -> list[list]:
    """Creates a list containing a list of colors and a list of edges"""

    new_list_of_edges = []
    edge_color_list = []

    for edge in list_of_edges:
        node1 = edge[0]
        node2 = edge[1]
        if node2.type_ == "course" and node1.name in node2.or_.keys():
            list_of_or_nodes = list(set(node2.or_[node1.name]))
            list_of_node_pairs = [(node1.name, or_node) for or_node in list_of_or_nodes]
            color = rand_color(0, 0, 0)
            while color in colors_used:
                color = rand_color(0, 0, 0)
            list_colors = [color] * len(list_of_node_pairs)

            edge_color_list.extend(list_colors)
            new_list_of_edges.extend(list_of_node_pairs)
            edge_color_list.append(color)
            new_list_of_edges.append((node1.name, node2.name))

        elif node1.type_ == "course" and node2.name in node1.or_.keys():
            list_of_or_nodes = list(set(node1.or_[node2.name]))

            list_of_node_pairs = [(node2.name, or_node) for or_node in list_of_or_nodes]
            color = rand_color(0, 0, 0)
            while color in colors_used:
                color = rand_color(0, 0, 0)
            list_colors = [color] * len(list_of_node_pairs)
            edge_color_list.extend(list_colors)
            new_list_of_edges.extend(list_of_node_pairs)
            edge_color_list.append(color)
            new_list_of_edges.append((node1.name, node2.name))

        else:                                   # No Ors
            edge_color_list.append((0, 0, 0))
            new_list_of_edges.append((node1.name, node2.name))

    return [new_list_of_edges, edge_color_list]


class EnterProgramButton:
    """Button class for entering a program"""

    def __init__(self, master: Tk) -> None:
        """Initalize the enter program button"""

        clicked2 = StringVar()
        clicked2.set(program_names[0])

        drop2 = OptionMenu(master, clicked2, *program_names)
        drop2.grid(row=2, columnspan=1)

        self.enter_program = Button(master, text="Enter the Program", command=self.generate_graph, font=10)
        self.enter_program.grid(row=1, columnspan=1)

    def generate_graph(self) -> None:
        """Generate the graph, containing a program and its courses"""

        program_name = clicked2.get()

        if program_name in UNI.nodes_dict:
            new_options = []

            if UNI.nodes_dict[program_name].type_ == 'program':
                list_of_edges = university.get_program_edges(program_name)
                program_name_label = "PROGRAM: " + program_name
                graph = nx.MultiGraph()

                list_of_edges_by_name = []

                r = 0
                g = 0
                b = 0

                _nodes = set()
                for edge in list_of_edges:
                    list_of_edges_by_name.append((edge[0].name, edge[1].name))
                    _nodes.add(edge[0])
                    _nodes.add(edge[1])

                for nnode in _nodes:
                    new_options.append(nnode.name)

                edge_color_lists = create_edge_color_list([(r, g, b)], list_of_edges)
                edge_mapping = edge_color_lists[0]
                color_mapping = edge_color_lists[1]

                for edge2 in edge_color_lists[0]:
                    graph.add_edge(edge2[0], edge2[1], color=color_mapping[edge_mapping.index(edge2)], weight=2)

                program_label.config(text=program_name_label, font=10)
                program_label.grid(row=0, columnspan=1)
                clicked.set('---')
                drop['menu'].delete(0, 'end')

                for option in new_options:
                    drop['menu'].add_command(label=option, command=lambda x=option: clicked.set(x))

                colors = nx.get_edge_attributes(graph, "color").values()

                plt.clf()
                nx.draw(graph,
                        edge_color=colors,
                        with_labels=True,
                        width=2,
                        node_color='yellow')
                plt.show()

            else:
                program_label.config(text="Please Input a Valid Program", fg="red", font=10)
                program_label.grid(row=0, columnspan=1)
        else:
            program_label.config(text="Please Input a Valid Program", fg="red", font=10)
            program_label.grid(row=0, columnspan=1)


root = Tk()
root.wm_title("Program of Study Course Graph")
root.wm_protocol('WM_DELETE_WINDOW', root.quit)
root.geometry("10000x400")
root.rowconfigure(10)
root.columnconfigure(10)

program_label = Label(root, text="PROGRAM: ", font=10)
program_label.grid(row=0, columnspan=1)

buttons = EnterProgramButton(root)

clicked = StringVar()
clicked.set(options[0])

clicked2 = StringVar()
clicked2.set(program_names[0])

# drop2 = OptionMenu(root, clicked2, *program_names)
# drop2.pack()

drop = OptionMenu(root, clicked, *options)
drop.grid(row=2, column=2)

breadth_label = Label(root, text='', font=10)
breadth_label.grid(row=1, column=4)

credit_label = Label(root, text='', font=10)
credit_label.grid(row=2, column=4)

exclusions_label = Label(root, text='', font=10)
exclusions_label.grid(row=3, column=4)

web_label = Label(root, text='', font=10)
web_label.grid(row=2, column=4)

selected_label = Label(root, text='', font=10)
selected_label.grid(row=1, column=4)

instruction_label = Label(root, text="The node in the middle \n"
                                     " of the generated \n "
                                     "graph represents the \n "
                                     "Program of Study. \n"
                                     "The non-black edges \n "
                                     "represent courses that \n"
                                     " can be taken in place of \n "
                                     "the other with the matching \n"
                                     "edge color. ")

instruction_label.grid(row=3, column=0)


def selected() -> None:
    """Get the course/program that was selected from the dropdown, and updates the labels that contain the info
    about the course/program
    """
    breadth_label.grid(row=5, column=3)
    credit_label.grid(row=2, column=3)
    exclusions_label.grid(row=3, column=3)
    selected_label.grid(row=1, column=3)
    web_label.grid(row=2, column=3)

    course = clicked.get()

    if course != "---":
        selected_label.config(text=course, font=10)
        if course not in program_names:
            credit_text = 'CREDITS: ' + str(UNI.get_num_credits(course))
            credit_label.config(text=credit_text)
            breadth_text = "BREADTH REQUIREMENT: " + str(UNI.nodes_dict[course].breadth)
            breadth_label.config(text=breadth_text)
            exclusions_text = 'EXCLUSIONS: \n' + str(UNI.nodes_dict[course].exclusions)
            exclusions_label.config(text=exclusions_text)
            web_link = "COURSE SITE: \n https://artsci.calendar.utoronto.ca/course/" + course.lower()
            web_label.config(text=web_link)

        else:
            credit_label.config(text='')
            breadth_label.config(text='')
            exclusions_label.config(text='')

    else:
        selected_label.config(text="Please enter a program first", fg="red", font=10)


select_node = Button(root, text="Select a course or the program", command=selected, font=10)
select_node.grid(row=1, column=2)

root.mainloop()

# if __name__ == '__main__':
#     # When you are ready to check your work with python_ta, uncomment the following lines.
#     # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
#     # You can use "Run file in Python Console" to run PythonTA,
#     # and then also test your methods manually in the console.
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'extra-imports': ['node', 'json_to_python']
    # })
