<template>
  <v-app>
    <div class="container" :class="{'sign-up-active' : signUp}">
      <div class="overlay-container">
        <div class="overlay">
          <div class="overlay-left">
            <h4>
              <!--<img :src="home_url"  alt="..." style="height: 4vw; margin-bottom: 10px;">-->
              {{'跑合間儲位管理系統'}}
            </h4>
            <button class="invert" id="signIn" @click="signUp = !signUp">登入</button>
          </div>

          <div class="overlay-right">
            <h4>
              <!--<img :src="home_url"  alt="..." style="height: 4vw; margin-bottom: 10px;">-->
              {{'跑合間儲位管理系統'}}
            </h4>
            <button class="invert" id="signUp" @click="signUp = !signUp">註冊</button>
          </div>
        </div>
      </div>
      <div class="sign-up">
        <h3>{{ '註冊' }}</h3>
        <v-text-field
          id="registerEmpID"
          label="員工編號"
          name="EmpID"
          class="text-teal"
          prepend-icon="mdi-account"
          type="text"
          required
          v-model='registerUser.empID'
          single-line
          :rules="rulesForEmpID"
          counter
          maxlength="4"
          @keydown="handleKeyDown"
          @blur="handleBlur"
        />
        <!-- {{ ErrMsg }} -->
        <small class="msgErr" v-text= "empIDErrMsg"></small>

        <v-text-field
          id="registerName"
          label="員工姓名"
          name="Name"
          class="text-teal"
          prepend-icon="mdi-account-edit"
          type="text"
          required
          v-model='registerUser.name'
        />
        <!-- {{ ErrMsg }} -->
        <small class="msgErr" v-text= "nameErrMsg"></small>
        <!--
        <v-select
          :items="desserts"
          label="組別"
          name="Dep"
          class="text-teal"
          prepend-icon="mdi-account-group"
          required
          v-model='registerUser.dep'
        ></v-select>
        -->
        <!-- {{ ErrMsg }} -->
        <!--<small v-text= "depErrMsg"></small>-->
        <v-text-field
          id="registerPassword"
          label="密碼"
          name="Password"
          class="text-teal"
          prepend-icon="mdi-lock"
          required
          :append-icon="eyeShow1 ? 'mdi-eye-off' : 'mdi-eye'"
          @click:append="() => (eyeShow1 = !eyeShow1)"
          :type="eyeShow1 ? 'password' : 'text'"
          v-model='registerUser.password'
          single-line
          :rules="rulesForEmpPass"
          counter
          maxlength="6"

        />
        <!-- {{ ErrMsg }} -->
        <small class="msgErr" v-text= "passwordErrMsg"></small>

        <v-text-field
          id="registerConfirmPassword"
          label="確認密碼"
          name="Confirm"
          class="text-teal"
          prepend-icon="mdi-account-check"
          required
          :type="eyeShow1 ? 'password' : 'text'"
          :rules="[rulesForPSW]"
          v-model='registerUser.confirmPassword'
          single-line
          counter
          maxlength="6"
        />

        <!-- {{ ErrMsg }} -->
        <!--
        <b-toast v-show="!registerOK" title="BootstrapVue" static no-auto-hide>
              Hello, world! This is a toast message.
        </b-toast>
        -->
        <Toaster v-show="tosterRegOK"
          :Title="tosterTitlt"
          :Type="tosterType"
          :Body="tosterBody"
          :Timeout="tosterTimeout"
           @removeToaster="onRemoveToaster"
        >
        </Toaster>

        <button @click="register">註冊</button>
        <!--<button @click="register" :disabled='checkRegisterUserForSaveButton'>註冊</button>-->
        <!--<small class="clickRegErr" v-text= "clickRegisterErrMsg"></small>-->
      </div>

      <div class="sign-in">
        <h3>{{ '登入' }}</h3>
        <v-text-field
          id="loginEmpID"
          label="員工編號"
          name="EmpID"
          class="text-teal"
          prepend-icon="mdi-account"
          type="text"
          v-model='loginEmpID'
          single-line
          :rules="rulesForEmpID"
          counter
          maxlength="4"
          @keydown="handleKeyDown"
        />

        <v-text-field
          id="loginPassword"
          label="密碼"
          name="Password"
          class="text-teal"
          prepend-icon="mdi-lock"
          :append-icon="eyeShow ? 'mdi-eye-off' : 'mdi-eye'"
          @click:append="() => (eyeShow = !eyeShow)"
          :type="eyeShow ? 'password' : 'text'"
          v-model='loginPassword'
          @keyup.enter="signin"
        />
        <!--<a href="#">{{ '忘記密碼' }}</a>-->

        <!-- {{ ErrMsg }} -->
        <!--<small class="clickLgnErr" v-text= "clickLoginErrMsg"></small> -->
        <Toaster v-show="tosterOK"
          :Title="tosterTitlt"
          :Type="tosterType"
          :Body="tosterBody"
          :Timeout="tosterTimeout"
           @removeToaster="onRemoveToaster"
        >
        </Toaster>
        <button @click="userLogin">登入</button>
        <BR />  <p style="margin: 0px 0 30px;"> {{ 'Build 2024-05-07' }} </p>
      </div>

    </div>
  </v-app>
