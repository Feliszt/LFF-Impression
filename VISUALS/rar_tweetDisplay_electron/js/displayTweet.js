//
const fs = require('fs');
const path = require('path');

function saveFunc(id) {
  console.log(id);
  document.getElementById(id).style.backgroundColor = "rgba(62, 140, 38, 0.5)";
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
        tweetButton.setAttribute("onclick", "saveFunc('" + array[i]["id_str"] + "');");
        tweetInstance.appendChild(tweetButton);

        // Add it to the list:
        tweetsList.appendChild(tweetInstance);
    }

    // Finally, return the constructed list:
    return tweetsList;
}

// load json
let rawJSON = fs.readFileSync('./assets/10-08-2020_checked.json');
let tweetDATA = JSON.parse(rawJSON);

//console.log(tweetDATA);

// Add the contents of options[0] to #foo:
tweetList = makeUL(tweetDATA["tweets"]);
document.getElementById('tweetList').appendChild(tweetList);


//console.log(tweetDATA["tweets"][0]);

// parse emojis
twemoji.parse(document.body);
