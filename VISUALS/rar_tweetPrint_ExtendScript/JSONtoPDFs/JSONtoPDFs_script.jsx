﻿#include "../lib/json2.js"

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

//  set variables
var TWEET2INFO = 10.0;
var INTERINFO =  5.0;
var FONTMIN = 12;
var FONTMAX = 90;

// load pdf preset
var myPDFExportPreset = app.pdfExportPresets.item("RAR_PDF_PRESET");

// setup folders
var savedPDFFolder  = "D:/PERSO/_CREA/rar/_DEV/VISUALS/rar_tweetPrint_ExtendScript/JSONtoPDFs/res/";
var inputFolder         = "D:/PERSO/_CREA/rar/_DEV/DATA/log/";

// load json
tweets =  readJSON (File(inputFolder + "savedTweets_json.json"));

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
  if(si.name === "tweet_text")       tweet_text = si;
  if(si.name === "tweet_date")      tweet_date= si;
  if(si.name === "tweet_hour")      tweet_hour = si;
  if(si.name === "id")                    tweet_id = si;
  if(si.name === "page_size")        page_size = si;
};

// get page size
var temp  = page_size.geometricBounds;
var page_sz = [temp[3] - temp[1], temp[2] - temp[0]];

// log
$.writeln("Page size : [" + page_sz[0] + ", " + page_sz[1] + "]");

for(var i = 0; i < tweets.length; i+= 1) {
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
    var allH = tweet_text_sz[1];// + tweet_date_sz[1] + tweet_hour_sz[1] + TWEET2INFO + INTERINFO;
    var topY = (page_sz[1] - allH) / 2;
    
    // set tweet_text position
    tweet_text.geometricBounds = [topY, tweet_text_bounds[1], topY + tweet_text_sz[1], tweet_text_bounds[3]];
    topY = topY +  tweet_text_sz[1] + TWEET2INFO;
    
    // set tweet_date position
    tweet_date.geometricBounds = [topY, tweet_date_bounds[1], topY + tweet_date_sz[1], tweet_date_bounds[3]];
    topY = topY +  tweet_date_sz[1] + INTERINFO;
    
    // set tweet_hour position
    tweet_hour.geometricBounds = [topY, tweet_hour_bounds[1], topY + tweet_hour_sz[1], tweet_hour_bounds[3]];
    
    // print to pdf
    var filename = tweets[i]["id_str"] + ".pdf";
    $.writeln("Saving with name [" + filename + "]");
    app.activeDocument.exportFile(ExportFormat.pdfType, File(savedPDFFolder + filename), false, myPDFExportPreset);
}