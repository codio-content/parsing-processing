# Parsing Processing Code

## Purpose

The idea behind this project is to transform student code in Processing into something that instructors can easily query. Every student sketch should have a standard structure from the assessment point of view.

## Parsing Student Code

```python
from ppc import parse_student_code

file = ‘path/to/student/file.pde’
parsed_code = parse_student_code(file)
```

To parse student code, import the `parse_student_code` function from the `ppc` (Parsing Processing Code) module. You only need to call the `parse_student_code` function. At a minimum, you need a student file (including the path) to parse. By default, the function will parse the `setup` and `draw` methods and it will not parse the user-defined class. 

If you want to parse user-defined methods, you need to use the `sketch_methods` optional argument. Create a list of method names (including `setup` and `draw`) you expect to see in the sketch. Pass the list to the `sketch_methods` optional argument.

```python
from ppc import parse_student_code

file = ‘path/to/student/file.pde’
expected_methods = [‘setup’, ‘draw’, ‘user_method1’, ‘user_method2’]
parsed_code = parse_student_code(file, sketch_methods=expected_methods)
```

If you want to parse a user-defined class, you need to make use of the `class_methods` optional argument. By default, this argument defaults to `None`. Create a list of the expected class methods and pass it to the `class_methods` optional argument.

```python
from ppc import parse_student_code

file = ‘path/to/student/file.pde’
class_methods = [‘class_method1’, ‘class_method2’, ‘class_method3’]
parsed_code = parse_student_code(file, class_methods=class_methods)
```

## Limitations

This is not a fully comprehensive Processing parser. It is designed to do “just enough” for a UTD course. As such, there are several limitations to the parser.

* You have to provide a list of required methods when parsing student code.
* The parser assumes only one user-defined class. In addition, you have to provide a list of required methods when parsing a user-defined class.
* According to the [Processing documentation](https://processing.org/reference#control), loops are either for-loops or while-loops. The parser only works with these kinds of loops. Other valid loops from Java are not included in this structure.
* Conditionals expect curly braces to be on the same line as the “else” or “else if” statements as shown in the [Processing documentation](https://processing.org/reference/else.html).
* This parsing structure is not very granular. It does not determine if there are nested loops, for example. You would have to manually search the body of a loop for another loop.

## Parsing Structure

Student code is represented as a dictionary. The list below is an example of the general overall structure of how student code is represented:

* **Classes** - Dictionary that represents a user-defined class. You do not need to specify the name of the class, but you must provide the expected class methods. If no class is detected, this will be an empty string. It has the following key-value pairs.
    * **Attributes** - List of strings representing attributes of a class. 
    * **Code** - List of strings representing a user-defined class. No comments are in the list. Elements retain leading whitespace.
    * **Constructor** - Dictionary representing the constructor of a user-defined class. It has the following key-value pairs:
        * **Code** - List of strings representing the constructor. There is no leading whitespace.
        * **Parameters** - List of strings representing all of the parameters passed to the constructor.
    * **Methods** - List of dictionaries. Each dictionary represents a method. It has the following key-value pairs:
        * **Code** - List of strings representing the method. There is no leading whitespace.
        * **Conditionals** - List of dictionaries representing a conditional. Each dictionary has the following key-value pairs:
            * **Code** - List of strings representing the conditional. There is no leading whitespace.
            * **False Branch** - List of strings representing the `else` or `else if` branch of the conditional.
            * **True Branch** - List of strings representing the `if` branch of the conditional.
        * **Loops** - List of dictionaries representing a loop. Each dictionary has the following key-value pairs:
            * **Code** - List of strings representing a loop. There is no leading whitespace.
            * **Type** - String with the value `for` or `while` that describes the loop.
        * **Name** - String with the name of the method.
        * **Parameters** - List of strings representing the parameters passed to the method.
        * **Return Type** - String with the type the method should return.
        * **Return Value** - String representing the value returned by the method. The keyword `return` is not included in the string.
    * **Code** - List of strings representing student code. Comments and newlines have been removed. Leading whitespace remains. This list of strings is used for the parsing.
    * **Full Code** - List of strings representing the student code as they wrote it. It includes comments and blank lines. This list is not used for parsing.
    * **Global Variables** - List of strings representing the global variables.
    * **Methods** - List of dictionaries. Each dictionary represents a method. It has the following key-value pairs:
        * **Code** - List of strings representing the method. There is no leading whitespace.
        * **Conditionals** - List of dictionaries representing a conditional. Each dictionary has the following key-value pairs:
            * **Code** - List of strings representing the conditional. There is no leading whitespace.
            * **False Branch** - List of strings representing the `else` or `else if` branch of the conditional.
            * **True Branch** - List of strings representing the `if` branch of the conditional.
        * **Loops** - List of dictionaries representing a loop. Each dictionary has the following key-value pairs:
            * **Code** - List of strings representing a loop. There is no leading whitespace.
            * **Type** - String with the value `for` or `while` that describes the loop.
        * **Name** - String with the name of the method.
        * **Parameters** - List of strings representing the parameters passed to the method.
        * **Return Type** - String with the type the method should return.
        * **Return Value** - String representing the value returned by the method. The keyword `return` is not included in the string. 

## Querying Processing Code

Once the student code has been parsed with the `parse_student_code` function, you can query this structure with the `qpc` (query processing code) module.

```python
from ppc import parse_student_code
import qpc

file = ‘path/to/student/file.pde’
parsed_code = parse_student_code(file)
setup_for_loops = qpc.get_method_for_loops(parsed_code, 'setup')
```

For more information on the functions available in the `qpc` module, use `pydoc`. The following command will open the documentation in the terminal:

```
python3 -m pydoc qpc
```

Press `Enter` to page through the documentation. Pressing `q` will exit the docs.

You can open the documenation in your browser with the following command:

```
python3 -m pydoc -b
```

Note, this command will not work if you are running this command in a Codio box. In Codio, you will see the `qpc.html` file in the `docs` directory. Right-click on the file and select `Preview static` to see the documentation.
