String currentPath, fullImagePath;
String imagePath = "/../../DATA/pdfs_to_jpegs/";
String[] fileNames;
PImage img;
ArrayList<PImage> imgs = new ArrayList<PImage>();

void setup() {
  // populate list of file names
  currentPath = sketchPath();  
  fullImagePath = currentPath + imagePath;
  fileNames = listFileNames(fullImagePath);
  
  // load all images
  for (int i = 0; i < fileNames.length; i++) {
   //imgs.add(loadImage(fullImagePath + fileNames[i])); 
  }
  
  //
  smooth(2);
  fullScreen();
}

void draw() {
  background(255);
  
  // pick random picture
  int randInd = int(random(0, fileNames.length));
  if (fileNames[randInd].equals(".gitkeep")) {
   return;
  }
  img = loadImage(fullImagePath + fileNames[randInd]);
  
  // get scale
  //float sc_w = (float) width / (float) imgs.get(randInd).width;
  float sc_w = (float) width / (float) img.width;
  //float sc_h = (float) height / (float) imgs.get(randInd).height;
  float sc_h = (float) height / (float) img.height;
  float sc = sc_w < sc_h ? sc_w : sc_h;
  
  // compute new size and offsets
  //float new_w = imgs.get(randInd).width * sc;
  float new_w = img.width * sc;
  //float new_h = imgs.get(randInd).height * sc;
  float new_h = img.height * sc;
  float offset_x = width * 0.5 - new_w * 0.5;
  float offset_y = height * 0.5 - new_h * 0.5;
  
  // display image
  pushMatrix();
  translate(offset_x, offset_y);
  scale(sc, sc);
  //image(imgs.get(randInd), 0, 0);
  image(img, 0, 0);
  popMatrix();
  
  //println("img width = " + img.width + "\tnew width = " + new_w + "\timg height = " + img.height + "\tnew height = " + new_h);  
  
  // pick random delay
  int timeDelay = int(random(0, 10));
  delay(timeDelay);
}

// This function returns all the files in a directory as an array of Strings  
String[] listFileNames(String dir) {
  File file = new File(dir);
  if (file.isDirectory()) {
    String names[] = file.list();
    return names;
  } else {
    // If it's not a directory
    return null;
  }
}
