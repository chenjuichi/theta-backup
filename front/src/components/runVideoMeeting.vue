<template>
<v-app>
  <v-container fluid class='main_container'>
  <!--
    <h1>Vue.js Socket.io Chat</h1>
    <v-row align="center" justify="space-around">
      <v-btn @click="socketSendmsg">建立message</v-btn>
    </v-row>
    <v-row align="center" justify="space-around">
      <div v-for="(message, index) in messages" :key="index">
        {{ message }}
      </div>
    </v-row>
  -->
    <div class='dashboard_container' :class="{ 'blur-effect': display_filter }">
      <div class='logo_container'>
        <img id="sourceImage" :src="imageSrc" alt="Source Image" class="display_none">
        <canvas id="canvas" class="logo_img" />
      </div>

      <div>
        <div class='description_container'>
          <p class='description_container_paragraph'>
            Hello...User {{user_id}}
          </p>
        </div>
        <div class='personal_code_container'>
          <div class='personal_code_title_container'>
            <p class='personal_code_title_paragraph'>
              Your personal code
            </p>
          </div>
          <div class="personal_code_value_container">
            <p class='personal_code_value_paragraph' id='personal_code_paragraph'>
              {{sock_id}}
            </p>
            <v-btn @click="copyBtn" small color="white" style="position: relative; left: 10px;" class="copy_btn">
              <span style="color: Tomato;">
                <i class="fa-regular fa-copy fa-2x" />
              </span>
            </v-btn>
          </div>
        </div>

        <div class='personal_code_connecting_container'>
          <v-text-field
            label="Personal Code"
            solo
            v-model="personal_code_input"
            class='flex-grow-1 flex-shrink-0'
            style='min-width: 85px; max-width: 100%;'
          >
            <template #prepend-inner>
              <v-icon>mdi-account</v-icon>
            </template>
          </v-text-field>
          <div class='personal_code_connecting_buttons_container'>
            <v-btn @click="chatBtn" small  class="chat_btn">
              <span style="color: Dodgerblue;">
                <i class="fa-regular fa-comment-dots fa-2x" />
              </span>
            </v-btn>
            <v-btn @click="videoBtn" small class="video_btn">
              <span style="color: Tomato;">
                <i class="fa-solid fa-video fa-2x" />
              </span>
            </v-btn>
          </div>
        </div>

        <div class='stranger_connecting_container'>
          <p class='stranger_title_container'>
            Stranger
          </p>
          <div class='stranger_buttons_container'>
            <v-btn @click="stranger_chatBtn" small>
              <v-icon>mdi-chat</v-icon>
            </v-btn>
            <v-btn @click="stranger_videoBtn" small>
              <v-icon>mdi-video</v-icon>
            </v-btn>
          </div>
        </div>

        <div class='checkbox_container'>
          <div class='checkbox_connection'>
            <v-checkbox
              v-model="allow_strangers_checkbox"
              label="Allow connection from strangers"
              color="red"
              hide-details
            ></v-checkbox>
          </div>
        </div>
        <div class='display_none'></div>
      </div>
    </div>

    <div class='call_container' :class="{ 'blur-effect': display_filter }">
      <div class='videos_container'>
          <div class='videos_placeholder'>
            <img src='../assets/pmc2_r_logo.png' />
          </div>
          <!--<video class='remote_video display_none' autoplay />-->
          <video ref="remoteVideo" class='remote_video' autoplay playsinline />

          <div class='local_video_container'>
              <div v-if="videoPreparing" class="video-preparing">
                視訊準備中...
              </div>
              <video ref="video" class='local_video' autoplay playsinline />
          </div>

          <div class='call_buttons_container'>
            <v-btn @click="micBtn" small fab :class="{ 'display_none': call_buttons_nonvisible }">
              <v-icon>mdi-microphone</v-icon>
            </v-btn>
            <v-btn @click="cameraBtn" small fab :class="{ 'display_none': call_buttons_nonvisible }">
              <v-icon>mdi-camera</v-icon>
            </v-btn>
            <v-btn @click="hangUpBtn"
              fab
              style="background: #fc5d5b; transition: 0.3s;"
              :class="{'display_none': call_buttons_hangup_nonvisible , 'center_hor': !call_buttons_hangup_nonvisible}"
            >
              <v-icon>mdi-phone-hangup</v-icon>
            </v-btn>
            <v-btn @click="screenSharingBtn" small fab :class="{ 'display_none': call_buttons_nonvisible }">
              <v-icon>mdi-share-variant</v-icon>
            </v-btn>
            <v-btn @click="recordingBtn" small fab :class="{ 'display_none': call_buttons_nonvisible }">
              <v-icon>mdi-record-rec</v-icon>
            </v-btn>
          </div>

          <div class='finish_chat_button_container display_none'>
            <v-btn @click="finishCallBtn">
              <v-icon>mdi-phone-hangup</v-icon>
            </v-btn>
          </div>

          <div class='video_recording_buttons_container'>
            <v-btn @click="pauseBtn" icon color="white" class='recording_button'>
              <v-icon>mdi-pause-circle</v-icon>
            </v-btn>
            <v-btn @click="resumeBtn" icon color="white" class='recording_button'>
              <v-icon>mdi-arrow-right-drop-circle</v-icon>
            </v-btn>
            <v-btn @click="stopBtn" icon color="white" class='recording_button'>
              <v-icon>mdi-stop-circle</v-icon>
            </v-btn>
          </div>
      </div>
    </div>

    <div class='messenger_container' :class="{ 'blur-effect': display_filter }">
      <div class='messages_container' />
      <div class='new_message_container'>
        <v-text-field
          v-model="new_message_input"
          append-icon='mdi-send-circle'
          label="Message"
          clearable
          filled
          type="text"
          @click:append="newMsgSendBtn"
          style="position: relative; top:28px;"
        >
          <template #append>
            <v-icon color="#ffba6a">mdi-send-circle</v-icon>
          </template>
        </v-text-field>
      </div>
    </div>

    <div class="flex-container">
      <v-dialog v-model="dialogVisible" max-width="300px">
        <v-card>
          <v-card-title class="headline">
            {{ dialogTitle }}
          </v-card-title>
          <div class="image-container">
            <img src="../assets/dialogAvatar.png" aspect-ratio="1" max-width="150" class="mb-4" />
          </div>
          <v-card-actions class="button-container">
            <v-btn v-show="dialogTitle !== 'Calling'" color="green darken-1" icon @click="acceptCallHandler">
              <v-icon>mdi-phone</v-icon>
            </v-btn>
            <v-btn :class="{ 'centered-btn': dialogTitle === 'Calling' }" color="red darken-1" icon @click="rejectCallHandler">
              <v-icon>mdi-phone-off</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </v-container>
