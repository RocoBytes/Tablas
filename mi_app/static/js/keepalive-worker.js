setInterval(() => {
    self.postMessage('keepalive');
}, 30000); 