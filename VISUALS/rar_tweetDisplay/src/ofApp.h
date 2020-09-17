#pragma once

#include "ofMain.h"
#include "ofxGui.h"

class ofApp : public ofBaseApp{

	public:
		void setup();
		void update();
		void draw();
		void keyPressed(int key);

		// data
		ofJson				jsonData;
		std::u32string		currTweet_u32;
		string				currTweet_string;
		int					currTweetInd;
		int					numTweets;

		// text
		ofTrueTypeFont	font;

		// gui
		ofxPanel		gui;

		// utils
		bool			showDebug = true;
		ofVec2f			mouse, screen, center;
		int				state = 1;
};
