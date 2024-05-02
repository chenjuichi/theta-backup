<template>
<v-app>
  <v-container fluid>
    <v-snackbar v-model="snackbar" :color="snackbar_color" :right='snackbar_right' :top='snackbar_top'>
      {{ snackbar_info }}
      <template v-slot:action="{ attrs }">
        <v-btn icon :color="snackbar_icon_color" @click="snackbar= false">
          <v-icon dark>mdi-close-circle</v-icon>
        </v-btn>
      </template>
    </v-snackbar>

    <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
      <v-card width="80vw" class="pa-md-4  mt-5 mx-lg-auto">
        <v-data-table
          :headers="headers"
          :items="desserts"
          class="elevation-1"
          :options.sync="pagination"
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
          :search="search"
          :custom-filter="filterOnlyCapsText"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>主軸跑合資料</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>

                          <!--
              <div v-for="(schedule1, index) in schedule" :key="index" class="records_container">
            -->
              <div class="records_container" v-show="time_isOK">
                <div>自動讀檔倒數(hh:mm):</div><span>{{formattedHours}} : {{formattedMinutes}}</span>
              </div>

              <v-text-field v-model="search" label="關鍵字查詢 (UPPER CASE ONLY)"
                class="mx-4"
                style="position:relative; top: 5px;"
              ></v-text-field>
              <v-spacer></v-spacer>

              <v-dialog v-model="dialog" max-width="1200px" :content-class="temp_css">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on" v-show="currentUser.perm<=2">
                    <v-icon left dark>mdi-table-plus</v-icon>
                    新增資料
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                  </v-card-title>

                  <v-card-text>
                    <v-container>
                      <!-- 第1列-->
                      <v-row class="my-custom-for-line1">
                        <v-col cols="12" md="4" v-show="formTitle === '新增資料'">
                          <file-uploader @file-selected="handleFileSelected"></file-uploader>
                        </v-col>
                        <v-col cols="12" md="1"></v-col>
                        <v-col cols="12" md="2">
                          <v-text-field
                            label="前軸承震動速度-1 大於"
                            outlined
                            v-model="spindleRunIn_editedItem.frontV2"
                            color="blue"
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="1"></v-col>
                        <v-col cols="12" md="2">
                          <v-text-field
                            label="後軸承震動速度-1 大於"
                            outlined
                            v-model="spindleRunIn_editedItem.backV2"
                            color="blue"
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="2"></v-col>
                      </v-row>
                      <!-- 第2列-->
                      <v-row v-show="formTitle === '新增資料'">
                        <v-btn
                          @click="readAllExcelFiles"
                          style="position: relative; left: 25px; top:-15px;"
                        >
                          <v-icon left color="green">mdi-file-excel</v-icon>
                          讀取檔案
                        </v-btn>
                      </v-row>
                      <!-- 第3列-->
                      <v-row class="my-custom-for-line3">
                        <v-col cols="12" md="2">    <!-- 2023-04-14 modify md=3 => md=2   -->
                          <v-text-field
                            v-model="spindleRunIn_editedItem.customer"
                            label="客戶代碼"
                            readonly
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="2"></v-col>
                        <v-col cols="12" md="2">
                          <v-text-field
                            v-model="spindleRunIn_editedItem.employer"
                            label="檢測人員工號"
                            readonly
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="2"></v-col>
                        <v-col class="d-flex" cols="12" md="2">
                          <v-text-field
                            v-model="spindleRunIn_editedItem.date"
                            label="檢測日期"
                            readonly
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="2"></v-col>
                      </v-row>
                      <!-- 第4列-->
                      <v-row class="my-custom-for-line4">
                        <v-col cols="12" md="2">
                          <v-text-field
                            v-model="spindleRunIn_editedItem.spindle_cat"
                            label="型號"
                            readonly
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="2"></v-col>
                        <v-col cols="12" md="2">
                          <v-text-field
                            label="編  號"
                            v-model="spindleRunIn_editedItem.run_in_id"
                            readonly
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="6"></v-col>
                      </v-row>
                      <!-- 第5列-->
                      <v-row mt-10 align="center" justify="center" class="my-custom-for-line5">
                        <v-progress-linear v-show="isLoading" indeterminate color="indigo darken-2" height="25">
                          <strong>{{globalVar}}</strong>
                        </v-progress-linear>
                        <template>
                          <v-data-table
                            dense
                            :headers="spindleRunIn_headers"
                            :items="spindleRunIn_desserts"
                            :item-class="setRowBackground"
                            item-key="id"
                            fixed
                            class="custom-table-style"
                            :footer-props="{
                              'itemsPerPageText': '每頁的資料筆數',
                            }"
                          >
                          </v-data-table>
                        </template>
                      </v-row>
                    </v-container>
                  </v-card-text>
                  <v-card-actions class="my-custom-margin-for-btn">
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">取消</v-btn>
                    <v-btn color="blue darken-1" text @click="save" :disabled='checkDataForSaveButton' v-show="formTitle === '新增資料'">確定</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>

              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5">確定刪除這筆資料?</v-card-title>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="closeDelete">取消</v-btn>
                    <v-btn color="blue darken-1" text @click="removeSpindleRunIn()">刪除</v-btn>
                    <v-spacer></v-spacer>
                  </v-card-actions>
                </v-card>
              </v-dialog>

              <v-dialog v-show="rightDialog"
                v-model="rightDialog"
                transition="dialog-bottom-transition"
                max-width="500"
              >
                <v-card>
                  <v-toolbar color="primary" dark>錯誤訊息!</v-toolbar>
                  <v-card-text>
                    <div class="text-h4 pa-12">使用這項功能, 請通知管理人員...</div>
                  </v-card-text>
                  <v-card-actions class="justify-end">
                    <v-spacer></v-spacer>
                    <v-btn text @click="rightCloseFun"> 取消 </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>

          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)" style="color: green;">
              mdi-file-excel-box
            </v-icon>
            <v-icon small  @click="deleteItem(item)" style="color: red;">
              mdi-delete
            </v-icon>
          </template>

          <template v-slot:no-data>
            <strong><font color='red'>目前沒有資料</font></strong>
          </template>
        </v-data-table>
      </v-card>
    </v-row>

    <v-row align="center" justify="space-around" v-else>
        <v-dialog
          v-model="permDialog"
          transition="dialog-bottom-transition"
          max-width="500"
        >
          <v-card>
            <v-toolbar color="primary" dark>錯誤訊息!</v-toolbar>
            <v-card-text>
              <div class="text-h4 pa-12">使用這項功能, 請通知管理人員...</div>
            </v-card-text>
            <v-card-actions class="justify-end">
              <v-spacer></v-spacer>
              <v-btn text @click="permCloseFun"> 取消 </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
    </v-row>
  </v-container>