</v-app>
</template>

<script>
import { OLD_COLOR, NEW_COLOR } from '../mixin/css_constants.js';

import SocketioService from '../mixin/SocketioService.js';
import * as constants from '../mixin/constants.js';
//import { useDevicesList, useUserMedia } from '@vueuse/core';
import { mapGetters } from 'vuex';

import { EventBus } from '../mixin/EventBus.js';

export default {
  name: 'runVideoMeeting',

  computed: {
    /*
    user_id() {
      return this.$store.getters.user_id;
    },

    sock_id() {
      return this.$store.getters.sock_id;
    },
    */
    ...mapGetters(['user_id', 'sock_id']),
  },

  watch: {
    local_ip(newVal, oldVal) {
      localStorage.setItem('local_ip', newVal);
    },
    /*
    currentCamera() {
      if (this.enabled) {
        this.stopStream();
        this.startStream();
      }
    },
    */
  },

  created() {
    console.log("created()...");

    this.restoreStateFromLocalStorage();

    console.log("created(), user_id, step1...", this.local_ip, this.user_id);

    const initializeSocket = () => {
      if (!this.sock_id) {
        SocketioService.setupSocketConnection(this.local_ip, this.user_id)
          .then(() => {
            console.log("Socket connected and initialized.");

            if (SocketioService.socket) {
              SocketioService.socket.on('broadcast', this.handleBroadcastMessage);
              SocketioService.socket.on('pre-offer', this.handlePreOffer);
              SocketioService.socket.on('pre-offer-answer', this.handlePreOfferAnswer);
              SocketioService.socket.on('webRTC-signaling', this.handleWebRTC);
              this.changeSockID(SocketioService.socket.id);
            } else {
              console.error("SocketioService.socket is not initialized");
            }
          })
          .catch(err => {
            console.error("Socket setup failed:", err);
          });
      } else {
        SocketioService.reconnectSocket(this.local_ip, this.user_id, this.sock_id)
          .then(() => {
            console.log("Socket reconnected and initialized.");

            if (SocketioService.socket) {
              SocketioService.socket.on('broadcast', this.handleBroadcastMessage);
              SocketioService.socket.on('pre-offer', this.handlePreOffer);
              SocketioService.socket.on('pre-offer-answer', this.handlePreOfferAnswer);
              SocketioService.socket.on('webRTC-signaling', this.handleWebRTC);
            } else {
              console.error("SocketioService.socket is not initialized");
            }
          })
          .catch(err => {
            console.error("Socket reconnection failed:", err);
          });
      }
    };

    if (this.user_id === '00000000') {
      console.log("created(), user_id, sock_id, step2-1...", this.user_id, this.sock_id);
      this.changeUserID();
      initializeSocket();
      console.log("created(), user_id, sock_id, step2-2...", this.user_id, this.sock_id);
    } else {
      console.log("created(), user_id, sock_id, step3...", this.local_ip, this.user_id, this.sock_id);
      initializeSocket();
    }

    window.addEventListener('beforeunload', this.handleBeforeUnload);
  },

  mounted() {
    // if back button is pressed
    window.onpopstate = () => {
      console.log("press back button, good bye...");
    };
    //
    this.replaceImageColor();
    //
    //EventBus.$on('startVideoRequested', this.handleStartVideoRequest);
    EventBus.$on('startVideoRequested', this.startVideo);
    EventBus.$on('pauseVideoRequested', this.pauseVideo);
  },

  data() {
    return {
      Random_value: 0,
      personal_code_display: 'DDDDDD',
      personal_code_input: '',
      new_message_input: '',
      allow_strangers_checkbox: false,
      dialogVisible: false,
      call_buttons_nonvisible: true,
      call_buttons_hangup_nonvisible: true,
      dialogTitle: 'Incoming Call',
      messages: [],
      newMessage: '',
      display_filter: false,                  // 控制模糊效果
      local_ip: this.$store.getters.local_ip, // 初始化 local_ip
      caller_user_id: '',
      isPageReloading: false,
      imageSrc: require('../assets/TALK_TO_YOU_rm_color_0264ce.png'),
      //
      maxRetries: 5,
      retryDelay: 500,        // 0.5 seconds
      permissions: ["camera", "microphone"],
      videoPreparing: false,  // flag for视頻是否準備中
      //
      currentStream: null,    // 本地媒體流
      remoteStream: null,     // 遠端媒體流
      peerConnection: null,
      dataChannel: null,
      isCaller: false,
      iceServers: [
        {
          urls: 'stun:stun.l.google.com:19302'
        }
      ],
    };
  },

  methods: {
    replaceImageColor() {
      console.log("replaceImageColor()...");

      const sourceImage = document.getElementById('sourceImage');
      const canvas = document.getElementById('canvas');
      const ctx = canvas.getContext('2d');

      sourceImage.onload = function() {
        canvas.width = sourceImage.width;
        canvas.height = sourceImage.height;
        ctx.drawImage(sourceImage, 0, 0);

        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;

        //const oldColor = { r: 2, g: 100, b: 206 }; // #0264ce
        //const newColor = { r: 90, g: 150, b: 204 }; // #5a96cc
        // 解析舊颜色和新颜色
        const oldColor = {
          r: parseInt(OLD_COLOR.substr(1, 2), 16),
          g: parseInt(OLD_COLOR.substr(3, 2), 16),
          b: parseInt(OLD_COLOR.substr(5, 2), 16)
        };

        const newColor = {
          r: parseInt(NEW_COLOR.substr(1, 2), 16),
          g: parseInt(NEW_COLOR.substr(3, 2), 16),
          b: parseInt(NEW_COLOR.substr(5, 2), 16)
        };

        for (let i = 0; i < data.length; i += 4) {
          if (data[i] === oldColor.r && data[i + 1] === oldColor.g && data[i + 2] === oldColor.b) {
            data[i] = newColor.r;
            data[i + 1] = newColor.g;
            data[i + 2] = newColor.b;
          }
        }

        ctx.putImageData(imageData, 0, 0);
      };

      // 觸發圖片加載
      sourceImage.src = this.imageSrc;
    },

    getRandom(min,max){
      console.log("getRandom(), ", min, max);

      return Math.floor(Math.random()*(max-min+1))+min;
    },

    changeUserID() {
      console.log("changeUserID()...");

      let temp_user_id = String(this.getRandom(1, 10000000 - 1)).padStart(8, "0");
      this.$store.dispatch('updateUserID', temp_user_id);
      sessionStorage.setItem('user_id', temp_user_id); // Update sessionStorage
      console.log("changeUserID(), ", temp_user_id);
    },

    changeSockID(temp_sock_id) {
      console.log("changeSockID(), ", temp_sock_id);

      this.$store.dispatch('updateSockID', temp_sock_id);
      sessionStorage.setItem('sock_id', temp_sock_id);  // Update sessionStorage
      console.log("changeSockID(), ", temp_sock_id);
    },

    updateLocalIP(local_ip) {
      console.log("updateLocalIP(), ", local_ip);

      this.local_ip = local_ip;
      this.$store.dispatch('updateLocalIP', local_ip);
      localStorage.setItem('local_ip', local_ip);       // Update localStorage
      console.log("updateLocalIP(), ", local_ip);
    },

    clearSessionStorage() {
      console.log("clearSessionStorage()...");

      this.$store.dispatch('clearStorage');
      sessionStorage.setItem('user_id', '00000000');
      sessionStorage.setItem('sock_id', '');
      localStorage.setItem('local_ip', '');
      console.log('sessionStorage initialized: ', user_id, sock_id);
      console.log('localStorage initialized: ', local_ip);
    },

    async copyBtn() {
      console.log("copyBtn()...");

      if (navigator.clipboard && navigator.clipboard.writeText) {
        try {
          // Clear clipboard by writing an empty string
          await navigator.clipboard.writeText('');

          // Write the actual content to the clipboard
          await navigator.clipboard.writeText(this.user_id);
          console.log('Text copied to clipboard');
        } catch (err) {
          console.error('Error accessing clipboard:', err);
        }
      } else {
        this.fallbackCopyTextToClipboard(this.user_id);
      }
    },

    fallbackCopyTextToClipboard(text) {
      // Create a temporary textarea element
      const textArea = document.createElement('textarea');
      textArea.value = text;

      // Avoid scrolling to bottom
      textArea.style.position = 'fixed';
      textArea.style.top = '0';
      textArea.style.left = '0';
      textArea.style.width = '2em';
      textArea.style.height = '2em';
      textArea.style.padding = '0';
      textArea.style.border = 'none';
      textArea.style.outline = 'none';
      textArea.style.boxShadow = 'none';
      textArea.style.background = 'transparent';

      // Append textarea to body
      document.body.appendChild(textArea);

      // Select the text in the textarea
      textArea.select();
      textArea.setSelectionRange(0, 99999); // For mobile devices

      try {
        // Copy the text
        const successful = document.execCommand('copy');
        if (successful) {
          console.log('Text copied to clipboard');
        } else {
          console.error('Failed to copy text to clipboard');
        }
      } catch (err) {
        console.error('Error executing copy command', err);
      }

      // Remove the textarea
      document.body.removeChild(textArea);
    },

    newMsgSendBtn() {
    },

    chatBtn() {
      console.log("chatBtn()...");

      const myCallType = constants.callType.CHAT_PERSONAL_CODE;
      const myCalleePersonalCode = this.personal_code_input;  //接電話的人

      this.dialogTitle='Calling'

      this.display_filter=true;
      this.dialogVisible=true;

      if (SocketioService.socket) {
        console.log("Socket is ok, send pre-offer.",this.user_id, myCallType, myCalleePersonalCode);
        SocketioService.sendPreOffer(this.user_id, myCallType, myCalleePersonalCode); //打電話的人, 通話型式, 接電話的人
      } else {
        console.error("Socket is not initialized. Cannot send pre-offer.");
      }

      console.log("chatBtn()...endding");
    },
    //===
    delay(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },

    async getMediaDevices() {
      try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        devices.forEach(device => {
          console.log(`${device.kind}: ${device.label} id = ${device.deviceId}`);
        });
      } catch (err) {
        console.error('Error accessing media devices:', err);

        if (err.name === 'NotAllowedError') {
          alert('Please allow access to camera and microphone.');
        } else if (err.name === 'NotReadableError' || err.name === 'OverconstrainedError') {
          alert('Media device is already in use by another application. Please close any other applications that might be using the device and try again.');
        } else {
          console.error('Error accessing media devices:', err);
        }
      }
    },

    startMediaDevice() {
      console.log("startMediaDevice()...");

      this.videoPreparing = true;           // 設定顯示提示文字
      EventBus.$emit('startVideoRequested');
    },

    async closeCurrentMediaStream() {
      console.log("closeCurrentMediaStream()...");

      if (this.currentStream) {
        console.log("closeCurrentMediaStream(), step1...");

        this.currentStream.getTracks().forEach(track => {
          track.stop();
          this.currentStream.removeTrack(track);
        });

        this.currentStream = null;
        console.log("closeCurrentMediaStream(), step2...");

        await this.delay(this.retryDelay);  // 延遲後繼續重試

        console.log("closeCurrentMediaStream(), step3...");
      }
      console.log("closeCurrentMediaStream(), step4...");
    },

    // Iterate through the permissions and log the result
    async processPermissions() {
      for (const permission of this.permissions) {
        const result = await this.getPermission(permission);
        console.log(result);
      }
    },

    // Query a single permission in a try...catch block and return result
    async getPermission(permission) {
      try {
        const result = await navigator.permissions.query({ name: permission });
        return `${permission}: ${result.state}`;
      } catch (error) {
        return `${permission} (not supported)`;
      }
    },

    async startVideo() {
      console.log("startVideo()...");

      await this.getMediaDevices();           // 取得媒体設備訊息

      await this.closeCurrentMediaStream();   // 關閉當前正在使用的媒体設備

      let retries = 0;

      while (retries < this.maxRetries) {
        await this.processPermissions();

        try {
          const constraints = {
            video: true,
            audio: true
          };

          console.log("Requesting user media with constraints:", constraints);
          const stream = await navigator.mediaDevices.getUserMedia(constraints);
          console.log("Received media stream:", stream);

          // 將媒体流 currentStream
          this.currentStream = stream;

          // 將媒体流绑定到 video 元素上
          const videoElement = this.$refs.video;
          if (videoElement) {
            videoElement.srcObject = stream;
            videoElement.play();
            console.log("Video stream started.");
            this.videoPreparing = false;  // 視頻開始播放後憑, 移除提示文字
            break;                        // 成功，退出while loop
          } else {
            console.error('No video element found.');
          }
        } catch (err) {
          // 獲取媒体設備失败的情况
          console.error('Error accessing media devices:', err);
          if (err.name === 'NotAllowedError') {
            alert('Please allow access to camera and microphone.');
            break; // 用户拒決訪問，退出while loop
          } else if (err.name === 'NotFoundError') {
            alert('No media devices found. Please connect a camera and microphone.');
            break; // 没有找到媒体設備，退出while loop
          } else if (err.name === 'NotReadableError') {
            console.log('Media device is already in use by another application. Retrying...');
            retries++;
            await this.delay(this.retryDelay); // 延遲後繼續重試
          } else {
            console.error('Error accessing media devices:', err);
            break; // 其他錯誤，退出while loop
          }
        }
      } //end while

      if (retries === this.maxRetries) {
        alert('Failed to access media devices after multiple attempts. Please ensure no other applications are using the device.');
      }
    },

    // 建立 RTCPeerConnection 並添加本地流
    createPeerConnection() {
      console.log("createPeerConnection()...");

      const configuration = { iceServers: this.iceServers };
      this.peerConnection = new RTCPeerConnection(configuration);

      this.peerConection.onicecandidate = (event) => {
        console.log("geeting ice candidates from stun server");
        if (event.candidate) {
          /*
          // send our ice candidates to other peer
          SocketioService.sendDataUsingWebRTCSignaling({
            connectedUserSocketId: this.user_id,          //接電話的人
            type: constants.webRTCSignaling.ICE_CANDIDATE,
            candidate: event.candidate,
          });
          */
        }
      };

      this.peerConection.onconnectionstatechange = (event) => {
        if (peerConection.connectionState === "connected") {
          console.log("succesfully connected with other peer");
        }
      };

      // 添加遠端媒體流到 peerConnection
      this.remoteStream = new MediaStream();
      this.peerConnection.ontrack=(event) => {
        this.remoteStream.addTrack(event.track);
      };

      if (connectedUserDetails.callType === constants.callType.VIDEO_PERSONAL_CODE ||
          connectedUserDetails.callType === constants.callType.VIDEO_STRANGER) {

        for (const track of localStream.getTracks()) {  //回傳MediaStream object 中包含的所有 MediaStreamTrack objects
          peerConection.addTrack(track, this.currentStream);
        }
      }


      /*
      // 添加本地流到 peerConnection
      this.currentStream.getTracks().forEach(track => {
        this.peerConnection.addTrack(track, this.currentStream);
      });

      // 處理來自遠端的流
      this.peerConnection.ontrack = event => {
        this.remoteStream = new MediaStream();
        //this.remoteStream = event.streams[0];
        const remoteVideo = this.$refs.remoteVideo;
        if (remoteVideo) {
          remoteVideo.srcObject = this.remoteStream;
        }
      };
      */
      /*
      // 在呼叫者端, 建立 dataChannel,
      if (this.isCaller) {
        this.dataChannel = this.peerConnection.createDataChannel('chat');
        this.setupDataChannel(this.dataChannel);
      } else {
        // 接收 dataChannel
        this.peerConnection.ondatachannel = event => {
          this.dataChannel = event.channel;
          this.setupDataChannel(this.dataChannel);
        };
      }

      // 處理來自遠端的流
      this.peerConnection.ontrack = event => {
        this.remoteStream = event.streams[0];
        const remoteVideo = this.$refs.remoteVideo;
        if (remoteVideo) {
          remoteVideo.srcObject = this.remoteStream;
        }
      };
      */
      /*
      // 處理 ICE 候選者
      this.peerConnection.onicecandidate = event => {
        if (event.candidate) {
          SocketioService.sendICECandidate(event.candidate);
        }
      };
      */
    },

    setupDataChannel(dataChannel) {
      dataChannel.onopen = () => {
        console.log('Data channel is open');
      };

      dataChannel.onmessage = event => {
        console.log('Received message:', event.data);
        this.messages.push(event.data);
      };

      dataChannel.onclose = () => {
        console.log('Data channel is closed');
      };
    },
    // 發送訊息
    sendMessage() {
      if (this.dataChannel && this.dataChannel.readyState === 'open') {
        this.dataChannel.send(this.newMessage);
        this.messages.push(this.newMessage);
        this.newMessage = '';
      } else {
        console.error('Data channel is not open');
      }
    },

    async makeCall() {
      this.isCaller = true;
      this.createPeerConnection();
      // 呼叫者建立一個包含連接配置資訊的 SDP (Session Description Protocol)
      const offer = await this.peerConnection.createOffer();
      console.log('Generated SDP Offer:', offer.sdp);
      // 呼叫者將 SDP 描述設置為本地描述
      await this.peerConnection.setLocalDescription(offer);
      console.log('Set Local Description:', this.peerConnection.localDescription.sdp);
      // 發送 SDP (Session Description Protocol) 描述給遠端對等端, 以建立信令（Signaling）來交換連接參數和媒體資訊。
      SocketioService.sendSDP(this.peerConnection.localDescription);
    },

    async handleOffer(offer) {
      this.createPeerConnection();

      await this.peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
      const answer = await this.peerConnection.createAnswer();
      await this.peerConnection.setLocalDescription(answer);
      SocketioService.sendSDP(this.peerConnection.localDescription);
    },

    async handleAnswer(answer) {
      await this.peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
    },

    async handleICECandidate(candidate) {
      try {
        await this.peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
      } catch (error) {
        console.error('Error adding received ICE candidate', error);
      }
    },
/*
    const createPeerConnection = () => {
  peerConection = new RTCPeerConnection(configuration);

  dataChannel = peerConection.createDataChannel("chat");

  peerConection.ondatachannel = (event) => {
    const dataChannel = event.channel;

    dataChannel.onopen = () => {
      console.log("peer connection is ready to receive data channel messages");
    };

    dataChannel.onmessage = (event) => {
      console.log("message came from data channel");
      const message = JSON.parse(event.data);
      ui.appendMessage(message);
    };
  };

  createPeerConnection() {
    peerConection = new RTCPeerConnection(configuration);

    dataChannel = peerConection.createDataChannel("chat");

    peerConection.ondatachannel = (event) => {
      const dataChannel = event.channel;

      dataChannel.onopen = () => {
        console.log("peer connection is ready to receive data channel messages");
      };

      dataChannel.onmessage = (event) => {
        console.log("message came from data channel");
        const message = JSON.parse(event.data);
        ui.appendMessage(message);
      };
    };
*/


    //===
    pauseVideo() {
      console.log("pauseVideo()...");

      if (this.currentStream) {
        const tracks = this.currentStream.getTracks();
        tracks.forEach(track => track.stop());
        this.currentStream = null;

        const videoElement = this.$refs.video;
        if (videoElement) {
          videoElement.srcObject = null;
        }

        console.log("Video stream paused.");
      } else {
        console.log("No current stream to pause.");
      }
    },
    /*
    retry() {
      this.error = null;
      this.startVideo();
    },
    */
    handleStartVideoRequest() {
      console.log("handleStartVideoRequest()...");

      // 開始視訊的操作
      this.startVideo()
    },
    //===
    acceptCallHandler() {
      console.log("call accepted");

      const myCallType = constants.preOfferAnswer.CALL_ACCEPTED;
      this.display_filter = false;
      this.dialogVisible = false;
      this.enabled = true;

      if (SocketioService.socket) {
        this.call_buttons_hangup_nonvisible = false;

        this.startMediaDevice();

        this.createPeerConnection();

        sendPreOfferAnswer(constants.preOfferAnswer.CALL_ACCEPTED);


      } else {
        console.error("Socket is not initialized. Cannot send pre-offer-answer.");
      }
    },

    rejectCallHandler() {
      console.log("call rejected");
      const myCallType = constants.preOfferAnswer.CALL_ACCEPTED;
      SocketioService.sendPreOfferAnswer(this.user_id, myCallType);
    },

    videoBtn() {
      console.log("videoBtn()...")

      const myCallType = constants.callType.VIDEO_PERSONAL_CODE;
      const myCalleePersonalCode = this.personal_code_input;

      if (myCallType === constants.callType.CHAT_PERSONAL_CODE || myCallType === constants.callType.VIDEO_PERSONAL_CODE) {
        //this.display_filter=true;
        //this.dialogVisible=true;

        if (SocketioService.socket) {
          console.log("Socket is ok, send pre-offer.",this.user_id, myCallType, myCalleePersonalCode);
          SocketioService.sendPreOffer(this.user_id, myCallType, myCalleePersonalCode);
        } else {
          console.error("Socket is not initialized. Cannot send pre-offer.");
        }
      }

      console.log("videoBtn...endding");
    },

    stranger_chatBtn() {
    },

    stranger_videoBtn() {
    },

    micBtn() {
    },

    cameraBtn() {
    },

    hangUpBtn() {
    },

    screenSharingBtn() {
    },

    recordingBtn() {
    },

    finishCallBtn() {
    },

    pauseBtn() {
    },

    stopBtn() {
    },

    resumeBtn() {
    },
//===
    socketSendmsg() {
      console.log("socketSendmsg()...");

      SocketioService.setupSocketConnection();
    },

    handleDisconnect(message) {
      console.log("handleDisconnect()...");

      const data = JSON.parse(message);   // 解析 JSON 字符串
      console.log('Received Disconnect, ', data);
    },

    handleBroadcastMessage(message) {
      console.log("handleBroadcastMessage()...");

      const data = JSON.parse(message);   // 解析 JSON 字符串
      if (this.personal_code_display == 'DDDDDD') {
        this.personal_code_display = data.id;
        console.log('Received broadcast, sock_id:', data.id);
        console.log('Received broadcast,', data.msg1);
      }
      this.messages.push(this.personal_code_display);
    },

    handlePreOffer(message) {
      console.log("handlePreOffer()...")

      const data = JSON.parse(message); // 解析 JSON 字符串
      this.caller_user__id=data.from;
      console.log('Received pre-offer, callerSocketId:', data.from, data.callerSocketId);
      console.log('Received pre-offer, callType', data.callType);
      this.dialogTitle='Incoming Call';

      this.display_filter=true;
      this.dialogVisible=true;
    },

    handlePreOfferAnswer(message) {
      console.log("handlePreOfferAnswer()...")

      const data = JSON.parse(message);   // 解析 JSON 字符串
      console.log('Received pre-offer-answer, callerSocketId:', data);
      /*
      if (preOfferAnswer === constants.preOfferAnswer.CALLEE_NOT_FOUND) {
        //ui.showInfoDialog(preOfferAnswer);
        // show dialog that callee has not been found
      }

      if (preOfferAnswer === constants.preOfferAnswer.CALL_UNAVAILABLE) {
        //ui.showInfoDialog(preOfferAnswer);
        // show dialog that callee is not able to connect
      }

      if (preOfferAnswer === constants.preOfferAnswer.CALL_REJECTED) {
        //ui.showInfoDialog(preOfferAnswer);
        // show dialog that call is rejected by the callee
      }
      */
      if (preOfferAnswer === constants.preOfferAnswer.CALL_ACCEPTED) {
        //ui.showCallElements(connectedUserDetails.callType);
        this.createPeerConnection();

      }

    },

    handleWebRTC(message) {
      console.log("handleWebRTC()...");

      const data = JSON.parse(message);   // 解析 JSON 字符串
      switch (data.type) {
      case constants.webRTCSignaling.OFFER:
        webRTCHandler.handleWebRTCOffer(data);
        break;
      case constants.webRTCSignaling.ANSWER:
        webRTCHandler.handleWebRTCAnswer(data);
        break;
      case constants.webRTCSignaling.ICE_CANDIDATE:
        webRTCHandler.handleWebRTCCandidate(data);
        break;
      default:
        return;
      }
    },

    handleBeforeUnload(event) {
      console.log("handleBeforeUnload()...");

      event.preventDefault();   // 防止瀏覽器直接卸載頁面
      event.returnValue = '';   // 必须設置此属性，但任何值都ok
      this.isPageReloading = true;
      // 執行與頁面銷毀前的清理工作
      if (!this.isPageReloading) {
        console.log("not disconnect!");
        SocketioService.disconnect();
        if (SocketioService.socket) {
          SocketioService.socket.off('broadcast', this.handleBroadcastMessage);
        }
      }
    },

    restoreStateFromLocalStorage() {
      console.log("restoreStateFromLocalStorage()...");

      const user_id = sessionStorage.getItem('user_id');
      const sock_id = sessionStorage.getItem('sock_id');
      const local_ip = localStorage.getItem('local_ip');

      if (user_id) {
        this.$store.dispatch('updateUserID', user_id);
      }
      if (sock_id) {
        this.$store.dispatch('updateSockID', sock_id);
      }
      if (local_ip) {
        this.updateLocalIP(local_ip);
      }

      console.log("State restored from localStorage:", { user_id, sock_id, local_ip });
    },
  },

  beforeUnmount() {
    window.removeEventListener('beforeunload', this.handleBeforeUnload);
  },

  beforeDestroy() {
    console.log("beforeDestroy()...", this.isPageReloading);

    if (!this.isPageReloading) {
      console.log("Disconnecting socket...");
      if (SocketioService.socket) {
        console.log("Socket exists. Disconnecting...");
        SocketioService.disconnect();
        console.log("Socket disconnected.");
      } else {
        console.log("Socket not initialized.");
      }
      if (SocketioService.socket) {
        console.log("Removing socket event listener...");
        SocketioService.socket.off('broadcast', this.handleBroadcastMessage);
        console.log("Socket event listener removed.");
      } else {
        console.log("Socket not initialized.");
      }
    }
    console.log("Removing beforeunload event listener...");
    window.removeEventListener('beforeunload', this.handleBeforeUnload);
    console.log("beforeDestroy() completed.");

    //this.stopStream();
    //EventBus.$off('startVideoRequested', this.handleStartVideoRequest);
    EventBus.$off('startVideoRequested', this.startVideo);
    EventBus.$off('pauseVideoRequested', this.pauseVideo);
  },
}
</script>

