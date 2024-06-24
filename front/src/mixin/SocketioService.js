import { io } from 'socket.io-client';

class SocketioService {
  socket = null;

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }
  //打電話的人, 通話型式, 接電話的人
  async sendPreOfferAnswer(userId, callType, calleeId) {
    if (!this.socket) {
      console.error("Socket is not initialized.");
      return;
    }

    const data = {
      callerUserId: userId,                   //打電話的人
      //targetUserId: userId,                   //打電話的人
      callType: callType,                     //通話型式
      //calleePersonalCode: calleePersonalCode, //接電話的人
      calleeUserId: calleeId,       //接電話的人
    };

    try {
      await this.ensureConnected();
      this.socket.emit('pre-offer-answer', JSON.stringify(data));
      console.log(`Pre-offer-answer sent with data: ${JSON.stringify(data)}`);
    } catch (error) {
      console.error("Failed to send pre-offer-answer due to connection issues.", error);
    }
  };

  //打電話的人, 通話型式, 接電話的人
  async sendPreOffer(userId, callType, calleePersonalCode) {
    if (!this.socket) {
      console.error("Socket is not initialized.");
      return;
    }

    const data = {
      callerUserId: userId,                   //打電話的人
      //targetUserId: userId,                   //打電話的人
      callType: callType,                     //通話型式
      //calleePersonalCode: calleePersonalCode, //接電話的人
      calleeUserId: calleePersonalCode,       //接電話的人
    };

    try {
      await this.ensureConnected();
      this.socket.emit('pre-offer', JSON.stringify(data));
      console.log(`Pre-offer sent with data: ${JSON.stringify(data)}`);
    } catch (error) {
      console.error("Failed to send pre-offer due to connection issues.", error);
    }
  }

  async sendDataUsingWebRTCSignaling(userId, callType, candidate) {
    if (!this.socket) {
      console.error("Socket is not initialized.");
      return;
    }

    const data = {
      connectedUserSocketId: userId,                   //接電話的人
      type: callType,
      candidate: candidate,
    };

    try {
      await this.ensureConnected();
      this.socket.emit('webRTC-signaling', JSON.stringify(data));
      console.log(`webRTC-signaling sent with data: ${JSON.stringify(data)}`);
    } catch (error) {
      console.error("Failed to send webRTC-signaling due to connection issues.", error);
    }
  }

  async setupSocketConnection(local_ip, user_id) {
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

  async reconnectSocket(local_ip, user_id, sock_id) {
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

  ensureConnected() {
    return new Promise((resolve, reject) => {
      if (this.socket && this.socket.connected) {
        resolve(this.socket);
      } else {
        this.socket.once('connect', () => {
          resolve(this.socket);
        });
        this.socket.once('connect_error', (err) => {
          reject(err);
        });
      }
    });
  }

    // 發送 SDP
    sendSDP(sdp) {
      this.socket.emit('sdp', sdp);
    }

    // 監聽 SDP
    onSDP(callback) {
      this.socket.on('sdp', callback);
    }

    // 发發送 ICE 候選者
    sendICECandidate(candidate) {
      this.socket.emit('ice-candidate', candidate);
    }

    // 監聽 ICE 候選者
    onICECandidate(callback) {
      this.socket.on('ice-candidate', callback);
    }
}

export default new SocketioService();