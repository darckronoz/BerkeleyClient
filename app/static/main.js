var socket = io();

        socket.on('connect', function() {
            console.log('Connected');
            socket.emit('start_stream');
        });

        socket.on('log', function(data) {
            var consoleDiv = document.querySelector('.log-console');
            var p = document.createElement('p');
            p.classList.add('console-text')
            p.innerText = data;
            consoleDiv.appendChild(p);
        });

        socket.on('update-time', function(data) {
            var hora = document.querySelector('.hora');
            hora.innerHTML = data
        });