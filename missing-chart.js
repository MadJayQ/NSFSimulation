// require file system and jsdom
var fs = require('fs');

// require only anychart export module
var anychartExport = require('anychart-nodejs');

// define javascript string that represent code of chart creating
var chart = "var chart = anychart.pie([10, 20, 7, 18, 30]); chart.bounds(0, 0, 800, 600); chart.container('container'); chart.draw()";

// generate PDF image and save it to a file
anychartExport.exportTo(chart, 'pdf').then(function(image) {
  fs.writeFile('anychart.pdf', image, function(fsWriteError) {
    if (fsWriteError) {
      console.log(fsWriteError);
    } else {
      console.log('Complete');
    }
  });
}, function(generationError) {
  console.log(generationError);
});