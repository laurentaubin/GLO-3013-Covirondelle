const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const axios = require('axios')
const path = require("path")


const STATION_ENDPOINT_URL = "http://localhost:5000/information"
const port = process.env.PORT || 4001;

const app = express();
app.use(express.static(path.join(__dirname, "..", "build")))
app.use(express.static(path.join(__dirname, "..", "public")))


app.use((req, res, next) => {
  res.sendFile(path.join(__dirname, "..", "build", "index.html"));
});

const server = http.createServer(app);


const io = socketIo(server, {
  cors: {
    origin: "http://localhost:4001",
    methods: ["GET", "POST"]
  }
});

let interval;

io.on("connection", (socket) => {
  console.log("New client connected");
  if (interval) {
    clearInterval(interval);
  }
  interval = setInterval(() => getApiAndEmit(socket), 1000);
  socket.on("disconnect", () => {
    console.log("Client disconnected");
    clearInterval(interval);
  });
});

const getApiAndEmit = socket => {
  axios.get(STATION_ENDPOINT_URL).then(function (response) {
      socket.emit("GameCycleUpdate", response.data);
    }
  ).catch(function (error) {
    console.log(`covirondelle-station webserver down: ${error.code}`);
  })
};

server.listen(port, () => console.log(`Listening on port ${port}`));