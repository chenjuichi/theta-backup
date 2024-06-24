<template>
<v-app>
  <b-navbar justified type="dark" variant="dark" class="navbar custom-nav fixed-top" expand="lg" light bg="light">
    <b-navbar-brand>
      <img :src="home_url"  alt="..." style="height: 4vw;">
    </b-navbar-brand>
    <b-navbar-nav style="margin-left: 100px;">
      <b-nav-item href="#">首頁</b-nav-item>
      <div v-for="navbar in navbars" :key="navbar.id">
        <b-nav-item-dropdown v-if="navbar.id !== 2 && navbar.id !== 3 && navbar.id !== 4" :text="navbar.text" @click.prevent="open=!open" right>
          <b-dropdown-item :to="navbar.router1">
            <b-avatar variant="success" :icon="navbar.icon1" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
            {{ navbar.name1 }}
          </b-dropdown-item>

          <b-dropdown-item :to="navbar.router2">
            <b-avatar variant="success" :icon="navbar.icon2" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
            {{ navbar.name2 }}
          </b-dropdown-item>

          <b-dropdown-item :to="navbar.router3">
            <b-avatar variant="success" :icon="navbar.icon3" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
            {{ navbar.name3 }}
            <v-badge color="green" variant="light" :content="navBar_in_drafTags" v-show="navbar.id==2 && navBar_in_drafTags!=0"></v-badge>
            <v-badge color="green" variant="light" :content="navBar_out_drafTags" v-show="navbar.id==3 && navBar_out_drafTags!=0"></v-badge>
          </b-dropdown-item>

          <b-dropdown-item :to="navbar.router4">
            <b-avatar variant="success" :icon="navbar.icon4" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
            {{ navbar.name4 }}
          </b-dropdown-item>

          <b-dropdown-item :to="navbar.router5">
            <b-avatar variant="success" :icon="navbar.icon5" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
            {{ navbar.name5 }}
          </b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item v-else @click="$router.push(navbar.router1)">
          <!-- 直接导航到 router1: "/inTag" 的操作 -->
          {{ navbar.text }}
        </b-nav-item>
      </div>
    </b-navbar-nav>
    <b-navbar-nav class="ml-auto">
          <em>{{ currentUser.name }}</em>
      <b-nav-item-dropdown right>
          <!-- Using 'button-content' slot -->


        <!--<b-dropdown-item href="#">Profile</b-dropdown-item>-->
        <b-dropdown-item href="#" @click="logout">

            <div>
              <!--<b-icon-arrow-up></b-icon-arrow-up>-->
              <!--<p class="h5 mb-2">-->
                <!--<b-icon icon="exclamation-circle-fill"></b-icon>-->
                <!--<b-icon icon="box-arrow-left" font-scale="1" style="color: #ff0000;"></b-icon>-->
                <b-avatar variant="danger" icon="box-arrow-left" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
                登出
              <!--</p>-->
            </div>

        </b-dropdown-item>

        <b-dropdown-item href="#" @click="changePassword">

            <div>
                <b-avatar variant="primary" icon="pencil-square" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
                修改密碼
            </div>

        </b-dropdown-item>

        <b-dropdown-item href="#" @click="$router.push('/camera')">
          <div>
              <b-avatar variant="primary" icon="pencil-square" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
              視訊
          </div>
        </b-dropdown-item>

        <b-dropdown-item href="#">

            <div>
                <b-avatar variant="primary" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
                關於 build 2024-05-07
            </div>

        </b-dropdown-item>


      </b-nav-item-dropdown>
    </b-navbar-nav>
  </b-navbar>

  <!--<ChangePassword :dialog_data="openDialog" @changePassword="onModifyPassword"></ChangePassword>-->
  <ChangePassword :dialog_data="openDialog"></ChangePassword>
  <div :style="inlineStyle"></div>
</v-app>
</template>

<script>
import axios from 'axios';

import Common from '../mixin/common.js'

import logo from '../assets/image/theta_logo.png'
import main_pic from '../assets/image/Company-img-02.jpg'

import ChangePassword from '../components/changePassword.vue';

// Note: Vue automatically prefixes the directive name with 'v-'
//import { VBHover } from 'bootstrap-vue'
import { VBVisible } from 'bootstrap-vue'

import { _createCSSWithConstants } from '../mixin/constant.js';

