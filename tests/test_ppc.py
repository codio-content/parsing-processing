import unittest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ppc import parse_student_code

class TestPPC(unittest.TestCase):

  def test_class_name(self):
    test_file = 'test_sketches/class_example.pde'
    class_methods = ['update']
    self.code = parse_student_code(test_file, class_methods=class_methods)
    self.assertEqual(self.code.get('classes').get('name'), "HLine")

  def test_class_code(self):
    test_file = 'test_sketches/class_example.pde'
    class_methods = ['update']
    expected_code = ['class HLine {', '  float ypos, speed;', '  HLine (float y, float s, String s1, int num) {', '    ypos = y;', '    speed = s;', '  }', '  void update() {', '    ypos += speed;', '    if (ypos > height) {', '      ypos = 0;', '    }', '    line(0, ypos, width, ypos);', '  }', '}']
    self.code = parse_student_code(test_file, class_methods=class_methods)
    self.assertEqual(self.code.get('classes').get('code'), expected_code)

  def test_class_methods(self):
    test_file = 'test_sketches/class_example.pde'
    class_methods = ['update']
    expected_name = 'update'
    expected_return_type = 'void'
    expected_parameters = ['']
    expected_return_value = ''
    expected_conditional = ['if (ypos > height) {', 'ypos = 0;', '}']
    expected_code = ['void update() {', 'ypos += speed;', 'if (ypos > height) {', 'ypos = 0;', '}', 'line(0, ypos, width, ypos);', '}']
    self.code = parse_student_code(test_file, class_methods=class_methods)
    self.assertEqual(self.code.get('classes').get('methods')[0].get('code'), expected_code)
    self.assertEqual(self.code.get('classes').get('methods')[0].get('name'), expected_name)
    self.assertEqual(self.code.get('classes').get('methods')[0].get('return_type'), expected_return_type)
    self.assertEqual(self.code.get('classes').get('methods')[0].get('return_value'), expected_return_value)
    self.assertEqual(self.code.get('classes').get('methods')[0].get('parameters'), expected_parameters)
    self.assertEqual(self.code.get('classes').get('methods')[0].get('conditionals')[0].get('code'), expected_conditional)

  def test_class_constructor(self):
    test_file = 'test_sketches/class_example.pde'
    class_methods = ['update']
    expected_constructor = ['HLine (float y, float s, String s1, int num) {', 'ypos = y;', 'speed = s;', '}']
    expected_parameters = ['float y', 'float s', 'String s1', 'int num']
    self.code = parse_student_code(test_file, class_methods=class_methods)
    self.assertEqual(self.code.get('classes').get('constructor').get('code'), expected_constructor)
    self.assertEqual(self.code.get('classes').get('constructor').get('parameters'), expected_parameters)

  def test_class_attributes(self):
    test_file = 'test_sketches/class_example.pde'
    class_methods = ['update']
    expected_attributes = ['float ypos, speed;']
    self.code = parse_student_code(test_file, class_methods=class_methods)
    self.assertEqual(self.code.get('classes').get('attributes'), expected_attributes)

  def test_code_no_comments(self):
    expected = ['void setup() {', '  size(200, 200); ', '}', 'void draw() {', '  background(0);', '}']
    test_file = 'test_sketches/comments.pde'
    self.code = parse_student_code(test_file)
    self.assertEqual(self.code.get('code'), expected)

  def test_conditional_code(self):
    test_file = 'test_sketches/conditionals.pde'
    self.code = parse_student_code(test_file)
    expected_conditional_1 = ['if (xpos > width) {', 'xpos = 0;', '}']
    expected_conditional_2 = ['if (num % 2 == 0) {', 'println("Even");', '} else {', 'println("Odd");', '}']
    expected_conditional_3 = ['if (a < b) {', 'printlin("less");', '} else if (a > b) {', 'println("greater");', '} else {', 'println("equal");', '}']
    self.assertEqual(self.code.get('methods')[0].get('conditionals')[0].get('code'), expected_conditional_1)
    self.assertEqual(self.code.get('methods')[1].get('conditionals')[0].get('code'), expected_conditional_2)
    self.assertEqual(self.code.get('methods')[1].get('conditionals')[1].get('code'), expected_conditional_3)

  def test_conditional_true(self):
    test_file = 'test_sketches/conditionals.pde'
    self.code = parse_student_code(test_file)
    expected_true_branch_1 = ['if (xpos > width) {', 'xpos = 0;', '}']
    expected_true_branch_2 = ['if (num % 2 == 0) {', 'println("Even");']
    expected_true_branch_3 = ['if (a < b) {', 'printlin("less");']
    self.assertEqual(self.code.get('methods')[0].get('conditionals')[0].get('true_branch'), expected_true_branch_1)
    self.assertEqual(self.code.get('methods')[1].get('conditionals')[0].get('true_branch'), expected_true_branch_2)
    self.assertEqual(self.code.get('methods')[1].get('conditionals')[1].get('true_branch'), expected_true_branch_3)

  def test_conditional_false(self):
    test_file = 'test_sketches/conditionals.pde'
    self.code = parse_student_code(test_file)
    expected_false_branch_1 = ''
    expected_false_branch_2 = ['} else {', 'println("Odd");', '}']
    expected_false_branch_3 = ['} else if (a > b) {', 'println("greater");', '} else {', 'println("equal");', '}']
    self.assertEqual(self.code.get('methods')[0].get('conditionals')[0].get('false_branch'), expected_false_branch_1)
    self.assertEqual(self.code.get('methods')[1].get('conditionals')[0].get('false_branch'), expected_false_branch_2)
    self.assertEqual(self.code.get('methods')[1].get('conditionals')[1].get('false_branch'), expected_false_branch_3)

  def test_nested_conditionals(self):
    test_file = 'test_sketches/nested_conditionals.pde'
    self.code = parse_student_code(test_file)
    expected_true_branch_1 = ['if (5 < 7) {', 'if (10 > 1) {', 'println("Inner conditional");', '}']
    expected_true_branch_2 = ['if (10 > 1) {', 'println("Inner conditional");', '}']
    expected_true_branch_3 = ['if (1 == 2) {', 'println("Another inner conditional");']
    expected_false_branch_1 = ['} else {', 'if (1 == 2) {', 'println("Another inner conditional");', '} else if (true) {', 'println("Last conditional");', '}', '}']
    expected_false_branch_2 = ''
    expected_false_branch_3 = ['} else if (true) {', 'println("Last conditional");', '}']
    self.assertEqual(self.code.get('methods')[1].get('conditionals')[0].get('true_branch'), expected_true_branch_1)
    self.assertEqual(self.code.get('methods')[1].get('conditionals')[1].get('true_branch'), expected_true_branch_2)
    self.assertEqual(self.code.get('methods')[1].get('conditionals')[2].get('true_branch'), expected_true_branch_3)
    self.assertEqual(self.code.get('methods')[1].get('conditionals')[0].get('false_branch'), expected_false_branch_1)
    self.assertEqual(self.code.get('methods')[1].get('conditionals')[1].get('false_branch'), expected_false_branch_2)
    self.assertEqual(self.code.get('methods')[1].get('conditionals')[2].get('false_branch'), expected_false_branch_3)

  def test_global_variables(self):
    expected = ['int age;', 'float x = 7.2;', 'String name = "Calvin";']
    test_file = 'test_sketches/global_variables.pde'
    self.code = parse_student_code(test_file)
    # lists are sorted since parsed comes from a set, order can change
    expected.sort()
    self.assertEqual(self.code.get('global_variables'), expected)

  def test_global_variabels_methods_file(self):
    expected_methods = ['setup', 'draw', 'checkEdge', 'evenOdd', 'concatStrings']
    test_file = 'test_sketches/methods.pde'
    expected_global_variable = ['int xpos = 0;']
    self.code = parse_student_code(test_file, sketch_methods=expected_methods)
    # lists are sorted since parsed comes from a set, order can change
    expected_global_variable.sort()
    self.assertEqual(self.code.get('global_variables'), expected_global_variable)

  def test_for_loop(self):
    expected_loop_code = ['for(int i = 0; i < 10; i++) {', 'println("Hello unit test!");', '}']
    expected_loop_type = 'for'
    test_file = 'test_sketches/for_loop.pde'
    self.code = parse_student_code(test_file)
    self.assertEqual(self.code.get('methods')[1].get('loops')[0].get('code'), expected_loop_code)
    self.assertEqual(self.code.get('methods')[1].get('loops')[0].get('type'), expected_loop_type)

  def test_while_loop(self):
    expected_loop_code = ['while(index < limit) {', 'println("Hello unit test!");', 'index++;', '}']
    expected_loop_type = 'while'
    test_file = 'test_sketches/while_loop.pde'
    self.code = parse_student_code(test_file)
    self.assertEqual(self.code.get('methods')[1].get('loops')[0].get('code'), expected_loop_code)
    self.assertEqual(self.code.get('methods')[1].get('loops')[0].get('type'), expected_loop_type)

  def test_method_name(self):
    expected_names = ['setup', 'draw', 'checkEdge', 'evenOdd', 'concatStrings']
    test_file = 'test_sketches/methods.pde'
    self.code = parse_student_code(test_file, expected_names)
    self.assertIn(self.code.get('methods')[0].get('name'), expected_names)
    self.assertIn(self.code.get('methods')[1].get('name'), expected_names)
    self.assertIn(self.code.get('methods')[2].get('name'), expected_names)
    self.assertIn(self.code.get('methods')[3].get('name'), expected_names)
    self.assertIn(self.code.get('methods')[4].get('name'), expected_names)

  def test_method_parameters(self):
    expected_names = ['setup', 'draw', 'checkEdge', 'evenOdd', 'concatStrings']
    test_file = 'test_sketches/methods.pde'
    self.code = parse_student_code(test_file, expected_names)
    self.assertEqual(self.code.get('methods')[0].get('parameters'), [''])
    self.assertEqual(self.code.get('methods')[1].get('parameters'), [''])
    self.assertEqual(self.code.get('methods')[2].get('parameters'), [''])
    self.assertEqual(self.code.get('methods')[3].get('parameters'), ['int num'])
    self.assertEqual(self.code.get('methods')[4].get('parameters'), ['String s1', 'String s2'])

  def test_method_return_type(self):
    expected_names = ['setup', 'draw', 'checkEdge', 'evenOdd', 'concatStrings']
    test_file = 'test_sketches/methods.pde'
    self.code = parse_student_code(test_file, expected_names)
    self.assertEqual(self.code.get('methods')[0].get('return_type'), 'void')
    self.assertEqual(self.code.get('methods')[1].get('return_type'), 'void')
    self.assertEqual(self.code.get('methods')[2].get('return_type'), 'int')
    self.assertEqual(self.code.get('methods')[3].get('return_type'), 'double')
    self.assertEqual(self.code.get('methods')[4].get('return_type'), 'String')

  def test_method_return_value(self):
    expected_names = ['setup', 'draw', 'checkEdge', 'evenOdd', 'concatStrings']
    test_file = 'test_sketches/methods.pde'
    self.code = parse_student_code(test_file, expected_names)
    self.assertEqual(self.code.get('methods')[0].get('return_value'), '')
    self.assertEqual(self.code.get('methods')[1].get('return_value'), '')
    self.assertEqual(self.code.get('methods')[2].get('return_value'), '')
    self.assertEqual(self.code.get('methods')[3].get('return_value'), '')
    self.assertEqual(self.code.get('methods')[4].get('return_value'), 's1 + s2')

  def test_method_code(self):
    test_file = 'test_sketches/methods.pde'
    self.code = parse_student_code(test_file)
    expected_method_code_1 = ['void setup() {', 'size(200, 200);', 'noStroke();', '}']
    expected_method_code_2 = ['void draw() {', 'background(0);', 'fill("red");', 'circle(xpos, height/2, 50);', 'xpos++;', 'checkEdge();', '}']
    self.assertEqual(self.code.get('methods')[0].get('code'), expected_method_code_1)
    self.assertEqual(self.code.get('methods')[1].get('code'), expected_method_code_2)

if __name__ == '__main__':
    unittest.main()