</template>

<script>
import axios from 'axios';

//import header from '../assets/image/china_header.png'

import Toaster from '../components/Toaster.vue';

import Common from '../mixin/common.js'
import Key from '../mixin/key.js'

//import { _thetaPasswordMaxLength, _thetaPasswordMinLength } from '../mixin/constant.js';

export default {
  name: 'LoginForm',

  mixins: [Common, Key],

  components: {
    Toaster,
  },

  data() {
    return {
      //home_url: header,
      signUp: false,    //初始畫面為登入畫面

      myPicker: {},

      tosterTitlt: 'Hello',
      tosterType: 'error',
      tosterBody: '資料錯誤或空白, 請重新輸入...',
      tosterTimeout: '3',

      loginEmpID: null,
      loginPassword: null,
      loginOK: false,       //true: 登入成功
      registerOK: false,    //true: 註冊成功
      tosterOK: false,
      tosterRegOK: false,

	    empIDErrMsg: '',
      nameErrMsg: '',
      passwordErrMsg: '',
      clickLoginErrMsg: '',       //登入錯誤訊息
      clickRegisterErrMsg: '',    //註冊錯誤訊息

      password_violate_count: 0,  //password按錯違規次數, 最多5次

      eyeShow: true,
      eyeShow1: true,
      eyeShow2: true,

      registerUser: {
		    empID: null,
        name: null,
				dep: null,
				password: null,
				confirmPassword: null,
	    },

      desserts: [],
      temp_desserts: [],

      loginedUser: {
				emp_id: null,
        emp_name: null,
				emp_dep: 0,
        emp_dep_name: null,
        emp_perm: 0,
        emp_perm_name: null,
        password: '',
      },

      //rules: {
      //  required: value => !!value || 'Required.',
      //},

      //rulesForEmpID: [v => v.length <= 4 || '最大4位數字'],
      rulesForEmpID: [v => !v || v.length <= 4 || '最大4位數字'],
      rulesForEmpPass: [v => !v || v.length >= 4  || v.length <= 6 || '4~6位數'],
      rulesForEmpCfrPass: [v => !v || v.length >= 4  || v.length <= 6 || '4~6位數'],
      load_SingleTable_ok: false,   //for get department table data
    };
  },

  mounted() {
    let myIdField=document.getElementById("loginEmpID")
    myIdField.addEventListener( 'keydown', function( event ) {
      var caps = event.getModifierState && event.getModifierState( 'CapsLock' );
      console.log( "CapsLock is: ", caps ); // true when you press the keyboard CapsLock key
      //if (!caps) {
      //  char = char.toUpperCase();
      //}
    });
  },

  created() {

    this.initAxios();

    this.initialize();
  },

  beforeCreate () {

  },

  beforeDestroy () {

  },

  computed: {
    rulesForPSW() {
      return () => (this.registerUser.password === this.registerUser.confirmPassword) || '密碼不相同!'
    },

    checkRegisterUserForSaveButton() {
      if (!!this.registerUser.emp_id && !!this.registerUser.emp_name &&
          !!this.registerUser.dep &&
          !!this.registerUser.password && !!this.registerUser.confirmPassword &&
          this.empIDErrMsg == '' && this.nameErrMsg == '' && this.passwordErrMsg == '' &&
          this.registerUser.password === this.registerUser.confirmPassword) {
        return false;
      } else {
        return true
      }
    },
  },

  watch: {
    signUp(val) {
      this.registerUser.empID='';
      this.registerUser.name='';
      this.registerUser.password='';
      this.registerUser.confirmPassword='';

      this.empIDErrMsg = '';
      this.nameErrMsg = '';
      this.passwordErrMsg='';
    },

    loginOK(val) {
      console.log("loginOK is: ", val);
      this.signin();
    },

    myPicker(value) {
      if (value.toString().match(/^[a-z]\d{4}$/)) {     // 密碼格式: 第1個字為小寫字母, 再接4個數字,長度為5個字元
          this.myPicker = value.substr(0, 5);           // 長度為5個字元
      }
    },

    load_SingleTable_ok(val) {
      if (val) {
        this.desserts = this.temp_desserts.map(item => Object.values(item)[0]); //從object中copy value至array
      }
    },

    'registerUser.empID': function (val) {
      let isEmpIDRule = /[0-9]{4}$/;  // 長度為4個數字
      let result = val.search(isEmpIDRule);
      //let len=this.registerUser.empID.length
      //this.empIDErrMsg = '';
      //if (result == -1) {
      //  this.empIDErrMsg = '員工編號資料格式錯誤!';
      //}
      if (result != -1) {
        this.empIDErrMsg = '';
      }
    },	//end 'empID': function()

    'registerUser.name': function () {
      let len=(this.registerUser.name==null)? 0: this.registerUser.name.length
      this.nameErrMsg = '';
      if (len > 10) {
        this.nameErrMsg = '資料長度太長!';
      }
    },	//end 'name': function()

    'registerUser.password': function () {
      //console.log("_thetaPasswordMinLength, _thetaPasswordMaxLength", _thetaPasswordMinLength, _thetaPasswordMaxLength)
      //Regular expression
      let isPasswordRule = /^(?=.*\d)(?=.*[a-z])[0-9a-zA-Z]{4,6}$/; // 密碼格式: 第1個字為英文字母, 再接4~6個數字或英文字母
      let result = this.registerUser.password.match(isPasswordRule);
      let len=this.registerUser.password.length;
      console.log("result: ", this.registerUser.password, result);
      this.passwordErrMsg = '';
      if (result == null && (len>=4 && len<=6)) {
      //if (result == null) {
        console.log("error...");
        this.passwordErrMsg = '資料格式或資料長度錯誤!';
      }
    },  //end 'password': function()
  },

  methods: {
    onRemoveToaster(val) {
      this.tosterOK=false;
      this.tosterRegOK=false;
    },

    initialize () {
      /*
      const path='/listDepartments';
      axios.get(path)
      .then((res) => {
        this.temp_desserts = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length, res.data.outputs);
        this.load_SingleTable_ok = true;  //true: 資料download成功
      })
      .catch((error) => {
        console.error(error);
        this.load_SingleTable_ok = false;
      });
      */
    },

    register() {
      console.log("---click_register---");
      this.signUp = true;  //true: 註冊畫面
      const path='/register';
      var payload= {
        emp_id: this.registerUser.empID,
        emp_name: this.registerUser.name,
        password: this.registerUser.password,
        dep: this.registerUser.dep,
      };
      axios.post(path, payload)
      .then(res => {
        console.log("register status: ", res.data.status)
        this.registerOK= res.data.status;
        if (this.registerOK) {
          this.tosterRegOK = false;  //false: 關閉錯誤訊息畫面

          this.registerUser={
            empID: '',
            name: '',
            dep: '',
            password: '',
            confirmPassword: '',
	        };

          this.signUp=false;  //false: 登入畫面
        } else {
          this.tosterRegOK = true;   //true: 顯示錯誤訊息畫面
          this.signUp=true;   //true: 註冊畫面
        }
      })
      .catch(err => {
        console.error(err);
        this.registerOK= false;
      });
    },

    userLogin() {
    console.log("---click_login---");

      const path='/login';
      var payload= {
        password: this.loginPassword,
        empID: this.loginEmpID,
      };
      this.clickLoginErrMsg='';
      axios.post(path, payload)
      .then(res => {
        console.log("login, post ok", res.data)
        this.loginOK= res.data.status;
        if (this.loginOK) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          this.loginedUser = Object.assign({}, res.data.user);
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        }
      })
      .catch(err => {
        console.error(err);
        this.loginOK= false;
      });
    },

    signin() {
      console.log("---click_signin---");
      this.removeLoginUser();

      let isAuthenticated=true;
      this.setAuthenticated(isAuthenticated);
      this.setLoginUser();
      this.$router.push('/navbar');
    },

    removeLoginUser() {
      localStorage.removeItem('loginedUser');
    },

    setLoginUser() {
      localStorage.setItem('loginedUser', JSON.stringify(this.loginedUser));
      localStorage.setItem('totalTags', 0);   //待入庫列印標籤總數清為0
      console.log("---click_signin---", this.loginedUser);
    },

    setAuthenticated(isLogin) {
      localStorage.setItem('Authenticated', isLogin)
    },
    /*
    handleKeyDown(event) {
      // 檢查按鍵是否為負號或超出範圍
      const numValue = parseInt(event.target.value + event.key);
      if (isNaN(numValue)) {
        console.log("handleKeyDown... Not number!")
        // 阻止事件的預設行為，即不允許輸入
        event.preventDefault();
      }
    },
    */
    handleBlur(event) {
      let len=(this.registerUser.empID==null) ? 0:this.registerUser.empID.length
      this.empIDErrMsg = '';
      if (len != 4) {
        this.empIDErrMsg = '員工編號資料格式錯誤!';
      }
    }
  },
};
</script>

