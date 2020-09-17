//
const fs = require('fs');
const path = require('path');

function makeUL(array) {
    // Create the list element:
    var tweetsList = document.createElement('ul');

    for (var i = 0; i < array.length; i++) {
        // Create the list item:
        var tweetInstance = document.createElement('li');
        tweetInstance.setAttribute("id", "tweet-instance");

        // set link
        var tweetLink = document.createElement('a');
        tweetLink.setAttribute("href", "https://twitter.com/" + array[i]["user_screen_name"] + "/status/" + array[i]["id_str"]);
        tweetLink.setAttribute("class", "tweet-link");
        tweetInstance.appendChild(tweetLink);

        // set text
        var tweetText = document.createElement('div');
        tweetText.setAttribute("id", "tweet-text");
        tweetText.appendChild(document.createTextNode(array[i]["text"]));
        tweetLink.appendChild(tweetText);

        // set date
        var tweetDate = document.createElement('div');
        tweetDate.setAttribute("id", "tweet-date");
        tweetDate.appendChild(document.createTextNode(array[i]["created_at"]));
        tweetLink.appendChild(tweetDate);

        // Add it to the list:
        tweetsList.appendChild(tweetInstance);
    }

    // Finally, return the constructed list:
    return tweetsList;
}

// load json
let rawJSON = fs.readFileSync(path.resolve("assets", '10-08-2020_checked.json'));
let tweetDATA = JSON.parse(rawJSON);


// Add the contents of options[0] to #foo:
document.getElementById('tweetList').appendChild(makeUL(tweetDATA["tweets"]));
//console.log(tweetDATA["tweets"][0]);

// parse emojis
twemoji.parse(document.body);
