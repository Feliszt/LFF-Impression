const ipc = require('electron').ipcRenderer

// write tweet
tweetText= "Ceux qui mange pas la cro\u00fbte des pizzas jles hais";
var tweetEl = document.getElementById("tweet-text");
tweetEl.textContent = tweetText;
twemoji.parse(document.body);

ipc.send('print-to-pdf');
