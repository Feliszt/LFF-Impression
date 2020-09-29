#include "../lib/json2.js"

/*
  -- main function  
*/
function main(){   
    // load pdf preset
    var myPDFExportPreset = app.pdfExportPresets.item("RAR_PDF_PRESET");

    // load json
    tweets =  readJSON (File("D:/PERSO/_CREA/rar/_DEV/DATA/fromChecker/06-08-2020_checked.json"));
    
    //
	if (app.documents.length != 0){
        var doc = app.activeDocument;
        var layers = doc.layers;
        var layerNames = "";
        for(var i = 0; i < layers.count(); i++) {
            var l = layers[i];
            var textFrames = l.textFrames;
            
            for(var j = 0; j < textFrames.count(); j++) {
                var t = textFrames[j];
                if(t.name == "TextBox1") {
                    t.contents = tweets[0]["text"];   
                 }
                layerNames += t.name + "\n";
             }
            
         }
     }
 }

/*
 -- load and read JSON
*/
function readJSON(file) {
    file.open("r");
    var data = file.read();
    file.close();
    data = JSON.parse(data);
    
    return data["tweets"];
}


main();