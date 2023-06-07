int counter 1 = 0;
int counter 2 = 0;

void setup() {
  while (counter1 < 10) {
    println("While loop #1");
    counter1++;
  }

  while (counter2 < 20) {
    println("While loop #2");
    counter2++;
  }
}

void draw() {
  for(int i = 0; i < 10; i++) {
    println("For loop #1");
  }

  for(int j = 0; j < 20; j++) {
    println("For loop #2");
  }
}