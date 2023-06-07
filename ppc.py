'''
Parsing Processing Code (PPC) - Parser for grouping Processing code into high level units that can be examined further to assess student work.
You are only expected to use the "parse_student_code". Everything else are helper functions. The resulting dictionary has the following structure:

* Classes - Dictionary that represents a user-defined class. You do not need to specify the name of the class,
            but you must provide the expected  class methods. If no class is detected, this will be an empty string.
            It has the following key-value pairs.
    - Attributes - List of strings representing attributes of a class. 
    - Code - List of strings representing a user-defined class. No comments are in the list. Elements retain leading whitespace.
    - Constructor - Dictionary representing the constructor of a user-defined class. It has the following key-value pairs:
        + Code - List of strings representing the constructor. There is no leading whitespace.
        + Parameters - List of strings representing all of the parameters passed to the constructor.
    - Methods - List of dictionaries. Each dictionary represents a method. It has the following key-value pairs:
        + Code - List of strings representing the method. There is no leading whitespace.
        + Conditionals - List of dictionaries representing a conditional. Each dictionary has the following key-value pairs:
            ~ Code - List of strings representing the conditional. There is no leading whitespace.
            ~ False Branch - List of strings representing the else or else if branch of the conditional.
            ~ True Branch - List of strings representing the if branch of the conditional.
        + Loops - List of dictionaries representing a loop. Each dictionary has the following key-value pairs:
            ~ Code - List of strings representing a loop. There is no leading whitespace.
            ~ Type - String with the value for or while that describes the loop.
        + Name - String with the name of the method.
        + Parameters - List of strings representing the parameters passed to the method.
        + Return Type - String with the type the method should return.
        + Return Value - String representing the value returned by the method. The keyword return is not included in the string.
* Code - List of strings representing student code. Comments and newlines have been removed. Leading whitespace remains. This list of strings is used for the parsing.
* Full Code - List of strings representing the student code as they wrote it. It includes comments and blank lines. This list is not used for parsing.
* Global Variables - List of strings representing the global variables.
* Methods - List of dictionaries. Each dictionary represents a method. It has the following key-value pairs:
    - Code - List of strings representing the method. There is no leading whitespace.
    - Conditionals - List of dictionaries representing a conditional. Each dictionary has the following key-value pairs:
        + Code - List of strings representing the conditional. There is no leading whitespace.
        + False Branch - List of strings representing the else or else if branch of the conditional.
        + True Branch - List of strings representing the if branch of the conditional.
    - Loops - List of dictionaries representing a loop. Each dictionary has the following key-value pairs:
    - Code - List of strings representing a loop. There is no leading whitespace.
    - Type - String with the value for or while that describes the loop.
    - Name - String with the name of the method.
    - Parameters - List of strings representing the parameters passed to the method.
    - Return Type - String with the type the method should return.
    - Return Value - String representing the value returned by the method. The keyword return is not included in the string. 
'''

def parse_student_code(file_name, sketch_methods=['setup', 'draw'], class_methods=None):
  '''
  Returns a dictionary of the parsed student code

  Parameters:
    file_name (string): student file to be parsed; should include the path
    sketch_methods (list of strings): methods expected to be found in the sketch; defaults to "setup" and "draw"
    class_methods (list of strings): methods expected to be found in user-defined class; defaults to "None"

  Returns:
     pc (dictionary): parsed student code; has the keys classes, code, full_code, global_variables, and methods
  '''

  pc = dict()
  pc['full_code'] = read_file(file_name)
  pc['code'] = strip_comments(pc.get('full_code'))
  pc['methods'] = parse_methods(pc.get('code'), sketch_methods)
  pc['classes'] = create_class_dict(pc.get('code'), class_methods) if class_methods else ''
  pc['global_variables'] = get_global_variables(pc.get('methods'), pc.get('code'), pc.get('classes'))

  return pc

#######################
## General Functions
#######################