</v-app>
</template>

<script>
import axios from 'axios';

import Common from '../../mixin/common.js'
import Notification from '../../mixin/notification.js'

import { _createCSSWithConstants } from '../../mixin/constant.js';
import { _thetaSpindleTypes } from '../../mixin/constant.js';

import FileUploader from '../../components/FileUpLoader.vue';

export default {
  name: 'SpindleRunIn',

  components: {
    FileUploader,
  },

  mixins: [Common, Notification],

  mounted() {
    // if back button is pressed
    window.onpopstate = () => {
      console.log("press back button, good bye...");

      const userData = JSON.parse(localStorage.getItem('loginedUser'));
      userData.setting_items_per_page = this.pagination.itemsPerPage;
      localStorage.setItem('loginedUser', JSON.stringify(userData));
    };

    // 設定每1分鐘執行一次 myWork 函式
    const timeValue = 1 * 60 * 1000;
    this.intervalId = setInterval(this.listFileOK, timeValue);

    // 設定每1秒鐘執行一次 myWork 函式
    const secValue = 1 * 1000;
    this.intervalIdForSec = setInterval(this.fetchGlobalVar, secValue);
  },

  data: () => ({
    currentUser: { },
    permDialog: false,
    rightDialog: false,
    dialog: false,
    dialogDelete: false,
    /*
    snackbar: false,
    snackbar_color: 'success',
    snackbar_right: true,
    snackbar_top: true,
    snackbar_info: '',
    snackbar_icon_color: '#adadad',
    */
    pagination: {
      //itemsPerPage: 10,   //預設值, rows/per page
      //page: 1,
    },

    tosterOK: false,
    toster_pos_x: 1000,
    toster_pos_y: 400,
    toster_delay:3,

    //資料表頭
    spindleRunIn_headers: [
      { text: '項次',  value: 'id', align: 'start',     sortable: false, width: '35px'},
      { text: '時間', value: 'spindleRunIn_period', align: 'start',  sortable: false, width: '40px' },
      { text: '段速', value: 'spindleRunIn_speed_level',                sortable: false, width: '40px' },
      { text: '轉速',         value: 'spindleRunIn_speed',        sortable: false, width: '50px' },
      { text: '定子溫度',      value: 'spindleRunIn_stator_temp', sortable: false, width: '75px' },
      { text: '內部前軸承溫度',   value: 'spindleRunIn_inner_frontBearing_temp',           sortable: false, width: '100px' },
      { text: '內部後軸承溫度',  value: 'spindleRunIn_inner_backBearing_temp',           sortable: false, width: '100px' },
      { text: '外部前軸承溫度',   value: 'spindleRunIn_outer_frontBearing_temp',          sortable: false,  width: '108px' },
      { text: '外部後軸承溫度',   value: 'spindleRunIn_outer_backBearing_temp',           sortable: false,  width: '108px' },
      { text: '室溫',            value: 'spindleRunIn_room_temp',                       sortable: false,  width: '50px' },
      { text: '冷卻機水溫',      value: 'spindleRunIn_coolWater_temp',           sortable: false, width: '100px' },
      { text: 'R相電流',         value: 'spindleRunIn_Rphase_current',             sortable: false, width: '78px' },
      { text: 'S相電流',         value: 'spindleRunIn_Sphase_current',             sortable: false, width: '78px' },
      { text: 'T相電流',         value: 'spindleRunIn_Tphase_current',             sortable: false, width: '78px' },
      { text: '冷卻機管路流量',   value: 'spindleRunIn_cool_pipeline_flow',       sortable: false, width: '100px' },
      { text: '冷卻機管路壓力',   value: 'spindleRunIn_cool_pipeline_pressure',      sortable: false, width: '100px' },
      { text: '前軸承震動速度-1', value: 'spindleRunIn_frontBearing_vibration_speed1', sortable: false,  width: '120px' },
      { text: '前軸承震動加速-1', value: 'spindleRunIn_frontBearing_vibration_acc1',   sortable: false,  width: '120px' },
      { text: '前軸承震動位移-1', value: 'spindleRunIn_frontBearing_vibration_disp1',   sortable: false,  width: '120px' },
      { text: '前軸承震動速度-2', value: 'spindleRunIn_frontBearing_vibration_speed2', sortable: false,  width: '120px' },
      { text: '前軸承震動加速-2', value: 'spindleRunIn_frontBearing_vibration_acc2',   sortable: false,  width: '120px' },
      { text: '前軸承震動位移-2', value: 'spindleRunIn_frontBearing_vibration_disp2',   sortable: false,  width: '120px' },
      { text: '後軸承震動速度-1', value: 'spindleRunIn_backBearing_vibration_speed1', sortable: false,  width: '120px' },
      { text: '後軸承震動加速-1', value: 'spindleRunIn_backBearing_vibration_acc1',   sortable: false,  width: '120px' },
      { text: '後軸承震動位移-1', value: 'spindleRunIn_backBearing_vibration_disp1',   sortable: false,  width: '120px' },
      { text: '後軸承震動速度-2', value: 'spindleRunIn_backBearing_vibration_speed2', sortable: false,  width: '120px' },
      { text: '後軸承震動加速-2', value: 'spindleRunIn_backBearing_vibration_acc2',   sortable: false,  width: '120px' },
      { text: '後軸承震動位移-2', value: 'spindleRunIn_backBearing_vibration_disp2',   sortable: false,  width: '120px' },
    ],
    spindleRunIn_desserts: [],
    temp_spindleRunIn_desserts: [],
    spindleRunIn_editedItem: {
      customer: '',
      spindle_cat: '',
      run_in_id: '',
      employer: '',
      date: '',
      frontV2: 0,
      backV2: 0,
      excel_file: '',
    },
    default_spindleRunIn_editedItem: {
      customer: '',
      spindle_cat: '',
      run_in_id: '',
      employer: '',
      date: '',
      frontV2: 0,
      backV2: 0,
      excel_file: '',
    },
    temp_spindleRunIn_editedItem: {},
    /*
    //資料表頭
    headers: [
      { text: '檔案名稱', sortable: false, value: 'spindleRunIn_excel_file', width: '17%' },
      { text: '客戶代碼', sortable: true, value: 'spindleRunIn_customer', width: '8%' },
      { text: '型號', sortable: true, value: 'spindleRunIn_spindle_cat', width: '18%' },
      { text: '編  號', sortable: true, value: 'spindleRunIn_id', width: '10%' },
      { text: '檢測人員工號', sortable: true, value: 'spindleRunIn_employer_emp_id', width: '15%' },
      { text: '檢測日期', sortable: false, value: 'spindleRunIn_date', width: '10%' },
      { text: 'Actions', sortable: false, value: 'actions', width: '7%' },
    ],
    */
    desserts: [],
    temp_desserts: [],

    editedIndex: -1,
    editedItem: {
      spindleRunIn_customer_id: '',

      spindleRunIn_cat_id: '',
      spindleRunIn_id: '',
      spindleRunIn_uidid: '',

      spindleRunIn_employee_id: '',
      spindleRunIn_date: '',

      spindleRunIn_period: '',
      spindleRunIn_speed_level: '',
      spindleRunIn_speed: '',
      spindleRunIn_stator_temp: '',
      spindleRunIn_inner_frontBearing_temp: '',
      spindleRunIn_inner_backBearing_temp: '',
      spindleRunIn_outer_frontBearing_temp: '',
      spindleRunIn_outer_backBearing_temp: '',
      spindleRunIn_room_temp: '',
      spindleRunIn_coolWater_temp: '',
      spindleRunIn_Rphase_current: '',
      spindleRunIn_Sphase_current: '',
      spindleRunIn_Tphase_current: '',
      spindleRunIn_cool_pipeline_flow: '',
      spindleRunIn_cool_pipeline_pressure: '',
      spindleRunIn_frontBearing_vibration_speed1: '',
      spindleRunIn_frontBearing_vibration_acc1: '',
      spindleRunIn_frontBearing_vibration_disp1: '',
      spindleRunIn_frontBearing_vibration_speed2: '',
      spindleRunIn_frontBearing_vibration_acc2: '',
      spindleRunIn_frontBearing_vibration_disp2: '',
      spindleRunIn_backBearing_vibration_speed1: '',
      spindleRunIn_backBearing_vibration_acc1: '',
      spindleRunIn_backBearing_vibration_disp1: '',
      spindleRunIn_backBearing_vibration_speed2: '',
      spindleRunIn_backBearing_vibration_acc2: '',
      spindleRunIn_backBearing_vibration_disp2: '',
    },

    defaultItem: {
      spindleRunIn_customer_id: '',

      spindleRunIn_cat_id: '',
      spindleRunIn_id: '',
      spindleRunIn_uidid: '',

      spindleRunIn_employee_id: '',
      spindleRunIn_date: '',

      spindleRunIn_period: '',
      spindleRunIn_speed_level: '',
      spindleRunIn_speed: '',
      spindleRunIn_stator_temp: '',
      spindleRunIn_inner_frontBearing_temp: '',
      spindleRunIn_inner_backBearing_temp: '',
      spindleRunIn_outer_frontBearing_temp: '',
      spindleRunIn_outer_backBearing_temp: '',
      spindleRunIn_room_temp: '',
      spindleRunIn_coolWater_temp: '',
      spindleRunIn_Rphase_current: '',
      spindleRunIn_Sphase_current: '',
      spindleRunIn_Tphase_current: '',
      spindleRunIn_cool_pipeline_flow: '',
      spindleRunIn_cool_pipeline_pressure: '',
      spindleRunIn_frontBearing_vibration_speed1: '',
      spindleRunIn_frontBearing_vibration_acc1: '',
      spindleRunIn_frontBearing_vibration_disp1: '',
      spindleRunIn_frontBearing_vibration_speed2: '',
      spindleRunIn_frontBearing_vibration_acc2: '',
      spindleRunIn_frontBearing_vibration_disp2: '',
      spindleRunIn_backBearing_vibration_speed1: '',
      spindleRunIn_backBearing_vibration_acc1: '',
      spindleRunIn_backBearing_vibration_disp1: '',
      spindleRunIn_backBearing_vibration_speed2: '',
      spindleRunIn_backBearing_vibration_acc2: '',
      spindleRunIn_backBearing_vibration_disp2: '',
    },

    newItemIn: '',
    newItemOut: '',
    newItem: '',

    load_SingleTable_ok: false,
    load_4thTable_ok: false,
    load_5thTable_ok: false,
    //readAllExcelFiles_isOK: false,

    isLoading: false,

    intervalId: null,
    intervalIdForSec: null,
    temp_file_ok: false,
    search: '',

    schedule: [],

    formattedHours: '00',
    formattedMinutes: '00',
    time_isOK: false,
    globalVar: '',
  }),

  computed: {
    headers () {
      return [
        { text: '檔案名稱', sortable: false, value: 'spindleRunIn_excel_file', width: '17%' },
        { text: '客戶代碼', sortable: true, value: 'spindleRunIn_customer', width: '8%' },
        { text: '型號', sortable: true, value: 'spindleRunIn_spindle_cat', width: '18%' },
        { text: '編  號', sortable: true, value: 'spindleRunIn_id', width: '10%' },
        { text: '檢測人員工號', sortable: true, value: 'spindleRunIn_employer_emp_id', width: '15%' },
        { text: '檢測日期', sortable: false, value: 'spindleRunIn_date', width: '10%' },
        { text: 'Actions', sortable: false, value: 'actions', width: '7%' },
      ]
    },

    formTitle () {
      return this.editedIndex === -1 ? '新增資料' : '資料顯示'
    },

    checkDataForSaveButton() {
      if (!!this.spindleRunIn_editedItem.customer) {
        return false;
      } else {
        return true;
      }
    },
  },

  watch: {
    dialog (val) {
      val || this.close();
    },

    dialogDelete (val) {
      val || this.closeDelete()
    },

    'spindleRunIn_editedItem.frontV2': function(newVal, oldVal) {
      console.log('aa:', newVal, oldVal);

      this.spindleRunIn_desserts.forEach(item => {
        item.bgColor = (item.spindleRunIn_frontBearing_vibration_disp2 >= newVal) ? 'red-background' : '';
      });
    },

    'spindleRunIn_editedItem.backV2': function(newVal, oldVal) {
      console.log('bb:', newVal, oldVal);

      this.spindleRunIn_desserts.forEach(item => {
        item.bgColor = (item.spindleRunIn_backBearing_vibration_disp2  >= newVal) ? 'red-background' : '';
      });
    },

    load_5thTable_ok(val) {   //從excel檔案, 存取runin資料
      if (val) {
        this.spindleRunIn_desserts = Object.assign([], this.temp_spindleRunIn_desserts);
        this.spindleRunIn_editedItem = Object.assign({}, this.temp_spindleRunIn_editedItem);

        this.isLoading = false;
        this.load_5thTable_ok = false;
      }
    },

    load_4thTable_ok(val) { //從mySQL, 存取runindata資料
      if (val) {
        this.spindleRunIn_desserts = Object.assign([], this.temp_spindleRunIn_desserts);

        this.isLoading = false;
        this.dialog = true;

        this.load_4thTable_ok = false;
      }
    },

    load_SingleTable_ok(val) {  ////從mySQL, 存取spindlerunin內容資料
      if (val) {
        this.desserts = Object.assign([], this.temp_desserts);

        this.listDotEnv();

        this.load_SingleTable_ok = false;
      }
    },
    /*
    readAllExcelFiles_isOK(val) {
      if (val) {
        this.showTosterForOK(res.data.message)
        this.close();
        this.$router.go(0);
        this.readAllExcelFiles_isOK=false;
      }
    },
    */
  },

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    console.log("this.currentUser", this.currentUser)
    if (this.currentUser.perm < 1) {
      this.permDialog=true;
    }

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.initAxios();
    this.initialize()
  },

  methods: {
    initialize() {
      //this.load_SingleTable_ok=false;
      this.listSpindleRunIns();
    },

    listSpindleRunIns() {
      console.log("listSpindleRunIns()...");

      this.load_SingleTable_ok = false;
      const path = '/listSpindleRunIns';
      axios.get(path)
      .then((res) => {
        this.temp_desserts = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_SingleTable_ok = true;
      })
      .catch((error) => {
        console.error(error);
        this.showTosterForError('錯誤! API連線問題...')
      });
    },

    formatTime() {
      console.log("formatTime(), ", this.schedule[0][0], this.schedule[0][1])

      const targetTime = new Date(); // 取得現在的時間
      targetTime.setHours(this.schedule[0][0]); // 設置目標時間的小時
      targetTime.setMinutes(this.schedule[0][1]); // 設置目標時間的分鐘
      targetTime.setSeconds(0); // 將秒數設置為 0，以確保精確度

      let now = new Date();
      let remainingTime = targetTime - now; // 計算剩餘時間（毫秒）

      if (remainingTime <= 0) {
        //clearInterval(this.intervalId); // 如果時間到了，停止計時器
        remainingTime = 0; // 將剩餘時間設置為 0
        this.time_isOK = false;
      } else {
        this.time_isOK = true;

        const hours = Math.floor(remainingTime / (1000 * 60 * 60));
        const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
        //console.log("date format 1: ", hours , minutes)

        // 格式化時和分數字，例如 1:3 -> 01:03
        this.formattedHours = String(hours).padStart(2, '0');
        this.formattedMinutes = String(minutes).padStart(2, '0');
        //console.log("date format 2: ", this.formattedHours , ':', this.formattedMinutes)
      }

    },

    listFileOK() {
      console.log("listFileOK()...")

      this.formatTime();

      const path = '/listFileOK';
      axios.get(path)
      .then((res) => {
        let now = new Date();
        let hour = now.getHours();
        let minute = now.getMinutes();
        this.temp_file_ok = res.data.outputs;
        console.log(hour + ":" + minute);
        console.log("GET ok, file_ok flag value is: ", res.data.outputs);

        if (this.temp_file_ok) {
          clearInterval(this.intervalId); // 如果時間到了，停止計時器
          this.formattedHours= '00';
          this.formattedMinutes= '00';
          this.$router.go(0);
          console.log("file_ok flag value is: ", res.data.outputs, "end timer");
        }
      })
      .catch((error) => {
        console.error(error);
        this.showTosterForError('錯誤! API連線問題...')
      });
    },

    listDotEnv() {
      console.log("listDotEnv()...")

      const path = '/listDotEnv';
      axios.get(path)
      .then((res) => {
        //let numArr1 = res.data.schedule_1.map(Number);
        let numArr1 = res.data.schedule_1.length ? res.data.schedule_1.map(Number) : [];
        let numArr2 = res.data.schedule_2.length ? res.data.schedule_2.map(Number) : [];
        //this.schedule= numArr1.concat(numArr2);
        this.schedule= [];
        this.schedule.push(numArr1);
        //console.log("hh:mm ", numArr1[0] + ":" + numArr1[1]);
        this.formatTime();
        //this.schedule.push(numArr2);
      })
      .catch((error) => {
        console.error(error);
        this.showTosterForError('錯誤! API連線問題...');
      });
    },

    readAllExcelFiles() {
      console.log("readAllExcelFiles, Axios get data...");
      //this.readAllExcelFiles_isOK=false;
      this.isLoading = true;
      const path = '/readAllExcelFiles';
      axios.get(path)
      .then((res) => {
        this.isLoading = false;
        if (res.data.status) {
          //this.readAllExcelFiles_isOK=true;
          //this.showTosterForOK(res.data.message);
          this.close();
          //this.$router.go(0);
          this.$router.push('/runIn');
          //this.readAllExcelFiles_isOK=false;
        } else {
          this.showTosterForError(res.data.message);
        }
      })
      .catch((error) => {
        this.isLoading = false;
        console.error(error);
        this.showTosterForError('錯誤! API連線問題...');
      });
    },

    fetchGlobalVar() {
      if (this.isLoading) {
        console.log("fetchGlobalVar()...");

        const path = '/fetchGlobalVar';
        axios.get(path)
        .then((res) => {
          this.globalVar = res.data.value;
        })
        .catch((error) => {
          console.error(error);
          this.showTosterForError('錯誤! API連線問題...');
        });
      }
    },

    handleFileSelected(fileName) {
      console.log('Selected file:', fileName); //接收到的檔案名稱
      this.isLoading = true;
      this.excel_file=fileName;

      this.listRunInFromCSV(fileName);
    },

    setRowBackground(item) {
      const rowClass1='red-background';
      const rowClass2='';
      let rowClass = (item.spindleRunIn_frontBearing_vibration_speed1 >= this.spindleRunIn_editedItem.frontV2 || item.spindleRunIn_backBearing_vibration_speed1  >= this.spindleRunIn_editedItem.backV2) ? rowClass1 : rowClass2;
      return rowClass;
    },

    listRunInData(myID) {
      console.log('listRunInData(), ', myID);

      this.load_4thTable_ok = false;
      let path='/listRunInData';
      let payload= {
        id: parseInt(myID),
      };
      axios.post(path, payload)
      .then(res => {
        console.log("listRunInDatas(), get data status: ", res.data.status);
        if (res.data.status) {
          this.temp_spindleRunIn_desserts = Object.assign([], res.data.outputs);

          this.load_4thTable_ok = true;
        } else {
          this.showTosterForError('錯誤! excel檔案問題...')
        }
      })
      .catch(err => {
        console.error(err)
        this.showTosterForError('錯誤! API連線問題...')
      });
    },

    editItem(item) {
      console.log("editItem (), ", item)

      if (this.currentUser.perm >2) {
        this.rightDialog = true;
        return;
      }

      this.isLoading = true;

      this.editedIndex = this.desserts.indexOf(item)

      let tmp_item ={
        customer : item.spindleRunIn_customer,
        spindle_cat : item.spindleRunIn_spindle_cat,
        run_in_id : item.spindleRunIn_id,
        employer : item.spindleRunIn_employer_emp_id,
        date : item.spindleRunIn_date,
        frontV2 : 100,
        backV2 : 100,
      };
      this.spindleRunIn_editedItem= Object.assign({}, tmp_item)
      this.listRunInData(item.id);
    },

    deleteItem (item) {
      console.log("deleteItem: ", item);

      if (this.currentUser.perm >2) {
        this.rightDialog = true;
        return;
      }

      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    removeSpindleRunIn() {
      //console.log("1. removeSpindleRunIn: ", item);
      console.log("removeSpindleRunIn: ", this.editedItem);

      const path='/removeSpindleRunIn';
      //let payload = Object.assign({}, this.editedItem);
      let payload= {
        id: this.editedItem.id,
      };
      axios.post(path, payload)
      .then(res => {
        console.log("remove spindleRunin status: ", res.data.status);
        if (res.data.status) {
          this.editedItem = Object.assign({}, this.defaultItem); //清空 editedItem

          this.desserts.splice(this.editedIndex, 1);

          this.closeDelete();
        } else {
          this.showTosterForError('錯誤! 刪除紀錄沒有完成...')
        }
      })
      .catch(err => {
        console.error(err)
        this.showTosterForError('錯誤! API連線問題...')
      });

    },

    close() {
      this.dialog = false;
      this.isLoading=false;
      this.$nextTick(() => {
        this.spindleRunIn_editedItem = Object.assign({}, this.default_spindleRunIn_editedItem);
        this.spindleRunIn_desserts = [];
        this.editedIndex = -1
      })
    },

    closeDelete () {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },
    /*
    showTosterForError(msg) {
      this.snackbar_color='red accent-2';
      this.snackbar=true;
      this.snackbar_info= msg;
      this.snackbar_icon_color= '#adadad';
    },
    */
    listRunInFromCSV(file_name) {
      console.log('listRunInFromCSV(), ', file_name);

      this.load_5thTable_ok = false;
      let path='/listRunInFromCSV';
      let payload= {
        file_name: file_name,
      };
      axios.post(path, payload)
      .then(res => {
        console.log("listRunInFromCSV(), get data status: ", res.data.status);
        if (res.data.status) {
          /*
          console.log( 'file ', res.data.file,)
          console.log( 'customer ', res.data.customer,)
          console.log( 'spindle_cat ', res.data.spindle_cat,)
          console.log( 'run_in_id ', res.data.run_in_id,)
          console.log( 'employer ', res.data.employer,)
          console.log( 'date ', res.data.date,)
          console.log( 'outputs: ')
          console.log( res.data.outputs,)
          */
          this.temp_spindleRunIn_desserts = Object.assign([], res.data.outputs);
          this.temp_spindleRunIn_editedItem = Object.assign({}, res.data.title_obj);
          let temp_len = this.temp_spindleRunIn_editedItem.employer.length;
          //tmp_item.grid_type = (t1 == '銑削/研磨主軸(自動換刀)') ? "1" : (t1 == '研磨主軸(手動換刀)') ? "2" : (t1 == '修砂主軸(手動換刀)') ? "3" : "0";

          //this.temp_spindleRunIn_editedItem.customer=
          //this.temp_spindleRunIn_editedItem.spindle_cat=
          //this.temp_spindleRunIn_editedItem.run_in_id=
          this.temp_spindleRunIn_editedItem.employer = this.temp_spindleRunIn_editedItem.employer.padStart(4,"0");
          //this.temp_spindleRunIn_editedItem.employer = (temp_len == 2) ? '00'+this.temp_spindleRunIn_editedItem.employer : (temp_len == 3) ? '0'+this.temp_spindleRunIn_editedItem.employer : (temp_len == 1) ? '000'+this.temp_spindleRunIn_editedItem.employer : this.temp_spindleRunIn_editedItem.employer
          //this.temp_spindleRunIn_editedItem.date=
          this.temp_spindleRunIn_editedItem.frontV2=100;
          this.temp_spindleRunIn_editedItem.backV2=100;
          this.temp_spindleRunIn_editedItem.excel_file = this.excel_file;

          this.load_5thTable_ok = true;
        } else {
          this.isLoading = false;
          this.showTosterForError(res.data.message)
        }
      })
      .catch(err => {
        console.error(err)
        this.showTosterForError('錯誤! API連線問題...')
      });
    },

    save() {
      console.log("click save button, editedIndex: ", this.editedIndex);

      let obj = {
        spindleRunIn_customer: this.spindleRunIn_editedItem.customer,
        spindleRunIn_date: this.spindleRunIn_editedItem.date,
        spindleRunIn_employer_emp_id: this.spindleRunIn_editedItem.employer,
        spindleRunIn_excel_file: this.spindleRunIn_editedItem.excel_file,
        spindleRunIn_id: this.spindleRunIn_editedItem.run_in_id,
        spindleRunIn_spindle_cat: this.spindleRunIn_editedItem.spindle_cat,
      }

      let payload = Object.assign({}, obj);
      payload.block=Object.assign([], this.spindleRunIn_desserts);
      const path='/createSpindleRunins';
      axios.post(path, payload)
      .then(res => {
        console.log("save spindleRunin data status: ", res.data.status)
        if (res.data.status) {
          this.desserts.push(obj);
          this.close();
          this.spindleRunIn_editedItem = Object.assign({}, this.default_spindleRunIn_editedItem) //清空 editedItem
        } else {
          this.showTosterForError(res.data.message)
        }
      })
      .catch(err => {
        console.error(err);
        this.showTosterForError('錯誤! API連線問題...')
      });
    },

    permCloseFun() {
      console.log("permCloseFun()...");

      this.permDialog = false
      this.$router.push('/navbar');
    },

    rightCloseFun() {
      console.log("rightCloseFun()...");

      this.rightDialog = false
      //this.$router.push('/navbar');
    },

    filterOnlyCapsText (value, search, item) {
      return value != null &&
        search != null &&
        typeof value === 'string' &&
        value.toString().toLocaleUpperCase().indexOf(search) !== -1
    },
  },

  beforeDestroy() {
    // 離開Vue之前, 清除interval
    clearInterval(this.intervalId);
    clearInterval(this.intervalIdForSec);
    // 離開Vue之前, 清除 window.onpopstate 的處理程序
    window.onpopstate = null;
  },
}
</script>

