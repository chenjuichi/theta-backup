import { io } from 'socket.io-client';

class SocketioService {
  socket;
  constructor() {}

  //setupSocketConnection(local_ip) {
  //  this.socket = io(`http://${local_ip}:6500`);
  //
  //  console.log(`Socket connection setup with local_ip: ${local_ip}`);
  //}
  setupSocketConnection(local_ip, user_id) {
    return new Promise((resolve, reject) => {
      this.socket = io(`http://${local_ip}:6500`);

      this.socket.on('connect', () => {
        this.socket.emit('message', `Hello there from Vue. ${user_id}`);
        console.log(`Socket connection setup with local_ip: ${local_ip}, user_id: ${user_id}`);
        resolve(this.socket);
      });

      this.socket.on('connect_error', (err) => {
        console.error('Connection error:', err);
        reject(err);
      });
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
    }
  }

  //setupSocketConnection(user_id) {
  //  this.socket = io("http://192.168.32.50:6500");
  //  this.socket.emit('message', 'Hello there from Vue. ' + user_id);
  //}

  //setupSocketConnection(local_ip, user_id) {
  //  this.socket = io(`http://${local_ip}:6500`);
  //  this.socket.emit('message', `Hello there from Vue. ${user_id}`);
  //
  //  console.log(`Socket connection setup with local_ip: ${local_ip}, user_id: ${user_id}`);
  //}

  sendPreOffer(callType, calleePersonalCode) {
    console.log("SocketioService.sendPreOffer(),", callType, calleePersonalCode);

    connectedUserDetails = {
      callType: callType,
      socketId: calleePersonalCode,
    };

    if (callType === constants.callType.CHAT_PERSONAL_CODE || callType === constants.callType.VIDEO_PERSONAL_CODE) {
      const data = {
        callType: callType,
        calleePersonalCode: calleePersonalCode,
      };

      //ui.showCallingDialog(callingDialogRejectCallHandler);
      //wss.sendPreOffer(data);
    }


    this.socket.emit('pre-offer', JSON.stringify(data));

    console.log(`Pre-offer sent with data: ${JSON.stringify(data)}`);
  };
}

export default new SocketioService();