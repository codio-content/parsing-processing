void setup() {
  size(400, 400);
}

void draw() {
  background(55);
  if (5 < 7) {
    if (10 > 1) {
      println("Inner conditional");
    }
  } else {
    if (1 == 2) {
      println("Another inner conditional");
    } else if (true) {
      println("Last conditional");
    }
  }
}