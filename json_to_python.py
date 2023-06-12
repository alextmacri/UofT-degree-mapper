"""This file makes a dict object containing all the scraped nodes in the json files.
It also makes a list of names of the programs for the dropdown menu.
"""
import json

all_nodes = {}
program_names = []

with open('scrapy/testcrawler/courses.json', 'r', errors='ignore') as courses_file:
    courses = json.load(courses_file)

    for course in courses:
        course['name'] = course['name'][:8]         # making the name just the course code
        course['or_'] = []
        course['type'] = 'course'
        all_nodes[course['name']] = course

with open('scrapy/testcrawler/programs.json', 'r', errors='ignore') as programs_file:
    programs = json.load(programs_file)

    for program in programs:
        program['name'] = program['name'][-9:]      # making the name just the program code
        program['or_'] = []
        program['type'] = 'program'
        all_nodes[program['name']] = program

        program_names.append(program['name'])
