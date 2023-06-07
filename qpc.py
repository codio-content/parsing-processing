'''
Query Processing Code (QPC) - Collection of functions to query Processing code once it has gone through the PPC parser
'''

#####################################
## Working with complete student code
#####################################

def get_code(pc):
  '''
  Returns a list of strings representing the Processing code the student wrote minus comments and blank lines

  Parameters:
    pc (dictionary): parsed student code

  Returns:
    code (list of strings): student code minus comments and blank lines
  '''

  return pc.get('code')

def get_full_code(pc):
  '''
  Returns a list of strings representing the Processing code as the student wrote it

  Parameters:
    pc (dictionary): parsed student code

  Returns:
    full_code (list of strings): Processing code as the student wrote it
  '''

  return pc.get('full_code')

################################
## Working with global variables
################################

def has_global_variable(pc, expected_variable):
  '''
  Returns a boolean denoting if a global variable is present in the sketch

  Parameters:
    pc (dictionary): parsed student code
    expected_variable (string): the global variable expected to be found in student code

  Returns:
    True or False (boolean): expected variable is found or not
  '''

  global_variables = pc.get('global_variables')
  for variable in global_variables:
    if variable == expected_variable:
      return True
  return False

def get_global_variables(pc):
  '''
  Returns a list of global variables in the sketch

  Parameters:
    pc (dictionary): dictionary representing the parsed student code

  Returns:
    global_variables (list of strings): global variables declared in the sketch
  '''

  return pc.get('global_variables')

#######################
## Working with methods
#######################

def get_method(pc, method_name):
  '''
  Returns a dictionary containing a parsed method. 

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    method_name (string): the method name expected to be found in student code

  Returns:
    method (dictionary): parsed method; the dictionary has the keys code, conditionals, loops, name, parameters, return_type, and return_value
    None (None type): represents lack of expected method
  '''

  methods = pc.get('methods')
  for method in methods:
    if method.get('name') == method_name:
      return method
  return None

def method_has_name(pc, method_name):
  '''
  Returns a boolean or None if the expected method is found (or not) in student code

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    method_name (string): the method name expected to be found in student code

  Returns:
    True or False (boolean): method is found or not
  '''

  method = get_method(pc, method_name)
  if method.get('name') == method_name:
    return True
  else:
    return False

def get_method_code(pc, method_name):
  '''
Returns a list of strings of the code found in a specified method

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    method_name (string): the method name expected to be found in student code

  Returns:
    code (list of strings): lines of code from the method
  '''

  method = get_method(pc, method_name)
  return method.get('code')

def get_method_parameters(pc, method_name):
  '''
  Returns a list of strings of the code of the parameters for a specified method

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    method_name (string): the method name expected to be found in student code

  Returns:
    parameters (list of strings): parameters for the specified method; returns a list with an empty string if no parameters
  '''

  method = get_method(pc, method_name)
  return method.get('parameters')

def get_method_return_type(pc, method_name):
  '''
  Returns a string representing the data type the method must return

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    method_name (string): the method name expected to be found in student code

  Returns:
    return_type (string): data type the method must return
  '''

  method = get_method(pc, method_name)
  return method.get('return_type')

def get_method_return_value(pc, method_name):
  '''
  Returns a string representing the value the method returns; returns an empty string for "void" methods

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    method_name (string): the method name expected to be found in student code

  Returns:
    return_value (string): value the method returns; does not include the word "return"
  '''

  method = get_method(pc, method_name)
  return method.get('return_value')

def get_method_loops(pc, method_name):
  '''
  Returns a list of dictionaries representing all loops found in the method

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    method_name (string): the method name expected to be found in student code

  Returns:
    loops (list of dictionaries): all loops found in a specified method; dictionary has the keys type and code
  '''

  method = get_method(pc, method_name)
  return method.get('loops')

def method_has_for_loop(pc, method_name):
  '''
  Returns a boolean if the method has a for loop

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    method_name (string): the method name expected to be found in student code

  Returns:
    True or False (boolean): for loop is found or not
  '''

  method = get_method(pc, method_name)
  loops = method.get('loops')
  for loop in loops:
    if loop.get('type') == 'for':
      return True
  return False

def method_has_while_loop(pc, method_name):
  '''
  Returns a boolean if the method has a while loop

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    method_name (string): the method name expected to be found in student code

  Returns:
     True or False (boolean): while loop is found or not
  '''

  method = get_method(pc, method_name)
  loops = method.get('loops')
  for loop in loops:
    if loop.get('type') == 'while':
      return True
  return False