def read_file(file_name):
  '''
  Returns a list of strings representing the student code as they wrote it

  Parameters:
    file_name (string): student file to be parsed; should include the path

  Returns:
     data (list of strings): lines of student code as they wrote it (no changes made)
  '''

  with open(file_name, 'r') as data:
    return data.readlines()

def get_start_bracket(code, keyword):
  '''
  Returns the index of where the keyword starts in the code list

  Parameters:
    code (list of strings): represents lines of code
    keyword (string): the word to be found in the code

  Returns:
     code.index(line) (integer): index of line of code where keyword was found
  '''

  for line in code:
    if keyword in line:
      return code.index(line)

def get_end_bracket(code, bracket_start):
  '''
  Returns the index of where the code block ends in the code list

  Parameters:
    code (list of strings): represents lines of code
    bracket_start (integer): represents the start of a code block

  Returns:
     code.index(line) (integer): index of line of code where keyword was found
  '''

  opened = 0
  for index, line in enumerate(code[bracket_start:]):
    opened += line.count('{')
    opened -= line.count('}')
    if opened == 0:
      return index + bracket_start + 1

#######################
## Parsing Classes
#######################

def create_class_dict(code, methods):
  '''
  Returns a dictionary that is the parsed class

  Parameters:
    code (list of strings): represents lines of code
    methods (list of strings): represents the methods to be found in the user-defined class

  Returns:
     class_dict (dictionary): represents a parsed class; has the keys name, code, methods, constructor, and attributes
  '''

  class_dict = dict()
  class_start = get_class_start(code)
  class_end = get_end_bracket(code, class_start)
  class_dict['name'] = get_class_name(code, class_start)
  class_dict['code'] = code[class_start:class_end]
  class_dict['methods'] = parse_methods(class_dict['code'], methods)
  class_dict['constructor'] = get_class_constructor(class_dict['code'], class_dict['name'])
  class_dict['attributes'] = get_class_attributes(class_dict['code'], class_dict['name'])

  return class_dict

def get_class_constructor(code, class_name):
  '''
  Returns a dictionary that is the parsed constructor

  Parameters:
    code (list of strings): represents lines of code
    class_name (string): represents the name of the user-defined class

  Returns:
     constructor (dictionary): represents a parsed class; has the keys code and parameters
  '''

  constructor = dict()
  constructor_start = get_start_bracket(code[1:], class_name) + 1
  constructor_end = get_end_bracket(code, constructor_start)
  constructor_code = [line.strip() for line in code[constructor_start:constructor_end]]
  parameters = get_constructor_parameters(constructor_code[0])
  constructor['code'] = constructor_code
  constructor['parameters'] = parameters

  return constructor

def get_constructor_parameters(constructor_header):
  '''
  Returns a list of strings representing the parameters passed to the constructor

  Parameters:
    constructor_header (string): represents the first line of the constructor

  Returns:
     parameters_list (list of strings): represents the parameters passed to the constructor
  '''

  parameters_start = constructor_header.index('(')
  parameters_end = constructor_header.index(')')
  parameters_string = constructor_header[parameters_start + 1:parameters_end]
  parameters_list = [line.strip() for line in parameters_string.split(',')]

  return parameters_list

def get_class_attributes(code, class_name):
  '''
  Returns a list of strings representing the attributes in a user-defined class

  Parameters:
    code (list of strings): represents lines of code
    class_name (string): represents the name of the user-defined class

  Returns:
     attributes (list of strings): represents the attributes in a user-defined class
  '''

  attributes = []
  for line in code[1:]:
    if class_name not in line:
      attributes.append(line.strip())
    else:
      break

  return attributes

def get_class_method(code, class_method):
  '''
  Returns a list of strings representing a method in a user-defined class

  Parameters:
    code (list of strings): represents lines of code
    class_method (string): represents the name of the method

  Returns:
     code[method_start:method_end] (list of strings): represents lines of code of a method in a user-defined class
  '''

  method_start = get_start_bracket(code, class_method)
  method_end = get_end_bracket(code, method_start)

  return code[method_start:method_end]

