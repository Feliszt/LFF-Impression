const ipc = require('electron').ipcRenderer

// write tweet
tweetText= "Il a vue la premi\u00e8re photo de ma story il a abandonn\u00e9 directement \ud83d\ude2d"
var tweetEl = document.getElementById("tweet-text");
tweetEl.textContent = tweetText;
twemoji.parse(document.body);

ipc.send('print-to-pdf');