<style lang="scss" scoped>
@import url(
  'https://fonts.googleapis.com/css?family=Noto+Sans+TC:400,500&display=swap&subset=chinese-traditional'
);

div.v-toolbar__title {
  margin: 0;
  font-family: "Noto Sans TC", "Microsoft Yahei", "微軟雅黑", sans-serif;
}

::v-deep .v-data-table-header {
  background-color:var(--navbar-header-color);
}

::v-deep .v-data-table-header th {
  font-size: 0.8em !important;
}

::v-deep .v-data-table td {
  font-size: 12px !important;
}

::v-deep .v-data-table-header th:nth-last-child(1) {
  font-size: 0.8em !important;
}

::v-deep .v-data-table-header th:nth-last-child(1) span {
  color: #1f4788 !important;
}
::v-deep .v-data-table-header th:nth-last-child(3) span {
  color: #1f4788 !important;
}
::v-deep .v-data-table-header th:nth-last-child(4) span {
  color: #1f4788 !important;
}
::v-deep .v-data-table-header th:nth-last-child(5) span {
  color: #1f4788 !important;
}
::v-deep .v-data-table-header th:nth-last-child(6) span {
  color: #1f4788 !important;
}

::v-deep .style-for-data-table td {
  padding-left: 8px !important;
  padding-right: 0px !important;
}