def get_class_start(code):
  '''
  Returns the index of the start of the user-defined class

  Parameters:
    code (list of strings): represents lines of code

  Returns:
     code.index(line) (integer): represents index of the line where the user-defined class starts; returns -1 if not found
  '''

  for line in code:
    if line.startswith('class'):

      return code.index(line)

  return -1

def get_class_name(code, class_start):
  '''
  Returns a string that is the class name

  Parameters:
    code (list of strings): represents lines of code
    class_start (string): represents the starting index of the user-defined class

  Returns:
     name (string): represents the name of the class
  '''

  end_class_name = code[class_start].index('{')
  name = code[class_start][5:end_class_name].strip()

  return name

#######################
## Parsing Loops
#######################

## Only checks for "for" and "while" loops
## as those are the officeal vehicles for
## iteration in the Processing docs.

def get_loop(method, index):
  '''
  Returns a list of strings representing the lines of code in a loop

  Parameters:
    method (list of strings): represents lines of code in a method
    index (integer): represents the start of the loop

  Returns:
     method[loop_start:loop_end] (list of strings): represents lines of code for a loop; returns "None" if not present
  '''

  loop_start = index
  loop_end = get_end_bracket(method, loop_start)

  return method[loop_start:loop_end] if loop_start != -1 else None

def parse_loops(method):
  '''
  Returns a list of dictionaries representing loops

  Parameters:
    method (list of strings): represents lines of code in a method

  Returns:
     loops (list of dictionaries): represents the loops in a method; dictionary has the keys type and code
  '''

  loops = []
  for line in method:
    if 'for(' in line.replace(' ', ''):
      loop = dict()
      loop['type'] = 'for'
      loop['code'] = get_loop(method, method.index(line))
      loops.append(loop)
    if 'while(' in line.replace(' ', ''):
      loop = dict()
      loop['type'] = 'while'
      loop['code'] = get_loop(method, method.index(line))
      loops.append(loop)

  return loops

###########################
## Parsing Global Variables
###########################

def get_global_variables(methods, code, classes):
  '''
  Returns a sorted list of strings representing the global variables

  Parameters:
    methods (list of dictionaries): represents all of the methods in the sketch
    code (list of strings): represents the lines of code in the sketch
    classes (dictionary): represents the user-defined class in the sketch

  Returns:
     list(code_set - methods_set - class_set) (list of strings): represents global variables in the sketch; this list is sorted
  '''

  methods_set = set()
  code_set = set([line.strip() for line in code])
  class_set = set(classes.get('code')) if len(classes) != 0 else set()
  for method in methods:
    set_from_list = set(method.get('code'))
    methods_set.update(set_from_list)
  variable_list = list(code_set - methods_set - class_set)
  variable_list.sort()

  return variable_list

#######################
## Parsing Conditionals
#######################

## All conditionals with an else statement are expected
##  to be in the format from the Processing documentation:
## } else {
## } else if (cond) {
## The else statement and curly brackets are on the same line

def fetch_conditional_code(method_body, index):
  '''
  Returns a list of strings representing a conditional

  Parameters:
    method_body (list of strings): represents lines of code in a method
    index (integer): represents the start of a conditional

  Returns:
     method_body[cond_start:cond_end] (list of strings): represents lines of code in a conditional
  '''

  cond_start = index
  opened = 0
  for index, line in enumerate(method_body[cond_start:-1]):
    opened += 1 if '{' in line else 0
    opened -= 1 if '}' in line else 0
    if opened == 0:
      cond_end = index + cond_start + 1

      return method_body[cond_start:cond_end]

def find_else_index(code):
  '''
  Returns the index of the element that contains "else"

  Parameters:
    code (list of strings): represents lines of code

  Returns:
     code.index(line) (integer): represents the start of the else statement
  '''

  for line in code:
    if 'else' in line:

      return code.index(line)

