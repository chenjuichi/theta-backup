import { io } from 'socket.io-client';
/*
class SocketioService {
  socket = null;

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  sendPreOffer(callType, calleePersonalCode) {
    if (!this.socket) {
      console.error("Socket is not initialized.");
      return;
    }
    const data = {
      callType: callType,
      calleePersonalCode: calleePersonalCode,
    };
    console.log(`data: ${JSON.stringify(data)}`);

    this.socket.emit('pre-offer', JSON.stringify(data));
    console.log(`Pre-offer sent with data: ${JSON.stringify(data)}`);
  }

  setupSocketConnection(local_ip, user_id) {
    return new Promise((resolve, reject) => {
      this.socket = io(`http://${local_ip}:6500`, {
        query: {
          userId: user_id
        }
      });

      this.socket.on('connect', () => {
        console.log('Socket connected:', this.socket.id);
        resolve(this.socket);
      });

      this.socket.on('connect_error', (err) => {
        console.error('Socket connection error:', err);
        reject(err);
      });
    });
  }

  reconnectSocket(local_ip, user_id, sock_id) {
    return new Promise((resolve, reject) => {
      this.socket = io(`http://${local_ip}:6500`, {
        query: {
          existingSockId: sock_id,
          userId: user_id
        }
      });

      this.socket.on('connect', () => {
        console.log('Socket reconnected:', this.socket.id);
        resolve(this.socket);
      });

      this.socket.on('connect_error', (err) => {
        console.error('Socket reconnection error:', err);
        reject(err);
      });
    });
  }
}
*/
class SocketioService {
  socket = null;

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  sendPreOffer(userId, callType, calleePersonalCode) {
    if (!this.socket) {
      console.error("Socket is not initialized.");
      return;
    }
    const data = {
      targetUserId: userId,
      callType: callType,
      calleePersonalCode: calleePersonalCode,
    };
    //console.log(`data: ${JSON.stringify(data)}`);
    this.socket.emit('pre-offer', JSON.stringify(data));
    console.log(`Pre-offer sent with data: ${JSON.stringify(data)}`);
  }

  setupSocketConnection(local_ip, user_id) {
    return new Promise((resolve, reject) => {
      console.log(`Attempting to connect to http://${local_ip}:6500 with user_id ${user_id}`);
      this.socket = io(`http://${local_ip}:6500`, {
        query: {
          userId: user_id
        }
      });

      this.socket.on('connect', () => {
        console.log('Socket connected:', this.socket.id);
        resolve(this.socket);
      });

      this.socket.on('connect_error', (err) => {
        console.error('Socket connection error:', err);
        reject(err);
      });
    });
  }

  reconnectSocket(local_ip, user_id, sock_id) {
    return new Promise((resolve, reject) => {
      console.log(`Attempting to reconnect to http://${local_ip}:6500 with existingSockId ${sock_id} and user_id ${user_id}`);
      this.socket = io(`http://${local_ip}:6500`, {
        query: {
          existingSockId: sock_id,
          userId: user_id
        }
      });

      this.socket.on('connect', () => {
        console.log('Socket reconnected:', this.socket.id);
        resolve(this.socket);
      });

      this.socket.on('connect_error', (err) => {
        console.error('Socket reconnection error:', err);
        reject(err);
      });
    });
  }
}

export default new SocketioService();
