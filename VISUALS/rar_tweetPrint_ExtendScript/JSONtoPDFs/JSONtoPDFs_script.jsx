#include "../lib/json2.js"

//  set variables
var TWEET2INFO          = 10.0;
var INTERINFO             =  5.0;
var FONTMIN               = 12;
var FONTMAX              = 70;
var EVENTNAME           = "OE2020";
var PRINT_NORMAL      = true;
var PRINT_FLIPPED       = true;
var PRINT_BARE           = false;

/*
 -- load and read JSON
*/
function readJSON(_file) {
    _file.open("r");
    var data = _file.read();
    _file.close();
    data = JSON.parse(data);
    
    return data["tweets"];
}

/*
 -- map function
 -- takes a numer and maps it in range
 -- can clamp or not
*/
function map(_in, _inMin, _inMax, _outMin, _outMax, _clamp) {
    if(_inMin == _inMax) return null;
    if(_clamp && _in <= _inMin) return _outMax;
    if(_clamp && _in >= _inMax) return _outMax;
    var a = (_outMax - _outMin) / (_inMax - _inMin);
    var b = (_outMin * _inMax - _inMin * _outMax) / (_inMax - _inMin);
    return a * _in + b;
}

 // load doc and items
var doc = app.activeDocument;
var curSpread = doc.layoutWindows[0].activeSpread;
var spreadItems = curSpread.allPageItems;

// load pdf preset
var myPDFExportPreset = app.pdfExportPresets.item("RAR_PDF_PRESET");

// setup folders and files
var eventsFolder         = "D:/PERSO/_CREA/rar/_DEV/DATA/events/";
var eventFolder         = eventsFolder + EVENTNAME + "/";
var savedPDFFolder   = eventFolder + "pdfs/";
var fileTweetsFinal     = eventFolder + EVENTNAME + "_tweetsFinal.json";

// load json
tweets =  readJSON (File(fileTweetsFinal));

// init items variables
var tweet_text;
var tweet_date;
var tweet_hour;
var tweet_id;
var page_size;

// collect all relevant objects in distObjects
for (var i = 0; i < spreadItems.length; i += 1) {
  var si = spreadItems[i];

  // skip if itemLayer is locked
  if (si.itemLayer.locked) continue;
  
  // get elements
  if(si.name === "tweet_text")                              tweet_text = si;
  if(si.name === "tweet_date")                            tweet_date= si;
  if(si.name === "tweet_hour")                            tweet_hour = si;
  if(si.name === "tweet_id")                                tweet_id = si;
  if(si.name === "impression_nb_in_session")          impression_nb_in_session = si;
  if(si.name === "session_nb")                             session_nb = si;
  if(si.name === "impression_date")                     impression_date = si;
  if(si.name === "page_size")                              page_size = si;
};

// get page size
var temp  = page_size.geometricBounds;
var page_sz = [temp[3] - temp[1], temp[2] - temp[0]];

// log
$.writeln("Page size : [" + page_sz[0] + ", " + page_sz[1] + "]");

