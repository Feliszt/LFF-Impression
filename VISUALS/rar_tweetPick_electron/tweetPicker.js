//
const fs = require('fs');
const path = require('path');
const readline = require('readline');

// get a random tweet from the list of filenames
function getRandomTweet(_fileNames) {
  // random file
  currFile = fileNames[Math.floor(Math.random() * fileNames.length)];

  // open file and load json
  let rawJSON = fs.readFileSync(tweetFolder + currFile);
  let tweetDATA = JSON.parse(rawJSON)["tweets"];

  // get random tweet and change HTML data
  currTweet =  tweetDATA[Math.floor(Math.random() * tweetDATA.length)];

  //
  foundAnUnsavedTweet = unsavableTweets.includes(currTweet["id_str"]);

  // check if tweet is in unsavable list
  var tweetEl = document.getElementById("tweet");
  if(foundAnUnsavedTweet) {
     tweetEl.style.backgroundColor = "rgba(186, 86, 43, 0.5)";
   } else {
     tweetEl.style.backgroundColor = "rgba(255, 255, 255, 1.0)";
   }

  //
  document.getElementById('tweet-text').innerHTML = currTweet['text'];
  document.getElementById('tweet-date').innerHTML = currTweet['created_at'];
  var tweetLink =document.getElementById('tweet-link');
  tweetLink.setAttribute("href", "https://twitter.com/" + currTweet["user_screen_name"] + "/status/" + currTweet["id_str"]);

  // parse emojis
  twemoji.parse(document.body);
}

// function
async function loadFirstTweet() {
  // get file list
  fileNames = await loadFileNames(tweetFolder);

  //
  getRandomTweet(fileNames);
}

// discard current tweet
async function discardTweet() {
  //
  unsavableTweets.push(currTweet["id_str"]);

  //
  getRandomTweet(fileNames);
}

// save current tweet
async function saveTweet() {
  //
  unsavableTweets.push(currTweet["id_str"]);

  // save to stream
  var dataToAppend = currFile + " " + currTweet["id_str"] + "\n";

  //
  fs.appendFileSync(eventLogFile, dataToAppend);
  savedTweetsCount++;

  //
  document.getElementById('countInLog').innerHTML = savedTweetsCount;

  //
  getRandomTweet(fileNames);
}

function loadFileNames (_folder) {
    return new Promise(function(resolve, reject) {
        fs.readdir(_folder, function(err, filenames){
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

// get list of files
var eventName = "test";
var eventTweetNum = 540;
var tweetFolder = "./../../DATA/fromChecker/";
var eventsFolder = "./../../DATA/events/";
eventLogFile = eventsFolder + eventName + "/" + eventName + "_tweetsLog.txt";

// set logged tweets variables
var unsavableTweets = [];
var savedTweetsCount = 0;

//
currTweet = "";

// create append stream
var stream = fs.createWriteStream(eventLogFile, {flags:'a'});

// set event name
document.getElementById('eventName').innerHTML = eventName;

//
const readInterface = readline.createInterface({
    input: fs.createReadStream(eventLogFile),
    output: process.stdout,
    console: false
});

readInterface.on('line', function(line) {
    savedTweetsCount++;
    unsavableTweets.push(line.split(' ')[1]);
});

readInterface.on('close', function() {
  document.getElementById('countInLog').innerHTML = savedTweetsCount;
  loadFirstTweet();
});