<style lang="scss" scoped>
@import "@/styles/variables.scss"; // 引入變數檔

.main_container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.dashboard_container {
  width: 25%;
  height: 100%;
  //background: linear-gradient(168.68deg, #0052c9 1.12%, #0a91db 100%);
  //background: #0264ce;
  background: $SYSTEM_COLOR;
  display: flex;
  flex-direction: column;   // 確保子元素垂直排列
  align-items: center;      // 子元素水平居中
  border-radius: 15px;
}
/*
.logo_img {
  width: 100%;
  height: 100%;
  //border-radius: 25px;
  //border: 2px solid #73AD21;
  position: relative;
  top: 50%;
  left: 154px;
  transform: translate(-50%, -50%);
}
*/
/*
.logo_container img {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}
*/
.logo_container img {
  position: absolute;
  top: 50%;
  left: 50%;
  width:100%;
  height: auto;             // 保持寬高比例
  transform: translate(-50%, -50%);
  object-fit: cover;
  object-position: center;
}
.logo_img {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: auto;
  transform: translate(-50%, -50%);
  object-fit: cover;
  object-position: center;
}
/*
.logo_container {
  margin-left: 0px;
  width: 180px;
  height: 120px;
  justify-content: center;
  align-items: center;
}

.logo_container + div {
  width: calc(100% - 40px);
  margin: 0 20px;
}
*/
/*
.logo_container {
  position: relative;
  width: 52%;
  padding-top: 52%;
}
*/
.logo_container {
  position: relative;
  width: 52%;                 //佔總寬度的52%
  padding-top: 52%;
  //height: auto;             //可以設為明確的高度，或者百分比的高度
  display: flex;
  align-items: center;
  justify-content: center;    //水平和垂直居中
  overflow: hidden;           //防止溢出
}

