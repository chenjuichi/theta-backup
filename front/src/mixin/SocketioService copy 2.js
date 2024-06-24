import { io } from 'socket.io-client';

class SocketioService {
  socket = null;
  /*
  async setupSocketConnection(local_ip, user_id) {
    if (!this.socket) {
      this.socket = io(`http://${local_ip}:6500`);
      this.socket.emit('message', `Hello there from Vue. ${user_id}`);

      console.log(`Socket connection setup with local_ip: ${local_ip}, user_id: ${user_id}`);

      return new Promise((resolve, reject) => {
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
  }

  async reconnectSocket(local_ip, user_id, existingSockId) {
    if (!this.socket) {
      this.socket = io(`http://${local_ip}:6500`, {
        query: { existingSockId } // Pass existingSockId to the server
      });

      console.log(`Reconnecting socket with existingSockId: ${existingSockId}`);

      return new Promise((resolve, reject) => {
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
    this.socket = io(`http://${local_ip}:6500`, {
      query: {
        userId: user_id
      }
    });
  };

  reconnectSocket(local_ip, user_id, sock_id) {
    this.socket = io(`http://${local_ip}:6500`, {
      query: {
        existingSockId: sock_id,
        userId: user_id
      }
    });
  };

}

export default new SocketioService();