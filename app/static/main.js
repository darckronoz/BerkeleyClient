var socket = io();

socket.on('connect', function() {
    console.log('Connected');
});

socket.on('message', function(data) {
    alert(data);
});