int xpos = 0;

void setup() {
  size(200, 200);
  noStroke();
}

void draw() {
  background(0);
  fill("red");
  circle(xpos, height/2, 50);
  xpos++;
  checkEdge();
}

int checkEdge() {
  if (xpos > width) {
    xpos = 0;
  }
}

double evenOdd(int num) {
  if (num % 2 == 0) {
    println("Even");
  } else {
    println("Odd");
  }
}

String concatStrings(String s1, String s2) {
  return s1 + s2;
}