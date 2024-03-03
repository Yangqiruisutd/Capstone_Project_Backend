const express = require("express");
const cors = require("cors");
const multer = require("multer");
const app = express();
app.use(cors());
const { exec } = require("child_process");

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "uploads/"); // Uploads will be stored in the 'uploads/' directory
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname); // Keep the original filename
  },
});

const upload = multer({ storage: storage });

app.post("/upload", upload.single("csvFile"), (req, res) => {
  if (!req.file) {
    return res.status(400).send("No file uploaded");
  }

  const csvFilePath = req.file.path;

  // Run Python script
  exec(`python ml.py ${csvFilePath}`, (error, stdout, stderr) => {
    if (error) {
      console.error("Error executing Python script:", error);
      return res.status(500).send("Error processing CSV file");
    }

    try {
      // Parse Python script output as JSON
      const jsonData = JSON.parse(stdout);
      console.log("Parsed JSON data:", jsonData);
      // Send JSON data as response
      res.json(jsonData);
    } catch (parseError) {
      console.error("Error parsing JSON:", parseError);
      return res.status(500).send("Error parsing JSON");
    }
  });
});

const port = 3000;
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
