import unittest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ppc import parse_student_code
import qpc

class TestQPC(unittest.TestCase):
  
  def test_get_code(self):
    expected = ['void setup() {', '  size(200, 200); ', '}', 'void draw() {', '  background(0);', '}']
    test_file = 'test_sketches/comments.pde'
    self.code = parse_student_code(test_file)
    actual = qpc.get_code(self.code)
    self.assertEqual(actual, expected)

  def test_get_full_code(self):
    expected = ['/*multiline \n', 'comment 1*/\n', '/*\n', 'multiline comment 2\n', '*/\n', '\n', 'void setup() {\n', '  /* multiline comment on a single line */\n', '  size(200, 200); //trailing comment\n', '}\n', '\n', 'void draw() {\n', '  // leading comment\n', '  background(0);\n', '}']
    test_file = 'test_sketches/comments.pde'
    self.code = parse_student_code(test_file)
    actual = qpc.get_full_code(self.code)
    self.assertEqual(actual, expected)

  def test_has_global_variable(self):
    test_file = 'test_sketches/global_variables.pde'
    self.code = parse_student_code(test_file)
    self.assertTrue(qpc.has_global_variable(self.code, 'int age;'))
    self.assertTrue(qpc.has_global_variable(self.code, 'float x = 7.2;'))
    self.assertTrue(qpc.has_global_variable(self.code, 'String name = "Calvin";'))

  def test_get_global_variables(self):
    expected = ['int age;', 'float x = 7.2;', 'String name = "Calvin";']
    test_file = 'test_sketches/global_variables.pde'
    self.code = parse_student_code(test_file)
    actual = qpc.get_global_variables(self.code)
    expected.sort()
    self.assertEqual(actual, expected)

  def test_get_method(self):
    expected = {'return_type': 'double', 'name': 'evenOdd', 'parameters': ['int num'], 'code': ['double evenOdd(int num) {', 'if (num % 2 == 0) {', 'println("Even");', '} else {', 'println("Odd");', '}', '}'], 'conditionals': [{'code': ['if (num % 2 == 0) {', 'println("Even");', '} else {', 'println("Odd");', '}'], 'true_branch': ['if (num % 2 == 0) {', 'println("Even");'], 'false_branch': ['} else {', 'println("Odd");', '}']}], 'loops': [], 'return_value': ''}
    test_file = 'test_sketches/methods.pde'
    expected_methods = ['setup', 'draw', 'checkEdge', 'evenOdd', 'concatStrings']
    self.code = parse_student_code(test_file, sketch_methods=expected_methods)
    actual = qpc.get_method(self.code, 'evenOdd')
    self.assertEqual(actual, expected)

  def test_has_method_name(self):
    test_file = 'test_sketches/methods.pde'
    expected_methods = ['setup', 'draw', 'checkEdge', 'evenOdd', 'concatStrings']
    self.code = parse_student_code(test_file, sketch_methods=expected_methods)
    self.assertTrue(qpc.method_has_name(self.code, 'setup'))
    self.assertTrue(qpc.method_has_name(self.code, 'draw'))
    self.assertTrue(qpc.method_has_name(self.code, 'checkEdge'))
    self.assertTrue(qpc.method_has_name(self.code, 'evenOdd'))
    self.assertTrue(qpc.method_has_name(self.code, 'concatStrings'))

  def test_get_method_code(self):
    test_file = 'test_sketches/methods.pde'
    expected_methods = ['setup', 'draw', 'checkEdge', 'evenOdd', 'concatStrings']
    self.code = parse_student_code(test_file, sketch_methods=expected_methods)
    expected = ['void draw() {', 'background(0);', 'fill("red");', 'circle(xpos, height/2, 50);', 'xpos++;', 'checkEdge();', '}']
    actual = qpc.get_method_code(self.code, 'draw')
    self.assertEqual(actual, expected)

  def test_get_method_parameters(self):
    test_file = 'test_sketches/methods.pde'
    expected_methods = ['setup', 'draw', 'checkEdge', 'evenOdd', 'concatStrings']
    self.code = parse_student_code(test_file, sketch_methods=expected_methods)
    expected_1 = ['']
    expected_2 = ['int num']
    expected_3 = ['String s1', 'String s2']
    actual_1 = qpc.get_method_parameters(self.code, 'setup')
    actual_2 = qpc.get_method_parameters(self.code, 'evenOdd')
    actual_3 = qpc.get_method_parameters(self.code, 'concatStrings')
    self.assertEqual(actual_1, expected_1)
    self.assertEqual(actual_2, expected_2)
    self.assertEqual(actual_3, expected_3)

  def test_get_method_return_type(self):
    test_file = 'test_sketches/methods.pde'
    expected_methods = ['setup', 'draw', 'checkEdge', 'evenOdd', 'concatStrings']
    self.code = parse_student_code(test_file, sketch_methods=expected_methods)
    expected_1 = 'void'
    expected_2 = 'void'
    expected_3 = 'int'
    expected_4 = 'double'
    expected_5 = 'String'
    actual_1 = qpc.get_method_return_type(self.code, 'setup')
    actual_2 = qpc.get_method_return_type(self.code, 'draw')
    actual_3 = qpc.get_method_return_type(self.code, 'checkEdge')
    actual_4 = qpc.get_method_return_type(self.code, 'evenOdd')
    actual_5 = qpc.get_method_return_type(self.code, 'concatStrings')
    self.assertEqual(actual_1, expected_1)
    self.assertEqual(actual_2, expected_2)
    self.assertEqual(actual_3, expected_3)
    self.assertEqual(actual_4, expected_4)
    self.assertEqual(actual_5, expected_5)

  def test_get_method_return_value(self):
    test_file = 'test_sketches/methods.pde'
    expected_methods = ['setup', 'draw', 'checkEdge', 'evenOdd', 'concatStrings']
    self.code = parse_student_code(test_file, sketch_methods=expected_methods)
    expected_1 = ''
    expected_2 = ''
    expected_3 = ''
    expected_4 = ''
    expected_5 = 's1 + s2'
    actual_1 = qpc.get_method_return_value(self.code, 'setup')
    actual_2 = qpc.get_method_return_value(self.code, 'draw')
    actual_3 = qpc.get_method_return_value(self.code, 'checkEdge')
    actual_4 = qpc.get_method_return_value(self.code, 'evenOdd')
    actual_5 = qpc.get_method_return_value(self.code, 'concatStrings')
    self.assertEqual(actual_1, expected_1)
    self.assertEqual(actual_2, expected_2)
    self.assertEqual(actual_3, expected_3)
    self.assertEqual(actual_4, expected_4)
    self.assertEqual(actual_5, expected_5)

  def test_get_method_loops(self):
    test_file = 'test_sketches/array_rect_ellipse.pde'
    expected_methods = ['setup', 'draw', 'mousePressed', 'mouseDragged', 'mouseReleased']
    self.code = parse_student_code(test_file, sketch_methods=expected_methods)
    expected = [{'type': 'for', 'code': ['for(int i=0; i<fcX.length; i++){', 'fill(colors[i]);', 'if(shapes[i] == 1){', 'rect(fcX[i], fcY[i], scX[i], scY[i]);', '}else if(shapes[i] == 2){', 'ellipse(fcX[i], fcY[i], scX[i], scY[i]);', '}', '}']}]
    actual = qpc.get_method_loops(self.code, 'mouseDragged')
    self.assertEqual(actual, expected)

  def test_method_has_for_loop(self):
    test_file = 'test_sketches/for_loop.pde'
    self.code = parse_student_code(test_file)
    self.assertTrue(qpc.method_has_for_loop(self.code, 'draw'))
    self.assertFalse(qpc.method_has_for_loop(self.code, 'setup'))

  def test_method_has_while_loop(self):
    test_file = 'test_sketches/while_loop.pde'
    self.code = parse_student_code(test_file)
    self.assertTrue(qpc.method_has_while_loop(self.code, 'draw'))
    self.assertFalse(qpc.method_has_while_loop(self.code, 'setup'))

  def test_method_has_conditional(self):
    test_file = 'test_sketches/methods.pde'
    expected_methods = ['setup', 'draw', 'checkEdge', 'evenOdd', 'concatStrings']
    self.code = parse_student_code(test_file, sketch_methods=expected_methods)
    self.assertFalse(qpc.method_has_conditional(self.code, 'setup'))
    self.assertFalse(qpc.method_has_conditional(self.code, 'draw'))
    self.assertTrue(qpc.method_has_conditional(self.code, 'checkEdge'))
    self.assertTrue(qpc.method_has_conditional(self.code, 'evenOdd'))
    self.assertFalse(qpc.method_has_conditional(self.code, 'concatStrings'))

  def test_has_class_name(self):
    test_file = 'test_sketches/class_example.pde'
    class_methods = ['update']
    self.code = parse_student_code(test_file, class_methods=class_methods)
    self.assertTrue(qpc.has_class_name(self.code, 'HLine'))

  def test_get_class(self):
    test_file = 'test_sketches/class_example.pde'
    class_methods = ['update']
    self.code = parse_student_code(test_file, class_methods=class_methods)
    expected = {'name': 'HLine', 'code': ['class HLine {', '  float ypos, speed;', '  HLine (float y, float s, String s1, int num) {', '    ypos = y;', '    speed = s;', '  }', '  void update() {', '    ypos += speed;', '    if (ypos > height) {', '      ypos = 0;', '    }', '    line(0, ypos, width, ypos);', '  }', '}'], 'methods': [{'return_type': 'void', 'name': 'update', 'parameters': [''], 'code': ['void update() {', 'ypos += speed;', 'if (ypos > height) {', 'ypos = 0;', '}', 'line(0, ypos, width, ypos);', '}'], 'conditionals': [{'code': ['if (ypos > height) {', 'ypos = 0;', '}'], 'true_branch': ['if (ypos > height) {', 'ypos = 0;', '}'], 'false_branch': ''}], 'loops': [], 'return_value': ''}], 'constructor': {'code': ['HLine (float y, float s, String s1, int num) {', 'ypos = y;', 'speed = s;', '}'], 'parameters': ['float y', 'float s', 'String s1', 'int num']}, 'attributes': ['float ypos, speed;']}
    actual = qpc.get_class(self.code)
    self.assertEqual(expected, actual)

  def test_get_constructor(self):
    test_file = 'test_sketches/class_example.pde'
    class_methods = ['update']
    self.code = parse_student_code(test_file, class_methods=class_methods)
    expected = {'code': ['HLine (float y, float s, String s1, int num) {', 'ypos = y;', 'speed = s;', '}'], 'parameters': ['float y', 'float s', 'String s1', 'int num']}
    actual = qpc.get_constructor(self.code)
    self.assertEqual(expected, actual)

  def test_get_constructor_parameters(self):
    test_file = 'test_sketches/class_example.pde'
    class_methods = ['update']
    self.code = parse_student_code(test_file, class_methods=class_methods)
    expected = ['float y', 'float s', 'String s1', 'int num']
    actual = qpc.get_constructor_parameters(self.code)
    self.assertEqual(expected, actual)

  def test_get_constructor_code(self):
    test_file = 'test_sketches/class_example.pde'
    class_methods = ['update']
    self.code = parse_student_code(test_file, class_methods=class_methods)
    expected = ['HLine (float y, float s, String s1, int num) {', 'ypos = y;', 'speed = s;', '}']
    actual = qpc.get_constructor_code(self.code)
    self.assertEqual(expected, actual)

  def test_has_class_method(self):
    test_file = 'test_sketches/class_example.pde'
    class_methods = ['update']
    self.code = parse_student_code(test_file, class_methods=class_methods)
    self.assertTrue(qpc.has_class_method(self.code, 'update'))
    self.assertFalse(qpc.has_class_method(self.code, 'setup'))

  def test_has_attribute(self):
    test_file = 'test_sketches/class_example.pde'
    class_methods = ['update']
    self.code = parse_student_code(test_file, class_methods=class_methods)
    self.assertTrue(qpc.has_attribute(self.code, 'float ypos, speed;'))
    self.assertFalse(qpc.has_attribute(self.code, 'float ypos;'))

  def test_get_attributes(self):
    test_file = 'test_sketches/class_example.pde'
    class_methods = ['update']
    self.code = parse_student_code(test_file, class_methods=class_methods)
    expected = ['float ypos, speed;']
    actual = qpc.get_attributes(self.code)
    self.assertEqual(expected, actual)

  def test_get_method_for_loops(self):
    test_file = 'test_sketches/loops.pde'
    self.code = parse_student_code(test_file)
    actual = qpc.get_method_for_loops(self.code, 'draw')
    expected = [['for(int i = 0; i < 10; i++) {', 'println("For loop #1");', '}'], ['for(int j = 0; j < 20; j++) {', 'println("For loop #2");', '}']]
    self.assertEqual(expected, actual)
    self.assertEqual(expected[0], qpc.get_method_for_loops(self.code, 'draw', 0))
    self.assertEqual(expected[1], qpc.get_method_for_loops(self.code, 'draw', 1))

  def test_get_method_while_loops(self):
    test_file = 'test_sketches/loops.pde'
    self.code = parse_student_code(test_file)
    actual = qpc.get_method_while_loops(self.code, 'setup')
    expected = [['while (counter1 < 10) {', 'println("While loop #1");', 'counter1++;', '}'], ['while (counter2 < 20) {', 'println("While loop #2");', 'counter2++;', '}']]
    self.assertEqual(expected, actual)
    self.assertEqual(expected[0], qpc.get_method_while_loops(self.code, 'setup', 0))
    self.assertEqual(expected[1], qpc.get_method_while_loops(self.code, 'setup', 1))

  def test_get_method_conditionals(self):
    pass

if __name__ == '__main__':
    unittest.main()