def fetch_true_branch(conditional_code):
  '''
  Returns a list of strings that represent the first half of a conditional (true branch)

  Parameters:
    conditional_code (list of strings): represents lines of code in a complete conditional

  Returns:
     code.index(line) (list of strings): represents the true branch of a conditional
  '''

  cond_end = find_else_index(conditional_code)

  return conditional_code[:cond_end]

def fetch_false_branch(conditional_code):
  '''
  Returns a list of strings that represent the second half of a conditional (false branch); returns an empty string if there is no false branch

  Parameters:
    conditional_code (list of strings): represents lines of code in a complete conditional

  Returns:
     conditional_code[false_start:] (list of strings): represents the false branch of a conditional; could be an empty string if there is no else statement
  '''

  false_start = find_else_index(conditional_code)
  if false_start == None:
    return ''

  return conditional_code[false_start:]

def parse_conditional(method_body):
  '''
  Returns a list of dictionaries that represent each conditional

  Parameters:
    method_body (list of strings): represents lines of code in a method

  Returns:
     conditionals (list of dictionaries): represents the conditionals in a method
  '''

  conditionals = []
  for line in method_body:
    if 'if(' in line.replace(' ', '') and 'else' not in line:
      conditional = dict()
      index = method_body.index(line)
      conditional['code'] = fetch_conditional_code(method_body, index)
      conditional['true_branch'] = fetch_true_branch(conditional.get('code'))
      conditional['false_branch'] = fetch_false_branch(conditional.get('code'))
      conditionals.append(conditional)

  return conditionals

#######################
## Parsing Methods
#######################

def parse_methods(code, required_methods):
  '''
  Returns a list of lists where each element in the first list represents an expected method

  Parameters:
    code (list of strings): represents lines of code in the student sketch
    required_methods (list of strings): represents the methods expected to be found in the sketch (not in a user-defined class)

  Returns:
     methods (list of lists): represents the code (list of strings) for each method expected to be in the sketch
  '''

  methods = []
  for method in required_methods:
    methods.append(fetch_method(code, method))

  return methods

def get_method_name(method_header):
  '''
  Returns a string that represents the name of the method

  Parameters:
    method_header (string): represents the header of a method

  Returns:
     name (string): represents the name of the method
  '''

  split_header = method_header.strip().split(' ')
  end_name = split_header[1].index('(')
  name = split_header[1][:end_name]

  return name

def get_method_type(method_header):
  '''
  Returns a string that represents the return type of the method

  Parameters:
    method_header (string): represents the header of a method

  Returns:
     return_type (string): represents the return type of the method
  '''

  split_header = method_header.strip().split(' ')
  return_type = split_header[0]

  return return_type

def get_method_parameters(method_header):
  '''
  Returns a list of strings that represents the parameters for a method

  Parameters:
    method_header (string): represents the header of a method

  Returns:
     parameters (list of strings): represents the parameters for the method
  '''

  param_start = method_header.index('(') + 1
  param_end = method_header.index(')')
  parameters = [param.strip() for param in method_header[param_start:param_end].split(',')]

  return parameters

def create_method_dict(method):
  '''
  Returns a dictionary with information about method

  Parameters:
    method (string): represents the name of a method

  Returns:
     method_dict (dictionary): represents a method; it has the keys return_type, name, parameters, code, conditionals, loops, and return_value
  '''

  method_dict = dict()
  method_dict['return_type'] = get_method_type(method[0])
  method_dict['name'] = get_method_name(method[0])
  method_dict['parameters'] = get_method_parameters(method[0])
  method_dict['code'] = [line.strip() for line in method]
  method_dict['conditionals'] = parse_conditional(method_dict['code'])
  method_dict['loops'] = parse_loops(method_dict['code'])
  method_dict['return_value'] = get_return_value(method_dict['code'])

  return method_dict