export default {
  name: 'Navbar',

  directives: {
    //'b-hover': VBHover
    'b-visible': VBVisible
  },

  mixins: [Common],

  components: {
    ChangePassword,
  },

  computed: {
    inlineStyle () {
      return {
        backgroundImage: `url(`+ this.main_pic_url +`)`,
        position: `fixed`,
        height: `100vh`,
        width: `100vw`,
        top: `16vh`,
        //backgroundPosition: `center`
      }
    },

    user_id() {
      return this.$store.getters.user_id;
    },
    sock_id() {
      return this.$store.getters.sock_id;
    },
    local_ip() {
      return this.$store.getters.local_ip;  // 从 Vuex 获取 local_ip
    },
  },

  watch: {
    load_SingleTable_ok(val) {
      if (val) {
        this.count_in = this.temp_count_in;
        this.navBar_in_drafTags = this.temp_count_in;
        console.log("navbar, ready total InTags: ", this.navBar_in_drafTags);

        this.load_SingleTable_ok=false;
        this.listStockOutTagPrintCount();
      }
    },

    load_2thTable_ok(val) {
      if (val) {
        this.count_out = this.temp_count_out;
        this.navBar_out_drafTags = this.temp_count_out;
        console.log("navbar, ready total OutTags: ", this.navBar_out_drafTags);

        this.load_2thTable_ok=false;
      }
    },
  },

  created() {
    _createCSSWithConstants();

    //disabled browser's back key
    //history.pushState(null, null, location.href);
    //window.onpopstate = function () {
    //  history.go(1);
    //};

    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    console.log("current user:",this.currentUser);

    this.load_SingleTable_ok=false;
    this.initAxios();

    //this.listStockInTagPrintCount();
  },

  destoyed() {
    clearInterval(this.myTimer);
  },

  beforeRouteLeave(to, from, next) {
    clearInterval(this.myTimer);
    next();
  },

  mounted() {
    //this.$store.dispatch('clearStorage');
    this.checkConnection();
    //this.navBar_in_drafTags=this.$route.params.in_drafTags;
    //if (typeof(this.navBar_in_drafTags) === 'undefined') {
    //  this.navBar_in_drafTags=0;
    /* 2022-12-7, remove
    let temp=localStorage.getItem("totalTags")
    if(typeof(temp)=='undefined' || temp==null)
        this.navBar_in_drafTags=0;
    else
      this.navBar_in_drafTags=parseInt(temp);
    */
    //if ("totalTags" in localStorage) {
    //  this.navBar_in_drafTags=localStorage.getItem("totalTags")
      //console.log("router undefine!")
    //} else {
    //  this.navBar_in_drafTags=0;
    //  localStorage.setItem("totalTags", 0);
    //}
    //2022-12-7, remove, console.log("navbar, totalTags: ", this.navBar_in_drafTags);
    //this.navBar_in_drafTags=2;

    //====
    this.myTimer = setInterval(this.checkConnection, 10000);  //每10秒check server連線概況

    this.$root.$on('bv::dropdown::show', bvEvent => {
      if (bvEvent.componentId === 'dropdown-1') {
        this.isDropdown1Visible = true;
      }

      if (bvEvent.componentId === 'dropdown-2') {
        this.isDropdown2Visible = true;
      }
    })

    this.$root.$on('bv::dropdown::hide', bvEvent => {
      if (bvEvent.componentId === 'dropdown-1') {
        this.isDropdown1Visible = false;
      }
      if (this.isDropdown1Visible) {
        bvEvent.preventDefault()
      }

      if (bvEvent.componentId === 'dropdown-2') {
        this.isDropdown2Visible = false;
      }
      if (this.isDropdown2Visible) {
        bvEvent.preventDefault()
      }
    })
    //===
    //disableBackButton
    window.history.pushState(null, "", window.location.href);
    window.onpopstate = () => {
      window.history.pushState(null, "", window.location.href);
    };

  },

  data() {
    return {
      openDialog: false,
      openVideoDialog: false,
      open: false,
      navBar_in_drafTags: 0,
      navBar_out_drafTags: 0,

      //navBar_newTags: 0,

      subMenu: false,
      isDropdown1Visible: false,
      isDropdown2Visible: false,

      home_url: logo,
      main_pic_url: main_pic,
      currentUser: {},
      navbars: [
        { id: 1,
          text: "資料維護",
          icon1: "person-plus", name1: "人員資料", router1: "/emp",
          icon2: "person-lines-fill", name2: "人員權限", router2: "/perm",
          icon3: "clipboard-data", name3: "主軸產品", router3: "/spindle",
          icon4: "bookshelf", name4: "主軸跑合儲位", router4: "/grid",
          icon5: "people", name5: "主軸跑合資料", router5: "/runIn",
        },
        { id: 2,
          text: "主軸入庫",
          icon1: "bookmark-plus", name1: "主軸入庫作業", router1: "/inTag",
          //icon2: "bag-plus", name2: "入庫標籤列印", router2: "/inTagPrint",
          //icon3: "cart-plus", name3: "待入庫作業", router3: "/stockIn",
        },
        { id: 3,
          text: "主軸出庫",
          //icon1: "cart-dash", name1: "待出庫作業", router1: "/stockOut",
          icon1: "bookmark-dash", name1: "主軸出庫作業", router1: "/outTag",
          //icon2: "bag-dash", name2: "出庫標籤列印", router2: "/outTagPrint",
          //icon3: "cart-dash", name3: "待出庫作業", router3: "/stockOut",
        },
        { id: 4,
          text: "在庫紀錄",
          icon1: "calendar2-check", name1: "在庫紀錄查詢", router1: "/stockRec",
          //icon1: "cart-dash", name1: "領用記錄查詢", router1: "/reqRec",
          //icon2: "calendar2-check", name2: "在庫紀錄查詢", router2: "/stockRec",
          //icon3: "upc-scan", name3: "盤點作業", router3: "/invent",
          //icon4: "printer", name4: "補印標籤", router4: "/reprintTag",
          //icon5: "cart-plus", name5: "入庫記錄查詢", router5: "/storageRec",
          //icon6: "chat-square-text", name6: "校正記錄查詢", router6: "/correction",
        },
      ],

      count_in: 0,
      temp_count_in: 0,
      count_out: 0,
      temp_count_out: 0,

      isOnline: true,
      myTimer: '',            //在component內設定timer, timer的handle

      load_SingleTable_ok: false, //for get stockin table data
      load_2thTable_ok: false,    //for get reagent table data
    };
  },

  methods: {
    /*
    listStockInTagPrintCount() {
      const path = '/listStockInTagPrintCount';
      console.log("listStockInTagPrintCount, Axios get data...")
      axios.get(path)
      .then((res) => {
        this.temp_count_in = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_SingleTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.load_SingleTable_ok=false;
      });
    },

    listStockOutTagPrintCount() {
      const path = '/listStockOutTagPrintCount';
      console.log("listStockOutTagPrintCount, Axios get data...")
      axios.get(path)
      .then((res) => {
        this.temp_count_out = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_2thTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.load_2thTable_ok=false;
      });
    },
    */
    changePassword() {
      this.openDialog=true;
    },

    /*
    async onModifyPassword(value) {
        let path='/updatePassword';
        let payload= {
          newPassword: value,
          empID: currentUser.emp_id,
        };

        try {
          let res = await axios.post(path, payload);
          console.log("change password ok", res.data.status);
        } catch (err) {
          console.error(err)
        }
    },
    */
    logout() {
      console.log("logout...");
      this.updateSetting();
      let isAuthenticated=false;
      this.setAuthenticated(isAuthenticated);
      this.removeLoginUser();
      if (this.$route.path != '/') {
        this.$router.push('/');
      }
    },

    updateSetting() {
      console.log("hello setting...")

      const userData = JSON.parse(localStorage.getItem('loginedUser'));
      let path='/updateSetting';
      let payload= {
        setting: userData.setting_items_per_page,
        empID: userData.empID,
      };

      axios.post(path, payload)
      .then(res => {
          console.log("update user's setting ok", res.data.status);
      })
      .catch(err => {
          console.error(err);
      });
    },

    removeLoginUser() {
      localStorage.removeItem('loginedUser');
    },

    setAuthenticated(isLogin) {
      localStorage.setItem('Authenticated', isLogin)
    },

    handleHover(e) {
      console.log("nav-dropdown key press: ", e);
    },

    async checkConnection() {
      try {
        let res = await this.fetchFunction();
        this.isOnline = res.status >=200 && res.status < 300;
      } catch (e) {
        this.isOnline = false;
        throw e;
      };

      console.log("Application is ", this.isOnline);
    },

    fetchFunction() {
      console.log("fetchFunction()...");

      //return axios.get('/hello');
      const path = '/hello';
      return axios.get(path)
      .then((res) => {
        let temp_local_ip = res.data.local_ip;
        console.log("temp_local_ip:", temp_local_ip)
        this.$store.dispatch('updateLocalIP', temp_local_ip);
        return res;
      })
      .catch((error) => {
        console.error(error);
        throw error;
      });
    },
  },
}
</script>

<style scoped lang="scss">
  @import url(
    'https://fonts.googleapis.com/css?family=Noto+Sans+TC:400,500&display=swap&subset=chinese-traditional'
  );

  ::v-deep div.v-application--wrap {
    margin: 0;
    font-family: "Noto Sans TC", "Microsoft Yahei", "微軟雅黑", sans-serif;
  }

  @media (min-width: 992px) {
    .navbar.custom-nav{
      padding-top:16px;
      padding-bottom:16px;
      background-color: var(--navbar-header-color) !important;
    }
  }

  span.v-badge__badge {
    background: red !important;
  }

  ::v-deep .dropdown.b-dropdown.subMenu.btn-group {
    background: red !important;
  }

  ::v-deep svg.bi-briefcase.b-icon.bi {
    color: #ffffff !important;
  }

  ::v-deep li.nav-item.b-nav-dropdown.dropdown > a > span {
    font-size: 16px !important;
  }

</style>