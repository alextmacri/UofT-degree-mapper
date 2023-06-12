"""Contains sample data for the university class."""

sample_data_dict = {
    'AST120':
        {'type': 'course', 'breadth': '3', 'credits': '0.5',
         'prerequisites': [], 'postrequisites': ['MAG400', 'PHY131'],
         'or_': {}, 'exclusions': ['AST121', 'AST122']},
    'PHY131':
        {'type': 'course', 'breadth': '5', 'credits': '0.5',
         'prerequisites': [], 'postrequisites': ['MAGIC 1111H'],
         'or_': {}, 'exclusions': ['MAG400']
         },
    'MAG400':
        {'type': 'course', 'breadth': '2', 'credits': '1.0',
         'prerequisites': ['AST120', '/', 'PHY131'], 'postrequisites': ['MAGIC 1111H'],
         'or_': {}, 'exclusions': ['PHY131']
         },
    'MAGIC 1111H':
        {'type': 'program', 'breadth': None, 'credits': None,
         'prerequisites': ['MAG400'], 'postrequisites': [],
         'or_': {}, 'exclusions': []
         }
}


"""Data Storage Method
    {
    'SHT122': {'name': 'SHT122H1 - something something', 'type': 'course', 'breadth': '1', 'credits': '0.5',
        'prerequisites': ['YUR691','MOM420'], 'or_': {'DAD122': ['FUK137']}, 'exclusions': []}
    }"""
