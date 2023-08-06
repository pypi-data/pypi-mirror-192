# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['regexparser']
setup_kwargs = {
    'name': 'regexparser',
    'version': '0.1.0',
    'description': 'Simple parser for small text chunks',
    'long_description': "## textparser\n\nFrequently I have to parse text into `float`, `int` and `date`, for a few examples.\nThe `TextParser` class to isolates the parsing task, instead of getting the parsing rules (or functions) spread all over the code.\n\n### Install\n\n`pip` install from github:\n\n\tpip install git+https://github.com/wilsonfreitas/textparser.git\n\n### Using\n\nCreate a class inheriting `TextParser` and write methods with names starting with `parse`.\nThese methods must accept 2 more arguments after `self` and those arguments are the `text` that will be parsed and the `MatchObject` that is returned by applying the regular expression to the `text`.\nThe `parse*` methods are called only if its regular expression is matched and their regular expressions are set in the methods' doc string.\n\n`textparser` provides a compact way of applying transformation rules and that rules don't have to be spread out along the code.\n\nThe following code shows how to create text parsing rules for a tew text chunks in portuguese.\n\n```python\nclass PortugueseRulesParser(TextParser):\n    # transform Sim and Não into boolean True and False, ignoring case\n    def parseBoolean_ptBR(self, text, match):\n        r'^(sim|Sim|SIM|n.o|N.o|N.O)$'\n        return text[0].lower() == 's'\n    # transform Verdadeiro and Falso into boolean True and False, ignoring case\n    def parseBoolean_ptBR2(self, text, match):\n        r'^(verdadeiro|VERDADEIRO|falso|FALSO|V|F|v|f)$'\n        return text[0].lower() == 'v'\n    # parses a decimal number\n    def parse_number_decimal_ptBR(self, text, match):\n        r'^-?\\s*\\d+,\\d+?$'\n        text = text.replace(',', '.')\n        return eval(text)\n    # parses number with thousands\n    def parse_number_with_thousands_ptBR(self, text, match):\n        r'^-?\\s*(\\d+\\.)+\\d+,\\d+?$'\n        text = text.replace('.', '')\n        text = text.replace(',', '.')\n        return eval(text)\n\nparser = PortugueseRulesParser()\n\nassert parser.parse('1,1') == 1.1\nassert parser.parse('-1,1') == -1.1\nassert parser.parse('- 1,1') == -1.1\nassert parser.parse('WÃ¡lson') == 'WÃ¡lson'\nassert parser.parse('1.100,01') == 1100.01\n```\n\nI copied the idea of using a regular expression in `__doc__` from [PLY](http://www.dabeaz.com/ply/).\n\n\n",
    'author': 'wilsonfreitas',
    'author_email': 'wilson.freitas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