def method_has_conditional(pc, method_name):
  '''
  Returns a boolean if the method has a conditional

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    method_name (string): the method name expected to be found in student code

  Returns:
     True or False (boolean): method has conditional or not
  '''

  method = get_method(pc, method_name)
  return len(method.get('conditionals')) > 0

#######################
## Working with classes
#######################

def has_class_name(pc, class_name):
  '''
  Returns a boolean if the class name is found

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    class_name (string): the class name expected to be found in student code

  Returns:
     True or False (boolean): class name is found or not
  '''

  return pc.get('classes').get('name') == class_name

def get_class(pc):
  '''
  Returns a dictionary representing the class

  Parameters:
    pc (dictionary): dictionary representing the parsed student code

  Returns:
     classes (dictionary): dictionary representation of the class; has the keys name, code, methods, constructor, and attributes
  '''

  return pc.get('classes')

def get_constructor(pc):
  '''
  Returns a dictionary representing the constructor

  Parameters:
    pc (dictionary): dictionary representing the parsed student code

  Returns:
    constructor (dictionary): dictionary representation of the class; has the keys code and parameters
  '''

  return pc.get('classes').get('constructor')

def get_constructor_parameters(pc):
  '''
  Returns a list of strings representing the parameters for the constructor

  Parameters:
    pc (dictionary): dictionary representing the parsed student code

  Returns:
    parameters (list of strings): list of strings representing the parameters for the constructor
  '''

  return pc.get('classes').get('constructor').get('parameters')

def get_constructor_code(pc):
  '''
  Returns a list of strings representing the code for the constructor

  Parameters:
    pc (dictionary): dictionary representing the parsed student code

  Returns:
    code (list of strings): lines of code for the constructor
  '''

  return pc.get('classes').get('constructor').get('code')

def has_class_method(pc, method_name):
  '''
  Returns a boolean if the class method name is found

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    method_name (string): the method name expected to be found in the class

  Returns:
     True or False (boolean): method name is found or not in the class
  '''

  return get_method(pc.get('classes'), method_name)

def has_attribute(pc, expected_attribute):
  '''
  Returns a boolean if the attribute is found in the class

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    expected_attribute (string): the attribute name expected to be found in the class

  Returns:
     True or False (boolean): attribute is found or not in the class
  '''

  attributes = pc.get('classes').get('attributes')
  for attribute in attributes:
    if attribute == expected_attribute:
      return True
  return False

def get_attributes(pc):
  '''
  Returns a list of strings representing the attributes for the class

  Parameters:
    pc (dictionary): dictionary representing the parsed student code

  Returns:
    attributes (list of strings): list of strings representing the attributes for the class
  '''

  return pc.get('classes').get('attributes')

#####################
## Working with loops
#####################

def get_method_for_loops(pc, method_name, index=None):
  '''
  Returns a list of strings represeting a single for loop; if no value for "index" is provided then it returns a 2D list representing the code for every for loop in a method

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    method_name (string): the method name expected to be found in student code
    index (integer): specifies which for loop code to return; defaults to None

  Returns:
    for_loops (list of lists or list of strings): lines of code representing a for loop (list of strings) or all for loops (list of lists)
  '''

  method = get_method(pc, method_name)
  loops = method.get('loops')
  for_loops = [loop.get('code') for loop in loops if loop.get('type') == 'for']
  if index == None:
    return for_loops
  else:
    return for_loops[index]

def get_method_while_loops(pc, method_name, index=None):
  '''
  Returns a list of strings represeting a single while loop; if no value for "index" is provided then it returns a 2D list representing the code for every while loop in a method

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    method_name (string): the method name expected to be found in student code
    index (integer): specifies which for loop code to return; defaults to None

  Returns:
    while_loops (list of lists or list of strings): lines of code representing a while loop (list of strings) or all while loops (list of lists)
  '''

  method = get_method(pc, method_name)
  loops = method.get('loops')
  while_loops = [loop.get('code') for loop in loops if loop.get('type') == 'while']
  if index == None:
    return while_loops
  else:
    return while_loops[index]

def get_method_conditionals(pc, method_name, index=None):
  '''
  Returns a dictionaries represeting a conditional statements; if no value for "index" is provided then it returns a list of dictionaries representing all conditionals in a method

  Parameters:
    pc (dictionary): dictionary representing the parsed student code
    method_name (string): the method name expected to be found in student code
    index (integer): specifies which conditional to return; defaults to None

  Returns:
    conditionals (list of dictionaries): conditionals in a method; the dictionary has the keys code, true_branch, and false_branch
  '''

  method = get_method(pc, method_name)
  conditionals = method.get('conditionals')
  if index == None:
    return [cond.get('code') for cond in conditionals]
  else:
    return conditionals[index].get('code')