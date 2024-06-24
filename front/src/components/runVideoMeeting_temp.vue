<template>
<v-app>
  <v-container fluid class="web-camera-container">

  <vue-web-cam ref="camera"></vue-web-cam>
  <v-btn rounded @click="captureImage">拍照</v-btn>

  </v-container>
</v-app>
</template>

<script>
import axios from 'axios';

import { WebCam } from 'vue-web-cam';

import Common from '../mixin/common';

export default {
  name: 'runVideoMeeting',

  mixins: [Common],

  components: {
    'vue-web-cam': WebCam,
  },

  computed: {

  },

  watch: {
    isCameraOpen(val) {
      !val || this.startCameraStream();
    },

  },

  created() {

  },

  mounted() {

  },

  data() {
    return {
      currentUser: {
      },
      isCameraOpen: true,
      isPhotoTaken: false,
      isShotPhoto: false,
      isLoading: false,

      roomId: 'roomId',

      localStream: null,
      remoteStream: null,
      localPeerConnection: null,
      remotePeerConnection: null
    };
  },

  methods: {
    captureImage() {
      this.$refs.camera.capture()
      .then((imageData) => {
        console.log("imageData:", imageData)
      })
    },

    toggleCamera() {
      if (this.isCameraOpen) {
          this.isCameraOpen = false;
          this.isPhotoTaken = false;
          this.isShotPhoto = false;
          this.stopCameraStream();
      } else {
          this.isCameraOpen = true;
          this.createCameraElement();
      }
    },

    createCameraElement() {
      this.isLoading = true;
      const constraints = (window.constraints = {
				audio: false,
				video: true
			});

			navigator.mediaDevices.getUserMedia(constraints)
      .then(stream => {
        this.isLoading = false;
        this.$refs.camera.srcObject = stream;
      })
      .catch(error => {
        this.isLoading = false;
        alert("May the browser didn't support or there is some errors.");
      });
    },

    stopCameraStream() {
      let tracks = this.$refs.camera.srcObject.getTracks();

			tracks.forEach(track => {
				track.stop();
			});
    },

    takePhoto() {
      if (!this.isPhotoTaken) {
        this.isShotPhoto = true;

        const FLASH_TIMEOUT = 50;

        setTimeout(() => {
          this.isShotPhoto = false;
        }, FLASH_TIMEOUT);
      }

      this.isPhotoTaken = !this.isPhotoTaken;

      const context = this.$refs.canvas.getContext('2d');
      context.drawImage(this.$refs.camera, 0, 0, 450, 337.5);
    },

    downloadImage() {
      const download = document.getElementById("downloadPhoto");
      const canvas = document.getElementById("photoTaken").toDataURL("image/jpeg")
    .replace("image/jpeg", "image/octet-stream");
      download.setAttribute("href", canvas);
    },


    async startCall() {
      try {
        // Get local media stream
        this.localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        this.$refs.localVideo.srcObject = this.localStream;

        // Create local peer connection
        this.localPeerConnection = new RTCPeerConnection();
        this.localStream.getTracks().forEach(track => this.localPeerConnection.addTrack(track, this.localStream));

        // Create remote peer connection
        this.remotePeerConnection = new RTCPeerConnection();

        // Set up event handlers for local peer connection
        this.localPeerConnection.onicecandidate = event => {
          if (event.candidate) {
            this.remotePeerConnection.addIceCandidate(event.candidate);
          }
        };

        // Set up event handlers for remote peer connection
        this.remotePeerConnection.onicecandidate = event => {
          if (event.candidate) {
            this.localPeerConnection.addIceCandidate(event.candidate);
          }
        };
        this.remotePeerConnection.ontrack = event => {
          this.remoteStream = event.streams[0];
          this.$refs.remoteVideo.srcObject = this.remoteStream;
        };

        // Set up offer/answer negotiation
        this.localPeerConnection.createOffer()
          .then(offer => this.localPeerConnection.setLocalDescription(offer))
          .then(() => this.remotePeerConnection.setRemoteDescription(this.localPeerConnection.localDescription))
          .then(() => this.remotePeerConnection.createAnswer())
          .then(answer => this.remotePeerConnection.setLocalDescription(answer))
          .then(() => this.localPeerConnection.setRemoteDescription(this.remotePeerConnection.localDescription))
          .catch(error => console.error('Error creating WebRTC offer/answer: ', error));
      } catch (error) {
        console.error('Error accessing media devices: ', error);
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.web-camera-container {
  margin-top: 2rem;
  margin-bottom: 2rem;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 500px;
}

.web-camera-container .camera-button {
  margin-bottom: 2rem;
}

.web-camera-container .camera-box .camera-shutter {
  opacity: 0;
  width: 450px;
  height: 337.5px;
  background-color: #fff;
  position: absolute;
}

.web-camera-container .camera-box .camera-shutter.flash {
  opacity: 1;
}

.web-camera-container .camera-shoot {
  margin: 1rem 0;
}

.web-camera-container .camera-shoot button {
  height: 60px;
  width: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 100%;
}

.web-camera-container .camera-shoot button img {
  height: 35px;
  object-fit: cover;
}

.web-camera-container .camera-loading {
  overflow: hidden;
  height: 100%;
  position: absolute;
  width: 100%;
  min-height: 150px;
  margin: 3rem 0 0 -1.2rem;
}

.web-camera-container .camera-loading ul {
  height: 100%;
  position: absolute;
  width: 100%;
  z-index: 999999;
  margin: 0;
}

.web-camera-container .camera-loading .loader-circle {
  display: block;
  height: 14px;
  margin: 0 auto;
  top: 50%;
  left: 100%;
  transform: translateY(-50%);
  transform: translateX(-50%);
  position: absolute;
  width: 100%;
  padding: 0;
}

.web-camera-container .camera-loading .loader-circle li {
  display: block;
  float: left;
  width: 10px;
  height: 10px;
  line-height: 10px;
  padding: 0;
  position: relative;
  margin: 0 0 0 4px;
  background: #999;
  animation: preload 1s infinite;
  top: -50%;
  border-radius: 100%;
}

.web-camera-container .camera-loading .loader-circle li:nth-child(2) {
  animation-delay: 0.2s;
}

.web-camera-container .camera-loading .loader-circle li:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes preload {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
  100% {
    opacity: 1;
  }
}
</style>