.description_container {
  margin: 0 40px;
}

.description_container_paragraph {
  font-weight: 500;
  font-size: 16px;
  color: white;
}

.personal_code_title_container {
  padding: 0 25px;
}

.personal_code_value_container {
  display: flex;
  justify-content: space-between;
  margin: 0 25px;
  align-items: center;
}

p.personal_code_title_paragraph {
  font-size: 18px;
  font-weight: 500;
}

p.personal_code_value_paragraph {
  font-size: 14px;
  font-weight: 300;
}

.personal_code_container {
  width: calc(100% - 10px);
  height: 110px;
  margin: 0 5px 5px;
  background: rgba(196, 196, 196, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
}

.personal_code_value_container {
  display: flex;
  justify-content: space-between;
  margin: 0 25px;
  align-items: center;
}

.personal_code_connecting_container {
  display: flex;
  flex-direction: column;
  margin: 20px 10px 50px; //margin: 上   [右左]    下;
}

.stranger_connecting_container {
  display: flex;
  flex-direction: column;
  margin: 0 20px; //margin: [上下]   [右左];
}

.personal_code_connecting_buttons_container {
  margin-top: 30px;
  display: flex;
  justify-content: space-between;
}

.call_container {
  width: 50%;
  height: 100%;
}

.call_buttons_container {
  position: absolute;
  width: 395px;
  height: 75px;
  bottom: 40px;
  left: calc(50% - 200px);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.videos_container {
  position: relative;
  //top: 38px;
  //height: calc(100% - 70px);
  height: 100%;
  //margin: 30px 40px 40px 40px;
  margin: 0px 20px 0px 20px;
  border-radius: 15px;
  //background: linear-gradient(168.68deg, #0052c9 1.12%, #0a91db 100%);
  background: #5a96cc;
}

.videos_placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.local_video_container {
  position: absolute;
  //position: relative;
  width: 180px;
  height: 136px;
  //height: auto;
  border: 2px solid rgba(255, 255, 255, 0.5);
  //border-radius: 15px;
  background: rgba(196, 196, 196, 0.2);
  top: 15px;
  left: 15px;
}

.local_video {
  width: 100%;
  //height: auto;
  height: 100%;
}

.remote_video_container {
  position: absolute;
  width: 180px;
  height: 136px;
  border: 2px solid rgba(255, 255, 255, 0.5);
  background: rgba(196, 196, 196, 0.2);
  top: 15px;
  left: 200px;  // 假設將遠端視頻放置在本地視頻的右側
}

.remote_video {
  width: 100%;
  height: 100%;
}

.video-preparing {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.5); /* 半透明背景 */
  color: white;
  font-size: 18px;
  z-index: 1; // 提示文字在最上層
}

.messenger_container {
  width: 25%;
  height: 100%;
  background: #f4f9fd;
  display: flex;
  flex-direction: column;
}

.messages_container {
  flex-grow: 1;
  margin: 40px 30px;
  overflow-y: scroll;
  position: relative;
  right: -28px;
}

.new_message_container {
  position: relative;
}

.stranger_title_container {
  font-size: 16px;
  font-weight: 500;
}

.stranger_buttons_container {
  display: flex;
  justify-content: space-between;
}

.finish_chat_button_container {
  position: absolute;
  width: 395px;
  height: 75px;
  bottom: 40px;
  left: calc(50% - 200px);
  display: flex;
  justify-content: center;
  align-items: center;
}

.checkbox_container {
  display: flex;
  margin: 0 5px;
  margin-bottom: 25px;
  align-items: center;
  width: 100%;
}

.video_recording_buttons_container {
  position: absolute;
  width: 140px;
  height: 50px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 15px;
  backdrop-filter: blur(60px);
  right: 20px;
  top: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
}

.recording_button {
  height: 30px;
  min-width: 0px;
  padding: 0 10px;
}

#dialog {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.flex-container {
  display: flex;
  justify-content: center;
}

