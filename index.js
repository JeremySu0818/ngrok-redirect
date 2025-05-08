const express = require("express");
const fs = require("fs");
const path = require("path");
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static("public"));

const QUOTES_FILE = path.join(__dirname, "quotes.json");

app.get("/quotes", (req, res) => {
  fs.readFile(QUOTES_FILE, "utf8", (err, data) => {
    if (err) return res.status(500).json({ error: "讀取失敗" });
    res.json(JSON.parse(data));
  });
});

app.post("/save", (req, res) => {
  const quotes = req.body;
  fs.writeFile(QUOTES_FILE, JSON.stringify(quotes, null, 2), (err) => {
    if (err) return res.status(500).json({ error: "儲存失敗" });
    res.json({ status: "ok" });
  });
});

app.listen(PORT, () => {
  console.log("伺服器已啟動：http://localhost:" + PORT);
});
