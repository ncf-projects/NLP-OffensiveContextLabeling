const fs = require("fs");

const stream = fs.createReadStream("./train.csv")

// If the data folder does not exist, create it.
if (!fs.existsSync("./data")) {
    fs.mkdirSync("./data");
}

// If the folders 'testing' and 'training' inside the data folder do not exist, create them.
if (!fs.existsSync("./data/testing")) {
    fs.mkdirSync("./data/testing");
}
if (!fs.existsSync("./data/training")) {
    fs.mkdirSync("./data/training");
}

// Read csv data line by line
const readline = require('readline');
const rl = readline.createInterface({
    input: stream,
    crlfDelay: Infinity
});

let headers;
rl.once("line", (line) => {
    // Split the line by comma
    headers = line.split(",");
});

let entries = 0;
// Read csv data line by line
rl.on('line', (line) => {
    // Split the line by comma
    const values = line.split(",");
    // Create an object with the headers as keys
    const obj = headers.reduce((acc, header, index) => {
        let value = values[index]
        // Convert the value to a number if it is a number
        value = !isNaN(value) ? Number(value) : value;
        // Convert the value to a boolean if it is a boolean
        value = value === "True" ? true : value === "False" ? false : value;

        acc[header] = value;
        return acc;
    }, {});


    // Add 2500 files to the train folder and 2500 to the test folder.
    const folder = entries < 25000 ? "training" : "testing";
    fs.writeFileSync(`./data/${folder}/${obj["comment_id"]}.json`, JSON.stringify(obj, null, 4));

    entries++;
    if (entries === 50000) {
        rl.close();
        console.log("Done.")
    } else if (entries % 100 === 0) {
        console.log(`Processed ${entries} entries.`);
    }
});

