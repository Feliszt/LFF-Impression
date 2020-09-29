#include "../lib/json2.js"

/*
 -- load and read JSON
*/
function readJSON(file) {
    file.open("r");
    var data = file.read();
    file.close();
    data = JSON.parse(data);
    
    return data["tweets"];
}

 // load doc and items
var doc = app.activeDocument;
var curSpread = doc.layoutWindows[0].activeSpread;
var spreadItems = curSpread.allPageItems;

// load pdf preset
var myPDFExportPreset = app.pdfExportPresets.item("RAR_PDF_PRESET");

// setup folders
var savedPDFFolder  = "D:/PERSO/_CREA/rar/_DEV/VISUALS/rar_tweetPrint_ExtendScript/JSONtoPDFs/res/";
var inputFolder         = "D:/PERSO/_CREA/rar/_DEV/DATA/log/";

// load json
tweets =  readJSON (File(inputFolder + "savedTweets_json.json"));

var distObjects = [];
var tweet_text;
// collect all relevant objects in distObjects
for (var i = 0; i < spreadItems.length; i += 1) {
  var si = spreadItems[i];

  // skip if itemLayer is locked
  if (si.itemLayer.locked) continue;

  // skip if item is not a textFrame
  if (!(si instanceof TextFrame)) continue;
  
  if(si.name === "tweet_text") tweet_text = si;

  /*
  // skip if item is anchored
  if (si.name !== "tweet_text" && si.name !== "tweet_date" && si.name !== "tweet_hour" ) continue;
  distObjects.push(si);
  */
};


for(var i = 0; i < tweets.length; i+= 1) {
        // change text
        tweet_text.contents = tweets[i]["text"];
        
        // print to pdf
        var filename = tweets[i]["id_str"] + ".pdf";
        $.writeln(filename);
        app.activeDocument.exportFile(ExportFormat.pdfType, File(savedPDFFolder + filename), false, myPDFExportPreset);
}
/*
// group all collected objects to center them, then ungroup
var distGroup = curSpread.groups.add(distObjects);
doc.align([distGroup], AlignOptions.HORIZONTAL_CENTERS, AlignDistributeBounds.SPREAD_BOUNDS);
distGroup.ungroup();

// distribute all objects horizontally
doc.distribute(distObjects, DistributeOptions.HORIZONTAL_CENTERS, AlignDistributeBounds.ITEM_BOUNDS);
*/

/*
    //
for(var i = 0; i < tweets.length; i++) {
        //$.writeln(tweets[i]["text"]);
 }

// loop through all text frames
var textFrames = layer.textFrames;
for(var j = 0; j < textFrames.count(); j++) {
    var textFrame = textFrames[j];
    //  $.writeln(textFrame.name);
   
   // if tweett_ext
    if(textFrame.name == "tweet_text") {
        textFrame.contents = tweets[0]["text"];   
    }
 }
 */
