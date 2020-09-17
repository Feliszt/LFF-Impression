#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
	// setup json
	jsonData = ofLoadJson("D:/PERSO/_CREA/rar/_DEV/PYTHON/_TWEETS_AND_DATA/fromChecker/06-08-2020_checked.json");
	numTweets = jsonData["tweets"].size();
	

	// font
	ofTrueTypeFontSettings settings("D:/PERSO/_FONTS/twemoji-color-font-ttf/TwitterColorEmoji-SVGinOT.ttf", 15);
	settings.antialiased = true;
	settings.dpi = 300;
	settings.direction = OF_TTF_LEFT_TO_RIGHT;
	settings.addRanges(ofAlphabet::Emoji);
	font.load(settings);	
	

	// gui
	gui.setup();

	// utils
	screen = ofVec2f(ofGetWidth(), ofGetHeight());
	center = screen * 0.5;
}

//--------------------------------------------------------------
void ofApp::update(){
	// utils
	mouse.set(ofGetMouseX(), ofGetMouseY());
}

//--------------------------------------------------------------
void ofApp::draw(){
	//
	ofBackground(253);

	//
	ofSetColor(50);
	font.drawString((string) currTweet, 10, 100);

	// gui
	if (showDebug) {
		// gui
		gui.draw();	

		// info
		ofDrawBitmapStringHighlight(to_string(ofGetFrameRate()) + " fps.", 10, ofGetHeight() - 10);
	}
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){
	if (key == ' ') showDebug = !showDebug;
	if (key == 'q') currTweetInd = currTweetInd <= 0 ? 0 : currTweetInd - 1;
	if (key == 'd') currTweetInd = currTweetInd >= numTweets-1 ? 0 : currTweetInd + 1;
	if (key == 'q' || key == 'd') {
		

		currTweet_string = jsonData["tweets"][currTweetInd]["text"];
		currTweet_u32.clear();
		for (unsigned char c : currTweet_string) { currTweet_u32 += c; }

		for (const auto& c : currTweet_u32)
			std::wcout << static_cast<char>(c);
	}
	if (key == '1') state = 1;
	if (key == '2') state = 2;
}