.image-container {
  display: flex;
  justify-content: center;
}

.button-container {
  display: flex;
  justify-content: center;
}

.button-container .v-btn:not(:last-child) {
  margin-right: 25px;   //設定按鍵之間的右邊間距
}

.centered-btn {
  align-self: center;   //水平置中顯示
}

/* ok 1
.dashboard_container *,
.call_container *,
.messenger_container * {
  filter: blur(30px) brightness(0.7) saturate(100%) hue-rotate(120deg);
  background: rgba(255, 255, 255, 0.2);
}
*/
/* ok 2
.dashboard_container,
.call_container,
.messenger_container {
  filter: blur(30px) brightness(0.7) saturate(100%) hue-rotate(120deg);
  background: rgba(255, 255, 255, 0.2);
}

.dashboard_container *,
.call_container *,
.messenger_container * {
  filter: blur(30px) brightness(0.7) saturate(100%) hue-rotate(120deg);
  background: rgba(255, 255, 255, 0.2);
}
*/
.blur-effect {
  filter: blur(30px) brightness(0.7) saturate(100%) hue-rotate(120deg);
  background: rgba(255, 255, 255, 0.2);
}

.blur-effect * {
  filter: blur(30px) brightness(0.7) saturate(100%) hue-rotate(120deg);
  background: rgba(255, 255, 255, 0.2);
}


.display_none {
  display: none;
}
.copy_btn {
  //background: transparent;
  //background-color: white;
  //border: 3px solid transparent;
  transition: background-color 0.3s, border-color 0.3s;
}
.copy_btn:hover {
  //color: #fff;
  background: transparent;
  //border: 1px solid #fff
  //background-color: black;
  border: 2px solid white;
}

.chat_btn {
  transition: background-color 0.3s, border-color 0.3s;
}
.chat_btn:hover {
  background: transparent;
  border: 2px solid white;
}

.video_btn {
  transition: background-color 0.3s, border-color 0.3s;
}
.video_btn:hover {
  background: transparent;
  border: 2px solid white;
}

.center_hor {
  margin: 0 auto;
}
</style>