def get_method_start(code, method):
  '''
  Returns an integer that represents the starting line of the method

  Parameters:
    code (list of strings): represents the lines of the student code
    method (string): represents the name of a method

  Returns:
     code.index(line) (integer): represents index of the start of the method
  '''

  for line in code:
    words = line.split()
    if len(words) > 1:
      if method in line.split()[1]:

        return code.index(line)

def fetch_method(code, method):
  '''
  Returns a dictionary that represents a method

  Parameters:
    code (list of strings): represents the lines of the student code
    method (string): represents the name of a method

  Returns:
     method_dict (dictionary): represents a method
  '''

  method_start = get_method_start(code, method)
  method_end = get_end_bracket(code, method_start)
  method_code = code[method_start:method_end]
  method_dict = create_method_dict(method_code)

  return method_dict

def get_return_value(method):
  '''
  Returns a string that represents the return value of a method; an empty string is return if there is no "return" statement

  Parameters:
    method (list of strings): represents the lines of code in a method

  Returns:
     line[7:].replace(';', '') (string): represents the return value of the method; returns an empty string if no "return" statement
  '''

  for line in method:
    if 'return' in line:

      return line[7:].replace(';', '')

  return ''

#######################
## Removing Comments
#######################

def strip_leading_comments(code):
  '''
  Returns a list of strings that represents the student code minus any leading comments (lines that start with "//")

  Parameters:
    code (list of strings): represents the lines of code in the sketch

  Returns:
     [line for line in code if not(line.strip().startswith('//'))] (list of strings): represents student code minus lines that start with "//"
  '''

  return [line for line in code if not(line.strip().startswith('//'))]

def strip_trailing_comments(code):
  '''
  Returns a list of strings that represents the student code minus any trailing comments (lines that end with "//")

  Parameters:
    code (list of strings): represents the lines of code in the sketch

  Returns:
     [line[:line.find('//')] if '//' in line else line for line in code] (list of strings): represents student code minus lines that end with "//"
  '''

  return [line[:line.find('//')] if '//' in line else line for line in code]

def multiline_starting_indices(code):
  '''
  Returns a tuple of integers that represents the starting indices for multiline comments

  Parameters:
    code (list of strings): represents the lines of code in the sketch

  Returns:
     starting_indices (tuple of integers): represents the indices of elements that start with "/*"
  '''

  starting_indices = ()
  for line in code:
    if line.strip().startswith('/*'):
      starting_indices += (code.index(line),)

  return starting_indices

def multiline_ending_indices(code):
  '''
  Returns a tuple of integers that represents the ending indices for multiline comments

  Parameters:
    code (list of strings): represents the lines of code in the sketch

  Returns:
     ending_indices (tuple of integers): represents the indices of elements that end with "*/"
  '''

  ending_indices = ()
  for line in code:
    if line.strip().endswith('*/'):
      ending_indices += (code.index(line),)

  return ending_indices

def strip_multiline_comments(code):
  '''
  Returns a list of strings that represents student code without multiline comments

  Parameters:
    code (list of strings): represents the lines of code in the sketch

  Returns:
     no_multiline_comments (list of strings): represents the lines of code minus multiline comments
  '''

  starting_indices = multiline_starting_indices(code)
  ending_indices = multiline_ending_indices(code)
  zipped = list(zip(starting_indices, ending_indices))
  for item in list(zipped):
    for i in range(item[0], item[1] + 1):
      code[i] = '~~delete~me~~'
  no_multiline_comments = [line for line in code if line != '~~delete~me~~']
  
  return no_multiline_comments

def strip_comments(code):
  '''
  Returns a list of strings that represents student code without any comments

  Parameters:
    code (list of strings): represents the lines of code in the sketch

  Returns:
     no_comments (list of strings): represents the lines of code minus all comments
  '''

  code_no_newlines = [line.rstrip() for line in code]
  code_no_blank_lines = [line for line in code_no_newlines if line != '']
  no_comments = strip_leading_comments(code_no_blank_lines)
  no_comments = strip_trailing_comments(no_comments)
  no_comments = strip_multiline_comments(no_comments)

  return no_comments

