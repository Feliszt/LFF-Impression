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
  // if id in list, return now
  if(idsList.includes(id)) {
    console.log("id [" + id + "] already saved.");
    return;
  }

  // green background
  document.getElementById(id).style.backgroundColor = "rgba(62, 140, 38, 0.5)";

  // save to stream
  stream.write(currentFileName + " " + id + "\n");
  console.log("saving id [" + id + "].");

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
        var tweetLink = document.createElement('a');
        tweetLink.setAttribute("href", "https://twitter.com/" + array[i]["user_screen_name"] + "/status/" + array[i]["id_str"]);
        tweetLink.setAttribute("class", "tweet-link");
        tweetInstance.appendChild(tweetLink);

        // set text
        var tweetText = document.createElement('div');
        tweetText.setAttribute("class", "tweet-text");
        tweetText.appendChild(document.createTextNode(array[i]["text"]));
        tweetLink.appendChild(tweetText);

        // set date
        var tweetDate = document.createElement('div');
        tweetDate.setAttribute("class", "tweet-date");
        tweetDate.appendChild(document.createTextNode(array[i]["created_at"]));
        tweetLink.appendChild(tweetDate);

        // set button
        var tweetButton = document.createElement('BUTTON');
        tweetButton.innerHTML = "save";
        tweetButton.setAttribute("class", "saveButton");
        tweetButton.setAttribute("onclick", "saveFunc('" + array[i]["id_str"] + "');");
        tweetInstance.appendChild(tweetButton);

        // Add it to the list:
        tweetsList.appendChild(tweetInstance);
    }

    // Finally, return the constructed list:
    return tweetsList;
}

// get list of files
var tweetFolder = "./../../../DATA/fromChecker/";
var logFileName = "./../../../DATA/log/savedTweets.txt";
var currentFileName = "";
var listOfFiles = []
var idsList = [];

// load tweets of first file to start
loadFileNames(tweetFolder).then((files) => {
  // set drop down list
  var dropdownlist = document.getElementById('dropdown-list');
  dropdownlist.innerHTML = '';
  files.forEach(file => {
    var listElTemp = document.createElement('a');
    listElTemp.innerHTML = file;
    listElTemp.setAttribute("class", "tweetFileLink");
    listElTemp.setAttribute("onclick", "loadTweets('" + file + "');");
    dropdownlist.appendChild(listElTemp);
  })

  // load log of saved tweets
  loadSavedLog(logFileName);

  // load first file
  loadTweets(files[0]);
}).catch((error) => console.log(error));


// create append stream
var stream = fs.createWriteStream("./assets/savedTweets.txt", {flags:'a'});