::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  padding-left: 8px !important;
  padding-right: 0px !important;
  text-align: start !important;
}

::v-deep .v-label {
  font-size: 0.8em
}

::v-deep .v-label--active {
  font-size: 1em;
  font-weight: bold;
}

//::v-deep .v-data-table-header th:nth-last-child(1) span {
//  color: #1f4788 !important;
//}
.my-custom-for-line1 {
  position: relative;
  top: -20px;
}
/*
.my-custom-for-line3 {
  margin-bottom: 0px;
  position: relative;
  top: -25px;
}

.my-custom-for-line4 {
  margin-top: 0px;
  position: relative;
  top: -70px;
}

.my-custom-for-line5 {
  position: relative;
  top: -80px;
}

.my-custom-margin-for-btn {
  position: relative;
  top: -110px;
}
*/
.custom-table-style {
  overflow-x: auto;
  max-width: 100%;
}

::v-deep .red-background {
  background-color: #ff8080;
  //color: white;
}

::v-deep .v-text-field--outlined fieldset {
  border-color: blue !important;
  //border-color: blue;
}

::v-deep .v-data-table.custom-table-style .v-data-table-header th:nth-last-child(6) span {
  color: #1f4788 !important;
  animation: blink 1s infinite;
}

::v-deep .v-data-table.custom-table-style .v-data-table-header th:nth-last-child(12) span {
  color: #1f4788 !important;
  animation: blink 1s infinite;
}

/* 定義動畫 */
@keyframes blink {
  0% { opacity: 1; }
  50% { opacity: 0; }
  100% { opacity: 1; }
}

::v-deep .records_container {
    display: flex; /* 使用 flexbox */
    align-items: center; /* 垂直置中 */
    gap: 5px; /* 設定元素之間的間距 */
    position: relative;
    left: -110px;
    top: 20px;
    font-size: 12px;
    font-weight: bold;
}
</style>