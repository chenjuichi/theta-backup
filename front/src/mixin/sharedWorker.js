let ports = [];
let isCameraInUse = false;

self.onconnect = function(event) {
    const port = event.ports[0];
    ports.push(port);

    port.onmessage = function(event) {
        const { action } = event.data;

        if (action === 'check') {
            port.postMessage({ status: isCameraInUse });
        } else if (action === 'request') {
            if (!isCameraInUse) {
                isCameraInUse = true;
                port.postMessage({ status: true });
            } else {
                port.postMessage({ status: false });
            }
        } else if (action === 'release') {
            isCameraInUse = false;
            ports.forEach(p => p.postMessage({ status: false }));
        }
    };

    port.start();
};