<style lang="scss" scoped>
@import url(
  'https://fonts.googleapis.com/css?family=Noto+Sans+TC:400,500&display=swap&subset=chinese-traditional'
);

#app {
  background: #092525;
}

.container {
  position: relative;
  width: 768px;
  height: 480px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2), 0 10px 10px rgba(0, 0, 0, 0.2);
  background: linear-gradient(to bottom, #efefef, #ccc);
  margin-top: 10vh;

  .overlay-container {
    position: absolute;
    top: 0;
    left: 50%;
    width: 50%;
    height: 100%;
    overflow: hidden;
    transition: transform 0.5s ease-in-out;
    z-index: 100;
  }

  .overlay {
    position: relative;
    left: -100%;
    height: 100%;
    width: 200%;
    background: linear-gradient(to bottom right, #96b8de, #5a96cc);
    color: #fff;
    transform: translateX(0);
    transition: transform 0.5s ease-in-out;
  }

  @mixin overlays($property) {
    position: absolute;
    top: 0;
    display: flex;
    align-items: center;
    justify-content: space-around;
    flex-direction: column;
    padding: 70px 40px;
    /*width: calc(50% - 80px);*/
    width: calc(50% - 40px);
    height: calc(100% - 140px);
    text-align: center;
    transform: translateX($property);
    transition: transform 0.5s ease-in-out;
  }

  .overlay-left {
    @include overlays(-20%);
  }

  .overlay-right {
    @include overlays(0);
    right: 0;
  }
}

h2, h3 {
  margin: 0;
  font-family: "Noto Sans TC", "Microsoft Yahei", "微軟雅黑", sans-serif;
}

p {
  margin: 20px 0 30px;
}

a {
  color: #222;
  text-decoration: none;
  margin: 15px 0;
  font-size: 1rem;
}

button {
  border-radius: 20px;
  border: 1px solid #5a96cc;
  background-color: #5a96cc;
  color: #fff;
  font-size: 1rem;
  font-weight: bold;
  padding: 10px 40px;
  margin-top: 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
  cursor: pointer;
  transition: transform 0.1s ease-in;

  &:active {
    transform: scale(0.9);
  }

  &:focus {
    outline: none;
  }
}

button.invert {
  background-color: transparent;
  border-color: #fff;
}

div.sign-in, div.sign-up {
  position: absolute;
  top: 0;
  display: flex;
  align-items: center;
  justify-content: space-around;
  flex-direction: column;
  padding: 90px 60px;
  /*width: calc(50% - 120px);*/
  width: calc(50% - 0px);
  /*height: calc(100% - 180px);*/
  height: calc(100% - 0px);
  text-align: center;
  background: linear-gradient(to bottom, #efefef, #ccc);
  transition: all 0.5s ease-in-out;

  div {
    font-size: 1rem;
  }


}

.sign-in {
  left: 0;
  z-index: 2;
}

.sign-up {
  left: 0;
  z-index: 1;
  opacity: 0;
}

.sign-up-active {
  .sign-in {
    transform: translateX(100%);
  }

  .sign-up {
    transform: translateX(100%);
    opacity: 1;
    z-index: 5;
    animation: show 0.5s;
  }

  .overlay-container {
    transform: translateX(-100%);
  }

  .overlay {
    transform: translateX(50%);
  }

  .overlay-left {
    transform: translateX(0);
  }

  .overlay-right {
    transform: translateX(20%);
  }
}

@keyframes show {
  0% {
    opacity: 0;
    z-index: 1;
  }
  49% {
    opacity: 0;
    z-index: 1;
  }
  50% {
    opacity: 1;
    z-index: 10;
  }
}

button.v-icon {
  /*background: yellow;*/
  padding-left: 10px;
  padding-right: 10px;
  height: 20px;
  width: 30px;
  border-style: none;
  background: linear-gradient(to bottom, #efefef, #ccc);
  margin-left: calc(100% + 50px);
}

.v-text-field {
  min-width: 17vw;;
}
/*
.text-teal input {
  color: #4dc0b5 !important;
}

.text-teal input::placeholder {
  color: red!important;
  opacity: 1;
}
*/
.text-teal .v-label {
  color: #909090;
  opacity: 1;
  font-size: 16px;
}

.v-messages__message {
  color: #FF5c4E;
  font-size: 12px;
}

small.msgErr {
  font-size: 80%;
  color: red;
  margin-top: -20px;
}

small.clickLgnErr {
  font-size: 100%;
  color: red;
  margin-top: -60px;
  animation: blinker 0.5s linear infinite;
}

small.clickRegErr {
  font-size: 100%;
  color: red;
  margin-top: -40px;
  animation: blinker 0.5s linear infinite;
}

@keyframes blinker {
  50% {
    opacity: 0;
  }
}
</style>
