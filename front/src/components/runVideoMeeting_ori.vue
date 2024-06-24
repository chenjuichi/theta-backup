<template>
<v-app>
  <v-container fluid class="web-camera-container">
    <div v-if="!connected">
      <p>正在連線...</p>
    </div>
    <div v-else>
      <div v-for="(message, index) in messages" :key="index">
        {{ message }}
      </div>
      <input type="text" v-model="messageToSend" placeholder="輸入訊息">
      <button @click="sendMessage">發送訊息</button>
    </div>
  </v-container>
</v-app>
</template>

<script>

import io from 'socket.io-client';
import adapter from 'webrtc-adapter';

export default {
  name: 'runVideoMeeting',

  computed: {
  },

  watch: {
  },

  created() {
  },

  mounted() {
    // 連接到對等節點
    this.socket = io.connect(this.peerAddress);
    console.log("step 1...", this.socket);
    // 初始化對等連接
    this.initPeerConnection();
    console.log("step 2...");
    // 監聽從對等節點接收到的ICE候選
    this.socket.on('iceCandidate', (candidate) => {
      this.addIceCandidate(candidate);
    });
    console.log("step 3...");
    // 監聽連接建立事件
    this.socket.on('connect', () => {
      this.connected = true;
    });
    console.log("step 4...", this.connected);
    // 監聽連接斷開事件
    this.socket.on('disconnect', () => {
      this.connected = false;
    });
    console.log("step 4...", this.connected);
  },

  data() {
    return {
      currentUser: {
      },
      messages: [],
      messageToSend: '',
      socket: null,
      peerConnection: null,
      peerAddress: 'http://192.168.32.50:6500', // 例如：'http://对等节点IP:端口'
      connected: false
    };
  },

  methods: {

    // 初始化對等連接
    initPeerConnection() {
      // 使用adapter獲取流覽器相容的RTCPeerConnection物件
      this.peerConnection = new RTCPeerConnection();

      // 監聽ICE候選
      this.peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
          // 將ICE候選發送給對等節點
          this.socket.emit('iceCandidate', event.candidate);
        }
      };

      // 監聽從對等節點接收到的消息
      this.peerConnection.ondatachannel = (event) => {
        event.channel.onmessage = (messageEvent) => {
          this.messages.push(messageEvent.data);
        };
      };
    },
    // 創建資料通道並發送消息
    sendMessage() {
      if (this.messageToSend.trim() === '') return;
      const dataChannel = this.peerConnection.createDataChannel('dataChannel');
      dataChannel.send(this.messageToSend);
      this.messages.push('我： ' + this.messageToSend);
      this.messageToSend = '';
    },
    // 添加對等節點的ICE候選
    addIceCandidate(candidate) {
      this.peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
    }
  },
}
</script>

