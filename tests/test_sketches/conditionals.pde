void setup() {
  if (xpos > width) {
    xpos = 0;
  }
}

void draw() {
  if (num % 2 == 0) {
    println("Even");
  } else {
    println("Odd");
  }

  if (a < b) {
    printlin("less");
  } else if (a > b) {
    println("greater");
  } else {
    println("equal");
  }
  println("out of conditional");
}