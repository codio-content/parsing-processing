int limit = 10;
int index = 0;

void setup() {
  size(200, 200);
}

void draw() {
  background(0);

  while(index < limit) {
    println("Hello unit test!");
    index++;
  }
}