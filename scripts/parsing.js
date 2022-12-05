const fs = require("fs");
const builder = require("xmlbuilder");

const stream = fs.createReadStream("./train.csv")

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

    // Remove the first two elements
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

    // const doc = builder.create("root");
    // const tags = doc.ele("tags");
    // doc.ele("content")
    //     .txt(obj["text"])

    // for (const entry of Object.keys(obj)) {
    //     tags.att(entry.replace(">", "gt_").replace("<", "lt_"), obj[entry]);
    // }

    // Add 2500 files to the train folder and 2500 to the test folder.
    const folder = entries < 2500 ? "training" : "testing";
    fs.writeFileSync(`./data/${folder}/${obj["comment_id"]}.json`, JSON.stringify(obj, null, 4));


    entries++;
    if (entries === 5000) {
        rl.close();
        console.log("Done.")
    } else if (entries % 100 === 0) {
        console.log(`Processed ${entries} entries.`);
    }
});
    // for (let key in obj) {
    //     // If key/value is a boolean
    //     if (typeof obj[key] === "boolean") {
    //         const label = key.replace(">", "gt_").replace("<", "lt_");
    //         if (!fs.existsSync(`./training/${label}`)) {
    //             fs.mkdirSync(`./training/${label}`);
    //         }



    //         for (const tag of (Object.keys(obj).filter((key) => obj[key] === true))) {
    //             tags.att(tag.replace(">", "gt_").replace("<", "lt_"), "true");
    //         }

    //         doc.ele("content")
    //             .txt(obj["text"])

    //         fs.writeFileSync(`./training/${label}/${obj["comment_id"]}`, doc.toString({ pretty: true }));
    //     }
    // }
//     console.log(doc.toString({ pretty: true }));
// });
