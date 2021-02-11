/* PBD_1: Richard DROGO & Audric MERLEY.
* NodeJs Server allowing to retrieve the information from the MongoDb Server.
*/

// BEGIN: CONFIGURATION
const EXPRESS_PORT = 3000;
const MONGODB_PORT = 27017;
const DATABASE_URL = "mongodb://localhost:" + MONGODB_PORT;
const DATABASE_NAME = "bigDataProjectDb";
const DATABASE_COLLECTION_NAME = "summaryMatchingResults";
const RATES_COLUMN_NAME = "Rates"

const FOLDER_PAGES = "pages/";
const FOLDER_STYLES = "styles/";
const FOLDER_SCRIPTS = "scripts/";

var express = require('express');
var app = express();
var MongoClient = require('mongodb').MongoClient;	// [INSTALLATION] npm install --save express mongodb
// END: CONFIGURATION


// BEGIN: ROUTING
app.get('/', (req, res) => {
	res.set('Content-Type', 'text/html');
	res.sendFile(FOLDER_PAGES + "index.html", {root: __dirname });
})

app.get('/' + FOLDER_STYLES + "style.css", (req, res) => {
	res.set('Content-Type', 'text/css');
	res.sendFile(FOLDER_STYLES + "style.css", {root: __dirname });
})

app.get('/' + FOLDER_SCRIPTS + "getMongoDbData.js", (req, res) => {
	res.set('Content-Type', 'application/javascript');
	MongoClient.connect(DATABASE_URL, function(err, client) {
	if (!err) {

	const db = client.db(DATABASE_NAME);
	const collection = db.collection(DATABASE_COLLECTION_NAME);
	collection.find({}).toArray(function(err, summaryMatchingResultsArray) {
		if (!err) {
			//console.log(Object.keys(summaryMatchingResultsArray[0]));
			keys = Object.keys(summaryMatchingResultsArray[0]);
			let summaryMatchingResultsTable = '$("table")[0].outerHTML = "<table id=' + "'summaryMatchingTable'" + '>';
			
			// BEGIN: Headers of the table
			summaryMatchingResultsTable += '<tr>';
			keys.forEach(function(key){
				if(key != RATES_COLUMN_NAME){
					summaryMatchingResultsTable += '<th>' + key + '</th>';
				} else {
					n_keys = Object.keys(summaryMatchingResultsArray[0][key]);
					n_keys.forEach(function(n_key){
						summaryMatchingResultsTable += '<th>' + n_key + '</th>';
					});
				}
			});
			summaryMatchingResultsTable += '</tr>';
			// END: Headers of the table
			
			// BEGIN: Content of the table
			summaryMatchingResultsArray.forEach(function(summaryMatchingResult){
				summaryMatchingResultsTable += '<tr>';
				let keys = Object.keys(summaryMatchingResult);
				keys.forEach(function(key){
					if(key != RATES_COLUMN_NAME){
						summaryMatchingResultsTable += '<td>' + summaryMatchingResult[key] + '</td>';
					} else {
						
						n_keys = Object.keys(summaryMatchingResult[key]);
						
						n_keys.forEach(function(n_key){
							summaryMatchingResultsTable += '<td>' + summaryMatchingResult[key][n_key] + '</td>';
						});
					}
				});
				summaryMatchingResultsTable += '</tr>';
				//output += '<tr><td>' + summaryMatchingResult[_id] + '</td><td>' + todo.details + '</td></tr>';
			});
			// END: Content of the table
			
			// write HTML output (ending)
			summaryMatchingResultsTable += '</table>";';

			// send output back
			res.send(summaryMatchingResultsTable);
		}
	});

	// close db client
	client.close();
	}
	});
})
// END: ROUTING
app.listen(EXPRESS_PORT, () => console.log('Express app listening on port ' + EXPRESS_PORT))