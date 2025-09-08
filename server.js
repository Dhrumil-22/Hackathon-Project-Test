const express = require("express");
const axios = require("axios");
const cors = require("cors");
const multer = require("multer");
const upload = multer();

const app = express();
app.use(cors());
app.use(express.json());

app.post("/api/predict-text", async (req, res) => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/predict-text", null, {
      params: { text: req.body.text },
    });
    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post("/api/predict-image", upload.single("file"), async (req, res) => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/predict-image", 
      { file: req.file.buffer }, 
      { headers: { "Content-Type": "multipart/form-data" } }
    );
    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(5000, () => console.log("Backend running on http://localhost:5000"));
