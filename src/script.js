// Create WebSocket connection.
server_link = "ws://localhost:"
const socket = new WebSocket(server_link);

// Connection opened
socket.addEventListener("open", (event) => {
  socket.send("Hello Server!");
});

// Listen for messages
socket.addEventListener("message", (event) => {
  console.log("Message from server ", event.data);
});
