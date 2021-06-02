//
const fs = require('fs');
const path = require('path');
const readline = require('readline');

function loadSavedLog (logFile) {
  // read log of saved tweets
  var rd = readline.createInterface({
      input: fs.createReadStream(logFile),
      output: process.stdout,
      console: false
  });

  // on line, create list
  rd.on('line', function(line) {
      //var id = line.split('\t')[1];
      var els = line.split(' ');
      if(els.length > 1) {
        idsList.push(els[1]);
      }
  });
}

function loadFileNames (folder) {
    return new Promise(function(resolve, reject) {
        fs.readdir(folder, function(err, filenames){
            if (err)
                reject(err);
            else
                var files = []
                filenames.forEach(file => {
                  if (path.extname(file) == ".json")
                    files.push(file);
                })
                resolve(files);
        });
    });
};

function loadTweets(fileName) {
  // set current filename
  currentFileName = fileName;

  // change button element to fileName
  document.getElementById('buttonFiles').innerHTML = fileName;

  // load json
  let rawJSON = fs.readFileSync(tweetFolder + fileName);
  let tweetDATA = JSON.parse(rawJSON);

  // make html element and append it to page
  tweetList = makeUL(tweetDATA["tweets"]);
  document.getElementById('tweetList').innerHTML = '';
  document.getElementById('tweetList').appendChild(tweetList);

  // check if there are some saved tweets
  for(var i = 0; i < idsList.length; i++) {
    //console.log(idsList[i]);
    var elFromId = document.getElementById(idsList[i]);
    if(elFromId !== null){
      elFromId.style.backgroundColor = "rgba(62, 140, 38, 0.5)";
    }
  }

  // parse emojis
  twemoji.parse(document.body);
}

function saveFunc(id) {
  //console.log(id);

  // if id in list, return now
  if(idsList.includes(id)) {
    console.log("id [" + id + "] already saved.");
    return;
  }

  // green background
  document.getElementById(id).style.backgroundColor = "rgba(62, 140, 38, 0.5)";

  // save to stream
  var dataToAppend = currentFileName + " " + id + "\n";
  //stream.write(dataToAppend);
  console.log("saving id [" + id + "].");

  //
  fs.appendFileSync(eventLogFile, dataToAppend);

  // save to list
  idsList.push(id);
}

function makeUL(array) {
    // Create the list element:
    var tweetsList = document.createElement('ul');

    for (var i = 0; i < array.length; i++) {
        // Create the list item:
        var tweetInstance = document.createElement('li');
        tweetInstance.setAttribute("class", "tweet-instance");
        tweetInstance.setAttribute("id", array[i]["id_str"]);

        // set link
        var tweetSave = document.createElement('a');
        tweetSave.setAttribute("href", "javascript:saveFunc('" + array[i]["id_str"] + "');" );
        tweetSave.setAttribute("class", "tweet-save");
        tweetInstance.appendChild(tweetSave);

        // set text
        var tweetText = document.createElement('div');
        tweetText.setAttribute("class", "tweet-text");
        tweetText.appendChild(document.createTextNode(array[i]["text"]));
        tweetSave.appendChild(tweetText);

        // set date
        var tweetDate = document.createElement('div');
        tweetDate.setAttribute("class", "tweet-date");
        tweetDate.appendChild(document.createTextNode(array[i]["created_at"]));
        tweetSave.appendChild(tweetDate);

        // set button
        var tweetLink = document.createElement('a');
        tweetLink.innerHTML = "see tweet";
        tweetLink.setAttribute("class", "goToTwitter");
        tweetLink.setAttribute("href", "https://twitter.com/" + array[i]["user_screen_name"] + "/status/" + array[i]["id_str"]);
        tweetSave.appendChild(tweetLink);

        // Add it to the list:
        tweetsList.appendChild(tweetInstance);
    }

    // Finally, return the constructed list:
    return tweetsList;
}

// get list of files
var eventName = "videoPDF";
var tweetFolder = "./../../DATA/fromChecker/";
var eventsFolder = "./../../DATA/events/";
eventLogFile = eventsFolder + eventName + "/" + eventName + "_tweetsLog.txt";
var currentFileName = "";
var listOfFiles = []
var idsList = [];

// load tweets of first file to start
loadFileNames(tweetFolder).then((files) => {
  // set drop down list
  var dropdownlist = document.getElementById('dropdown-list-files');
  dropdownlist.innerHTML = '';
  files.forEach(file => {
    // set display name
    var fileDisplay = file.split('_');
    fileDisplay = fileDisplay[0];

    // create dom element
    var listElTemp = document.createElement('a');
    listElTemp.innerHTML = fileDisplay;
    listElTemp.setAttribute("class", "tweetFileLink");
    listElTemp.setAttribute("onclick", "loadTweets('" + file + "');");
    dropdownlist.appendChild(listElTemp);
  })

  // load log of saved tweets
  loadSavedLog(eventLogFile);

  // load first file
  //loadTweets(files[0]);
}).catch((error) => console.log(error));


// create append stream
var stream = fs.createWriteStream(eventLogFile, {flags:'a'});
