//
const fs = require('fs');
const path = require('path');
const readline = require('readline');

// get a random tweet from the list of filenames
function getRandomTweet(_fileNames) {
  // random file
  currFile = fileNames[Math.floor(Math.random() * fileNames.length)];

  // open file and load json
  var lines = fs.readFileSync(tweetFolder + currFile, 'utf-8').split('\n').filter(Boolean);
  var tweetJSON = lines[Math.floor(Math.random()*lines.length)];
  var currTweet = JSON.parse(tweetJSON);

  //
  foundAnUnsavableTweet = unsavableTweets.includes(currTweet["id_str"]);

  // check if tweet is in unsavable list
  var tweetEl = document.getElementById("tweet");
  if(foundAnUnsavableTweet) {
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
  var dataToAppend = currFile + '\t' + currTweet["id_str"] + "\n";

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
var eventName = "PLEIADES2021";
var eventTweetNum = 540;
var tweetFolder = "./../../DATA/tweetsChecked/";
var eventsFolder = "./../../DATA/events/";
eventLogFile = eventsFolder + eventName + "/" + eventName + "_toPrint.txt";

// set logged tweets variables
var unsavableTweets = [];
var savedTweetsCount = 0;

//
currTweet = "";

// fetch all events in event folder
var events = fs.readdirSync(eventsFolder)
var i;
for (i = 0; i < events.length; i++) {
  var ev = events[i];



  // discard gitkeep and current event
  if(ev == ".gitkeep" || ev == "test" || ev == "event-template") {
    continue;
  }

  // for current event, we check the _toPrint.txt file
  var fileToAnalyse = "_toPrint.txt";
  var fileNameFull = eventsFolder + events[i] + "/" + events[i] + fileToAnalyse;
  if (ev == eventName) {
    fileToAnalyse = "_toPrint.txt";
    fileNameFull = eventsFolder + events[i] + "/" + events[i] + fileToAnalyse;
  }

  // load lines and init already saved tweets number
  var lines = fs.readFileSync(fileNameFull, 'utf-8').split('\n').filter(Boolean);
  if (ev == eventName) {
    savedTweetsCount = lines.length;
    document.getElementById('countInLog').innerHTML = savedTweetsCount;
  }

  // init unsavable tweets array
  for (j = 0; j < lines.length; j++) {
    unsavableTweets.push(lines[j].split('\t')[1]);
  }

  /*

    const readInterface = readline.createInterface({input: fs.createReadStream(fileNameFull), output: process.stdout, console: false });
    readInterface.on('line', function(line) {
        savedTweetsCount++;
        unsavableTweets.push(line.split('\t')[1]);
    });

    readInterface.on('close', function() {
      document.getElementById('countInLog').innerHTML = savedTweetsCount;
      loadFirstTweet();
    });

    continue;
  }

  // read file
  const readInterface = readline.createInterface({input: fs.createReadStream(fileNameFull), output: process.stdout, console: false });
  readInterface.on('line', function(line) {
      unsavableTweets.push(line.split('\t')[1]);
  });
  */
  loadFirstTweet();
}

console.log(unsavableTweets)

// create append stream
var stream = fs.createWriteStream(eventLogFile, {flags:'a'});

// set event name
document.getElementById('eventName').innerHTML = eventName;
