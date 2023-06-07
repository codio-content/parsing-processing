/* Declare four global 1D arrays to store the 2 corners for a shape:
firstCornerX, firstCornerY, secondCornerX
secondCornerY - simplicity's sake using fcX, fcY, scX, scY
*/
float[] fcX = {}; //this is to store x1 info for all shapes
float[] fcY = {}; //this is to store y1 info for all shapes
float[] scX = {}; //this is to store x2 info for all shapes
float[] scY = {}; //this is to store y2 info for all shapes
color[] colors = {}; //this is to store color info for a shape
int[] shapes = {}; //this is the store the shape type

//Declare 2 variables: startX, startY.
float startX, startY; 
//these are to store x1, y1 for current shape
//  as we do not have x2, y2 of the current shape,
//  we are not putting these into the array yet.

color currentColor;
//just like how we store starting positions of current shape
//  we need another variable to hold/store color of the shape being drawn

int currentShape;
//just like currentColor, we need another variable to hold/store/remember
//    the shape preferred by the user for shape they are dragging currently

void setup(){
  size(1000, 1000);
  rectMode(CORNERS); 
  ellipseMode(CORNERS);
  //enables use of mouse positions to figure out diagonal opposite corners
  //  otherwise we have to do the math based on mouse positions 
}
void draw(){
}
void mousePressed(){
  //storing info for current rectangle that is being drawn
  //hold the current mouse positions as the first corner for the current rectangle
  startX = mouseX;
  startY = mouseY;
  currentColor = color(random(255), random(255), random(255));
  //user pressing left means rectangle; otherwise user wants ellipse 
  if(mouseButton == LEFT){
    currentShape = 1;
  }else{
    currentShape = 2;
  }
}
void mouseDragged(){
  background(255); //to clear draglines
  
  //clearing drag lines means that rects drawn earlier would ALSO be erased
  //as we remembered aspects/info about every rect inside the parallel arrays,
  //    we use a loop and draw those rectangles first
  //    this way the order of rectangles will be maintained.
  
  //Draw all stored rectangles using the values stored in the 4 arrays (Use a loop for this).
  for(int i=0; i<fcX.length; i++){
    //fill up with color info of the i-th rectangle
    fill(colors[i]); 
    //positional info of i-th rectangle is found in the i-th index the parallel arrays
    //use that to draw the i-th rectangle
    if(shapes[i] == 1){
      rect(fcX[i], fcY[i], scX[i], scY[i]);    
    }else if(shapes[i] == 2){
      ellipse(fcX[i], fcY[i], scX[i], scY[i]);    
    }
  }
  //now we need to draw current rectangle using the values in variables  
  fill(currentColor); //get the current rectangle's color
  if(currentShape == 1){
    rect(startX, startY, mouseX, mouseY);
  }else if(currentShape == 2){
      ellipse(startX, startY, mouseX, mouseY);    
    }
}
void mouseReleased(){
  //now that user decided on the second diagonal corner
  //  we need to register the values in the variables into appropriate arrays
  //  this way, the current shape can become part of the older shapes 
  //  when user decides to draw another shapes.
  
  fcX = append(fcX, startX);  //startX is x1 of current shape that was just drawn
  fcY = append(fcY, startY);  //startY is y1 of current shape that was just drawn
  scX = append(scX, mouseX);  //mouseX is x2 of current shape that was just drawn
  scY = append(scY, mouseY);  //mouseY is y2 of current shape that was just drawn
  
  colors = append(colors, currentColor); 
    //currentColor has color of shape that was just drawn
  shapes = append(shapes, currentShape);
    //currentShape stands for the shape that was just drawn
}