for(var i = 0; i < tweets.length; i+= 1) {
    //
    var index = parseInt(tweets[i]["printIndex"], 10);
    //if(tweets[i]["printed_at_date_saving"] !== "10-10-2020") continue;
    
    // log
    $.writeln("Processing [" + tweets[i]["id_str"] + "]");
    
    // compute font size depending on text length
    var tweetSize = tweets[i]["text"].length;
    var fontSize = Math.floor(map(tweetSize, 0, 280, FONTMAX, FONTMIN, true));
    tweet_text.parentStory.pointSize = fontSize;
    
    // log
    $.writeln("tweet size = " + tweetSize + "\tfont size = " + fontSize);
    
    // change contents
    tweet_text.contents = tweets[i]["text"];
    tweet_date.contents = tweets[i]["created_at_date_readable"];
    tweet_hour.contents = tweets[i]["created_at_hour_readable"];
    tweet_id.contents = tweets[i]["id_str"];
    impression_nb_in_session.contents = tweets[i]["printIndexPadded"];
    session_nb.contents = tweets[i]["sessionIndex"];
    impression_date.contents = tweets[i]["printed_at_date_readable"];    
    
    // create group
    var itemsToDistribute = [];
    itemsToDistribute.push (tweet_text);
    itemsToDistribute.push (tweet_date);
    itemsToDistribute.push (tweet_hour);
    
    // get size of items
    // tweet_text
    var tweet_text_bounds = tweet_text.geometricBounds;
    var tweet_text_sz = [tweet_text_bounds[3] - tweet_text_bounds[1], tweet_text_bounds[2] - tweet_text_bounds[0]];
    //  tweet_date
    var tweet_date_bounds = tweet_date.geometricBounds;
    var tweet_date_sz = [tweet_date_bounds[3] - tweet_date_bounds[1], tweet_date_bounds[2] - tweet_date_bounds[0]];
    // tweet_hour
    var tweet_hour_bounds = tweet_hour.geometricBounds;
    var tweet_hour_sz = [tweet_hour_bounds[3] - tweet_hour_bounds[1], tweet_hour_bounds[2] - tweet_hour_bounds[0]];
    
    // log
    $.writeln("[tweet_text]\twidth = " + tweet_text_sz[0] + "\theight = " + tweet_text_sz[1]);
    $.writeln("[tweet_date]\twidth = " + tweet_date_sz[0] + "\theight = " + tweet_date_sz[1]);
    $.writeln("[tweet_hour]\twidth = " + tweet_hour_sz[0] + "\theight = " + tweet_hour_sz[1]);
    
    // compute full height of those 3 elements and first y-position
    var allH = tweet_text_sz[1] ; //+ tweet_date_sz[1] + tweet_hour_sz[1] + TWEET2INFO + INTERINFO;
    var topY = (page_sz[1] - allH) / 2;
    
    // set tweet_text position
    tweet_text.geometricBounds = [topY, tweet_text_bounds[1], topY + tweet_text_sz[1], tweet_text_bounds[3]];
    topY = topY +  tweet_text_sz[1] + TWEET2INFO;
    
    // set tweet_date position
    tweet_date.geometricBounds = [topY, tweet_date_bounds[1], topY + tweet_date_sz[1], tweet_date_bounds[3]];
    topY = topY +  tweet_date_sz[1] + INTERINFO;
    
    // set tweet_hour position
    tweet_hour.geometricBounds = [topY, tweet_hour_bounds[1], topY + tweet_hour_sz[1], tweet_hour_bounds[3]];
    
    // set path and file name
    var filename = tweets[i]["printIndexPadded"] + "_" + tweets[i]["id_str"];
    var filePath = savedPDFFolder + tweets[i]["printed_at_date_saving"] + "/";
    
  
    // save normal pdf
    if(PRINT_NORMAL) {
        app.activeDocument.exportFile(ExportFormat.pdfType, File(filePath + filename + ".pdf"), false, myPDFExportPreset);
    }
    
    if(PRINT_FLIPPED) {
        // group content
        var spreadItemsArray = []
        spreadItemsArray.push(tweet_text);
        spreadItemsArray.push(tweet_date);
        spreadItemsArray.push(tweet_hour);
        spreadItemsArray.push(tweet_id);
        spreadItemsArray.push(impression_nb_in_session);
        spreadItemsArray.push(session_nb);
        spreadItemsArray.push(impression_date);
        var spreadItemsGroup = curSpread.groups.add(spreadItemsArray);
        
        // flip element
        spreadItemsGroup.rotationAngle  = 180;
        
        // save flipped pdf
        app.activeDocument.exportFile(ExportFormat.pdfType, File(filePath + filename + "_flipped.pdf"), false, myPDFExportPreset);
        
        // unflip element and ungroup
        spreadItemsGroup.rotationAngle  = 0;
        spreadItemsGroup.ungroup();
    
    }
    
    if(PRINT_BARE) {
        // hide certain elements to create a PDF that will be used in video
        impression_nb_in_session.visible = false;
        session_nb.visible = false;
        impression_date.visible = false;
        
        // print
        app.activeDocument.exportFile(ExportFormat.pdfType, File(filePath + filename + "_bare.pdf"), false, myPDFExportPreset);
        
        // unhide certain elements to create a PDF that will be used in video
        impression_nb_in_session.visible = true;
        session_nb.visible = true;
        impression_date.visible = true;
    }
    
    // debug
    $.writeln("Saving file at [" + filePath + "with name [" + filename + "]");
    //$.sleep(1000);
}