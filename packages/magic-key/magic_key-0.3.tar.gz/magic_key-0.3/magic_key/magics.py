# This code can be put in any Python module, it does not require IPython
# itself to be running already.  It only creates the magics subclass but
# doesn't instantiate it yet.
from __future__ import print_function

import IPython.core.magic
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
import ast      # AST is also magic, right?
from parsimonious.nodes import NodeVisitor      # And so are PEGs!
from parsimonious.grammar import Grammar


@magics_class
class NoMagic(Magics):
    """" This implementation uses exact string matching"""
    pass


@magics_class
class FalseMagic(Magics):
    """" This implementation uses whoosh search backend"""
    pass


@magics_class
class TrueMagic(Magics):
    """" This implementation uses AI backend"""

    @cell_magic
    def thread(self, line, cell):
        "This allows to create a temporary thread"
        # http://ipython.org/ipython-doc/dev/interactive/reference.html#embedding-ipython
        # https://gemfury.com/squarecapadmin/python:ipython/-/content/IPython/frontend/terminal/embed.py
        return line, cell


    @line_magic
    def prompt(self, line):
        "Identifies and executes the prompt for: @object prompt"
        #object, text = line[1:].split(maxsplit = 1)      # @object Prompt 
        # execute object.prompt(text) and return the result    
        return self.shell.ev(line)


    
    # print("Prompting. Full access to the main IPython object:", self.shell)
    # print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
    # return line


    @line_magic
    def hashtag(self, line):
        "tagging the object"
        object, text = line[1:].split(maxsplit = 1)      # #object Prompt 
        print("Prompting. Full access to the main IPython object:", self.shell)
        print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
        return line
    
    

    @line_magic
    def finetune(self, line):
        "execute python code"


    @line_magic
    def execute(self, line):
        "execute python code"
        print("Executing. Full access to the main IPython object:", self.shell)
        print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
        print("We'll run it!")
        return line


    @cell_magic
    def cmagic(self, line, cell):
        "my cell magic"
        return line, cell

    @line_cell_magic
    def execute(self, line, cell=None):
        "Magic that works both as %lcmagic and as %%lcmagic"
        if cell is None:
            print("Called as line magic")
            return line
        else:
            print("Called as cell magic")
            return line, cell



# define transformation 
# https://ipython.readthedocs.io/en/stable/config/inputtransforms.html


# Grammar to match code blocks

grammar = Grammar(
   r"""
    default_rule = (multi_line_code / inline_code / prompt / chat / hashtag)+
    
    multi_line_code = call "```" language? code "```"
    inline_code = call "`" code "`"
    language = ~r"[-\w]+" ws
    code = ~r"([^`]+)"
    
    prompt = call object ws text

    chat = ~r"([^`#@]+)"
 
    call = "@" search? magic? 
    
    hashtag = "#" search? magic? object
    
    magic = "*"
    search = "?"
    object = ~r"[0-9A-z_.]+"
    ws = ~r"\s+"i 

    text = ~r"([^`#@]+)"
    """
)

class Transformer(NodeVisitor):
    def __init__(self):
        self.code_lines = []
                
    def visit_magic(self, node, visited_children):
        self.code_lines.append('%magic')

    def visit_search(self, node, visited_children):
        self.code_lines.append('%search')
    
    def visit_code(self, node, visited_children):
        # ast.parse(node.text.split("\n"))
        self.code_lines.extend(node.text.split("\n"))    
    
    def visit_prompt(self, node, visited_children):
        call,object,ws,text = visited_children
        line = '%prompt' + object.text + '.__prompt__(ur"""' + text.text + '""")'
        self.code_lines.append(line)

    def visit_chat(self, node, visited_children):
        text = node.text.strip()
        if text:
            self.code_lines.append('%chat ur"""' + node.text + '""")')

    def visit_hashtag(self, node, visited_children):
        self.code_lines.append('%hashtag ' + node.text)   
        
    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return visited_children or node


def transform_to_python(lines):
    """
        This transforms lines from @```python.code()``` to python.code()
        and from @object Prompt to %prompt object.__prompt__("Prompt").
        This also processes #hastag tags, replacing it with %memory
    """

    tree = grammar.parse("\n".join(lines))
    visitor = Transformer()
    visitor.visit(tree)
    return visitor.code_lines


# In order to actually use these magics, you must register them with a
# running IPython.
def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    # You can register the class itself without instantiating it.  IPython will
    # call the default constructor on it.
    ipython.register_magics(TrueMagic)
    ipython.input_transformers_cleanup.append(transform_to_python)

