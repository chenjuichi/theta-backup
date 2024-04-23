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

    <v-row align="center" justify="center" v-if="currentUser.perm == 1">
    <!--<v-row align="center" justify="center" v-if="currentUser.perm >= 1">-->
      <v-card width="100vw" class="pa-md-4 mt-5 mx-lg-auto">
        <v-data-table
          dense
          :headers="headers"
          :items="dessertsDisplay"
          :options.sync="pagination"
          :item-class="setRowBackground"
          class="elevation-1"
          :search="search"
          item-key="spindleIn_workID"
          :custom-filter="filterOnlyCapsText"
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <div class="v-data-table-top-height">
              <v-toolbar flat>
                <v-toolbar-title style="height:40px;">在庫記錄查詢</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-spacer></v-spacer>
                <!--關鍵字查詢-->
              <v-text-field
                v-model="search"
                placeholder="關鍵字查詢(Caps)"
                @input="(val) => (search = search.toUpperCase())"
                style="position:relative; left:-100px;"
                class="style-0"
              >
              </v-text-field>
                <!-- 入庫日期查詢 -->
                <v-menu
                  v-model="fromDateMenu"
                  :close-on-content-click="false"
                  :nudge-right="40"

                  transition="scale-transition"
                  offset-y

                  max-width="280px"
                  min-width="280px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      placeholder="入庫開始日期查詢"
                      prepend-icon="event"
                      readonly
                      :value="fromDateDisp"
                      v-model="compareDate"
                      v-on="on"
                      class="shrink style-3"
                      style="position:relative; left:-300px;"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    locale="zh-TW"
                    :min="minDate"
                    :max="maxDate"
                    v-model="fromDateVal"
                    no-title
                    @input="fromDateMenu = false"
                  ></v-date-picker>
                </v-menu>

                <v-menu
                  v-model="fromDateMenuEnd"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  max-width="280px"
                  min-width="280px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      placeholder="入庫截止日期查詢"
                      prepend-icon="event"
                      readonly
                      :value="fromDateDispEnd"
                      v-model="compareDateEnd"
                      v-on="on"
                      class="shrink style-3"
                      style="position:relative; left:-250px;"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    locale="zh-TW"
                    :min="minDate"
                    :max="maxDate"
                    v-model="fromDateValEnd"
                    no-title
                    @input="fromDateMenuEnd = false"
                  ></v-date-picker>
                </v-menu>
              <!-- 效期查詢 -->
            <!--
              <v-menu
                v-model="fromDateMenuPeriod"
                :close-on-content-click="false"
                :nudge-right="40"

                transition="scale-transition"
                offset-y

                max-width="280px"
                min-width="280px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    placeholder="效期查詢"
                    prepend-icon="event"
                    readonly
                    :value="displayPeriodDate"
                    v-model="compareDatePeriod"
                    v-on="on"
                    class="shrink style-2"

                  ></v-text-field>
                </template>
                <v-date-picker
                  locale="zh-TW"
                  :min="minDate"
                  :max="maxDate"
                  v-model="fromDateValP"
                  no-title
                  @input="fromDateMenuPeriod = false"
                ></v-date-picker>
              </v-menu>
            -->
              <!-- 按鍵指令 -->
              <v-btn color="primary" class="mt-n1 mr-15 mx-auto excel_wrapper" style="position:relative; left:-70px; top:-5px !important;" @click="exportToExcel" v-show="currentUser.perm<=2">
                <v-icon left>mdi-microsoft-excel</v-icon>
                Excel
              </v-btn>
              <div class="flip_wrapper" style="position:relative; left:-70px; top:10px;" v-show="currentUser.perm<=2">
                <div class="flip_btn">
                  <v-btn color="primary" class="side default-side mt-n1 mr-15 mx-auto">
                    <v-icon left>mdi-content-save-edit-outline</v-icon>
                    資料更新
                  </v-btn>
                  <v-btn color="primary" class="side hover-side mt-n1 mr-15 mx-auto" @click="updateStockInDataByInv">
                    <v-icon left size="24px">mdi-check-circle-outline</v-icon>
                    確定?
                  </v-btn>
                </div>
              </div>
              </v-toolbar>
            </div>

            <div class="records_container">
              <div class="square1"></div>
              <span style="position:relative; left: -15px;">:效期異常</span>
              <div class="square2"></div>
              <span style="position:relative; left: -15px;">:出庫異常</span>
            </div> <!-- 包含兩個四方形和文字的容器 -->

            <v-progress-linear v-show="isLoading" indeterminate color="red"/>
          </template>

          <template v-slot:item.stkRecord_sum="props" v-show="compareSafeStock">
            <v-edit-dialog
              :return-value.sync="props.item.stkRecord_sum"

              persistent
              @save="save"
              @cancel="cancel"
              @open="open"
              @close="close"
            >
              {{ props.item.stkRecord_sum }}  {{ props.item.stkRecord_unit }}
              <template v-slot:input>
                <v-text-field
                  v-model="props.item.stkRecord_sum"
                  label="Edit"
                  readonly
                  single-line
                ></v-text-field>
              </template>
            </v-edit-dialog>
          </template>

          <!-- text field 3 -->
          <template v-slot:item.comment="props">
            <div v-if="props.item.comment !== '其他'">
              <v-select
                v-model="props.item.comment"
                :items="comment_items"
                class="pe-0 me-2 py-1 my-0 myText"
                @change="getmSelect(props.item)">

                required
              ></v-select>
            </div>
            <div v-else>
              <v-text-field
                autofocus
                style="position:relative; top:-10px;"
                v-model="commentForInventory"
                v-on:keyup.enter="getmComment(props.item)">
              </v-text-field>
            </div>
          </template>

          <template v-slot:no-data>
            <!--<strong><font color='red'>目前沒有資料</font></strong> 2023-07-21 mark-->
            <strong><font color='blue'>資料下載中...</font></strong>   <!--2023-07-21 add-->
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

import '../../mixin/dateformate.js'

import { _createCSSWithConstants } from '../../mixin/constant.js';
import { _thetaSpindleTypes } from '../../mixin/constant.js';

export default {
  name: 'SpindleStockRecord',

  mixins: [Common, Notification],

  mounted() {
    // if back button is pressed
    window.onpopstate = () => {
      console.log("press back button, good bye...");

      const userData = JSON.parse(localStorage.getItem('loginedUser'));
      userData.setting_items_per_page = this.pagination.itemsPerPage;
      localStorage.setItem('loginedUser', JSON.stringify(userData));
    };
  },

  data () {
    return {
      currentUser: {},
      permDialog: false,
      /*
      snackbar: false,
      snackbar_color: 'success',
      snackbar_right: true,
      snackbar_top: true,
      snackbar_info: '',
      snackbar_icon_color: '#adadad',
      */
      //theta ===
      fromDateMenu: false,
      fromDateVal: null,
      compareDate: '',          //查詢開始日期

      fromDateMenuEnd: false,
      fromDateValEnd: null,
      compareDateEnd: '',       //查詢截止日期
      //theta ===

      //fromDateMenuStart: false,
      //fromDateValStart: null,
      //compareDateStart: '',  //查詢開始日期

      //fromDateMenuEnd: false,
      //fromDateValEnd: null,
      //compareDateEnd: '',    //查詢截止日期

      fromDateMenuPeriod: false,
      fromDateValP: null,
      compareDatePeriod: '',      //查詢效期

      comparePeriods: '',
      compareSafeStock: false,

      //compareStart: false,

      minDate: "2012-07-01",
      maxDate: "2042-06-30",

      search: '',

      periodMessage: '效期天數',

      pagination: {
        //itemsPerPage: 10,   //預設值, rows/per page
        //page: 1,
      },

      itemsForSelect:[],
      selectedItems: [],
      isAllSelected: false,

      singleExpand: false,
      expanded: [],

      dessertsDisplayForCheckbox: [],
      dessertsDisplayForSelect: [],
      dessertsDisplay: [],

      headers :[
        //{ text: 'ID', sortable: false, value: 'id', align: 'start', width: '4%' },  //2023-06-26 modify
        { text: '製令單號', sortable: true, value: 'spindleIn_workID', width: '8%', },
        { text: '類別 / 型號', sortable: true, value: 'spindleStockIn_type_cat', width: '20%',},
        { text: '入庫日期', sortable: false, value: 'spindleStockIn_date', width: '8%',},
        { text: '入庫人員', sortable: true, value: 'spindleStockIn_employer', width: '7%',},
        { text: '效期', sortable: false, value: 'spindleStockIn_period', width: '8%',},
        { text: '出庫日期', sortable: false, value: 'spindleStockOut_date', width: '8%',},
        { text: '出庫人員', sortable: true, value: 'spindleStockOut_employer', width: '7%',},
        { text: '儲位', sortable: true, value: 'spindleStockIn_st_lay', width: '15%', },                    //
        { text: '說明(輸入完後按enter)', sortable: false, value: 'comment', width: '15%' },
      ],

      isLoading: false,

      desserts: [ ],
      temp_desserts: [],

      comment_items: ['人員忘記出入庫', '主軸跑合異常', '在庫過期', '主軸允收異常', '其他'],
      commentForInventory: '',
      //commentForStockRecord: '',
      today: 0,

      load_SingleTable_ok: false,
    }
  },

  computed: {
    /*
    displayPeriodDate() {
      if (this.fromDateValP != null) {
        let yy_value=this.fromDateValP.substring(0, 4);
        let mmdd_value=this.fromDateValP.substring(5, this.fromDateValP.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.compareDatePeriod = yy_value + '/' + mmdd_value;
      }
      return this.fromDateValP;
    },

    fromDateDispStart() {
      if (this.fromDateValStart != null) {
        let yy_value=this.fromDateValStart.substring(0, 4);
        let mmdd_value=this.fromDateValStart.substring(5, this.fromDateValStart.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.compareDateStart = yy_value + '/' + mmdd_value;
      }
      return this.fromDateValStart;
    },

    fromDateDispEnd() {
      if (this.fromDateValEnd != null) {
        let yy_value=this.fromDateValEnd.substring(0, 4);
        let mmdd_value=this.fromDateValEnd.substring(5, this.fromDateValEnd.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.compareDateEnd = yy_value + '/' + mmdd_value;
      }
      return this.fromDateValEnd;
    },
    */
    //theta ===
    displayPeriodDate() {
      if (this.fromDateValP != null) {
        let yy_value=this.fromDateValP.substring(0, 4);
        let mmdd_value=this.fromDateValP.substring(5, this.fromDateValP.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.compareDatePeriod = yy_value + '/' + mmdd_value;
      }
      return this.fromDateValP;
    },

    fromDateDisp() {
      if (this.fromDateVal != null) {
        let yy_value=this.fromDateVal.substring(0, 4);
        let mmdd_value=this.fromDateVal.substring(5, this.fromDateVal.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.compareDate = yy_value + '/' + mmdd_value;
      }
      return this.fromDateVal;
    },

    fromDateDispEnd() {
      if (this.fromDateValEnd != null) {
        let yy_value=this.fromDateValEnd.substring(0, 4);
        let mmdd_value=this.fromDateValEnd.substring(5, this.fromDateValEnd.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.compareDateEnd = yy_value + '/' + mmdd_value;
      }
      return this.fromDateValEnd;
    },
    //theta ===
  },

  watch: {
    /*
    compareSafeStock(val) {
      if (val) {
        let safeStockEl=[];
        this.dessertsDisplayForCheckbox =  JSON.parse(JSON.stringify(this.dessertsDisplay))
        for (let i = 0; i < this.dessertsDisplay.length; i++) {
          let cStart=parseInt(this.dessertsDisplay[i].stkRecord_saftStock);     //安全庫存數量

          let cEnd=this.dessertsDisplay[i].stkRecord_sum;             //目前在庫總數量
          console.log("start, end", cStart, cEnd)
          if (cEnd < cStart)
            safeStockEl.push(this.dessertsDisplay[i]);
        }
        this.dessertsDisplay =  Object.assign([], safeStockEl);

        this.dessertsDisplayForSelect =  Object.assign([],this.dessertsDisplay);

        let removedEl=['全部'];
        for (let i = 0; i < this.dessertsDisplay.length; i++) {
          removedEl.push(this.dessertsDisplay[i].stkRecord_supplier)
        }
        this.itemsForSelect = [...new Set(removedEl)];
        this.selectedItems = Object.assign([], this.itemsForSelect);
        this.isAllSelected=true;

        this.getSumForDisplay();
      } else {
        this.dessertsDisplay =  Object.assign([], this.dessertsDisplayForCheckbox);
        this.dessertsDisplayForCheckbox=[];
      }
    },

    compareDatePeriod(val) {
      if (val!='') {
        let tem_len=this.desserts.length;
        for (let i=0; i < tem_len; i++) {
          //this.desserts = this.desserts.filter(function( obj ) {
          this.dessertsDisplay = this.dessertsDisplay.filter(function( obj ) {
            let myVar2 = obj.stkRecord_period.split('/');
            let c2 = myVar2.map(str => {
              return Number(str);
            });

            let myVar1 = val.split('/');
            let c1 = myVar1.map(str => {
              return Number(str);
            });

            console.log("效期, date: ", c1, c2)
            if (c1[0] > c2[0])
                return obj;
            if (c1[0] == c2[0] && c1[1] > c2[1])
                return obj;
            if (c1[0] == c2[0] && c1[1] == c2[1] && c1[2] >= c2[2])
                return obj;
          });
        }
        this.dessertsDisplayForSelect =  Object.assign([],this.dessertsDisplay);

        let removedEl=['全部'];
        for (let i = 0; i < this.dessertsDisplay.length; i++) {
          removedEl.push(this.dessertsDisplay[i].stkRecord_supplier)
        }
        this.itemsForSelect = [...new Set(removedEl)];
        this.selectedItems = Object.assign([], this.itemsForSelect);
        this.isAllSelected=true;

        this.getSumForDisplay();
      }
    },

    compareDateStart(val) {
      if (val!='') {
        let tem_len=this.desserts.length;
        for (let i=0; i < tem_len; i++) {
          //this.desserts = this.desserts.filter(function( obj ) {
          this.dessertsDisplay = this.dessertsDisplay.filter(function( obj ) {
            let myVar1 = obj.stkRecord_Date.split('/');
            let c1 = myVar1.map(str => {
              return Number(str);
            });

            let myVar2 = val.split('/');
            let c2 = myVar2.map(str => {
              return Number(str);
            });

            if (c1[0] > c2[0])
                return obj;
            if (c1[0] == c2[0] && c1[1] > c2[1])
                return obj;
            if (c1[0] == c2[0] && c1[1] == c2[1] && c1[2] >= c2[2])
                return obj;
          });
        }
        this.dessertsDisplayForSelect =  Object.assign([],this.dessertsDisplay);

        let removedEl=['全部'];
        for (let i = 0; i < this.dessertsDisplay.length; i++) {
          removedEl.push(this.dessertsDisplay[i].stkRecord_supplier)
        }
        this.itemsForSelect = [...new Set(removedEl)];
        this.selectedItems = Object.assign([], this.itemsForSelect);
        this.isAllSelected=true;

        this.getSumForDisplay();
      }
    },

    compareDateEnd(val) {
      if (val!='') {
        let tem_len=this.desserts.length;
        for (let i=0; i < tem_len; i++) {
          //this.desserts = this.desserts.filter(function( obj ) {
          this.dessertsDisplay = this.dessertsDisplay.filter(function( obj ) {
            let myVar2 = obj.stkRecord_Date.split('/');
            let c2 = myVar2.map(str => {
              return Number(str);
            });

            let myVar1 = val.split('/');
            let c1 = myVar1.map(str => {
              return Number(str);
            });

            if (c1[0] > c2[0])
                return obj;
            if (c1[0] == c2[0] && c1[1] > c2[1])
                return obj;
            if (c1[0] == c2[0] && c1[1] == c2[1] && c1[2] >= c2[2])
                return obj;
          });
        }
        this.dessertsDisplayForSelect =  Object.assign([],this.dessertsDisplay);

        let removedEl=['全部'];
        for (let i = 0; i < this.dessertsDisplay.length; i++) {
          removedEl.push(this.dessertsDisplay[i].stkRecord_supplier)
        }
        this.itemsForSelect = [...new Set(removedEl)];
        this.selectedItems = Object.assign([], this.itemsForSelect);
        this.isAllSelected=true;

        this.getSumForDisplay();
      }
    },
    */
    //theta ===
    compareDatePeriod(val) {
      if (val!='') {
        let tem_len=this.desserts.length;
        //let tem_len = this.dessertsDisplayForSelect.length;

        for (let i=0; i < tem_len; i++) {
          //this.desserts = this.desserts.filter(function( obj ) {
          this.dessertsDisplay = this.this.desserts.filter(function( obj ) {
            let myVar2 = obj.spindleStockIn_period.split('/');
            let c2 = myVar2.map(str => {
              return Number(str);
            });

            let myVar1 = val.split('/');
            let c1 = myVar1.map(str => {
              return Number(str);
            });

            console.log("效期, date: ", c1, c2)
            if (c1[0] > c2[0])
                return obj;
            if (c1[0] == c2[0] && c1[1] > c2[1])
                return obj;
            if (c1[0] == c2[0] && c1[1] == c2[1] && c1[2] >= c2[2])
                return obj;
          });
        }
        this.dessertsDisplayForSelect =  Object.assign([],this.dessertsDisplay);

        this.load_SingleTable_ok=false;
      }
    },

    compareDate(val) {
      if (val!='') {
        let tem_len=this.desserts.length;
        //let tem_len = this.dessertsDisplayForSelect.length;
        console.log("watch, compareDate: ", val, tem_len)

        for (let i=0; i < tem_len; i++) {
          //this.desserts = this.desserts.filter(function( obj ) {
          this.dessertsDisplay =  this.desserts.filter(function( obj ) {
            let myVar1 = obj.spindleStockIn_date.split('/');
            let c1 = myVar1.map(str => {
              return Number(str);
            });

            let myVar2 = val.split('/');
            let c2 = myVar2.map(str => {
              return Number(str);
            });

            if (c1[0] > c2[0])
                return obj;
            if (c1[0] == c2[0] && c1[1] > c2[1])
                return obj;
            if (c1[0] == c2[0] && c1[1] == c2[1] && c1[2] >= c2[2])
                return obj;
          });
        }
        console.log("watch, dessertsDisplay: ", this.dessertsDisplay, this.dessertsDisplay.length)
        this.dessertsDisplayForSelect =  Object.assign([],this.dessertsDisplay);
      }
    },

    compareDateEnd(val) {
      if (val!='') {

        let tem_len=this.desserts.length;
        //let tem_len = this.dessertsDisplayForSelect.length;
        console.log("watch, compareDateEnd: ", val, tem_len)
        for (let i=0; i < tem_len; i++) {
          //this.desserts = this.desserts.filter(function( obj ) {
          this.dessertsDisplay = this.desserts.filter(function( obj ) {
            let myVar2 = obj.spindleStockIn_date.split('/');
            let c2 = myVar2.map(str => {
              return Number(str);
            });

            let myVar1 = val.split('/');
            let c1 = myVar1.map(str => {
              return Number(str);
            });

            if (c1[0] > c2[0])
                return obj;
            if (c1[0] == c2[0] && c1[1] > c2[1])
                return obj;
            if (c1[0] == c2[0] && c1[1] == c2[1] && c1[2] >= c2[2])
                return obj;
          });
        }
        this.dessertsDisplayForSelect =  Object.assign([],this.dessertsDisplay);
      }
    },
    //theta ===

    load_SingleTable_ok(val) {
      if (val) {
        // 篩選出 aufnr 不是空陣列的物件
        let filteredArr = this.temp_desserts.filter(item => item.aufnr.length > 0);
        // 依據 aufnr 陣列的內容來擴展每個物件，並排除 aufnr 屬性
        this.desserts = filteredArr.flatMap(item => item.aufnr.map(subItem => {
          let { aufnr, ...rest } = item;
          return {...rest, ...subItem};
        }));
        // 新增object內的key(isGridChange), false: grid資料沒有更改
        this.desserts = this.desserts.map(v => ({...v, isGridChange: false}))
        this.dessertsDisplay = Object.assign([], this.desserts);
        console.log("dessertsDisplay: ", this.dessertsDisplay);

        this.dessertsDisplayForSelect =  Object.assign([],this.dessertsDisplay);

        this.isLoading = false;

        this.load_SingleTable_ok=false;
      }
    },
  },

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm != 1) {
    //if (this.currentUser.perm < 1) {
      this.permDialog=true;
    }
    this.stockOutTag_EmpID = this.currentUser.empID;

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.today = new Date();

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listStockRecords();
  },

  methods: {
    initialize() {
        this.load_SingleTable_ok=false;
        this.listStockRecords();
    },

    listStockRecords() {    //從後端讀取dataTable的資料
      console.log("listStockRecords, Axios get data...")

      this.isLoading = true;     //2023-07-21 add
      const path = '/listStockRecords';
      axios.get(path)
      .then((res) => {
        this.temp_desserts = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs);
        this.load_SingleTable_ok=true;    //true: dataTable的資料ok
      })
      .catch((error) => {
        console.error(error);
        this.isLoading = true;     //2023-07-21 add
        this.load_SingleTable_ok=false;
      });
    },

    exportToExcel() {
      console.log("StockRecord, exportToExcel, Axios post data...")

      let obj= {
        spindleIn_workID: '製令單號',
        spindleStockIn_type_cat: '類別 / 型號',
        spindleStockIn_date: '入庫日期',
        spindleStockIn_employer: '入庫人員',
        spindleStockIn_period: '效期',
        spindleStockOut_date: '出庫日期',
        spindleStockOut_employer: '出庫人員',
        spindleStockIn_st_lay: '儲位',
        comment: '說明',
        date_comment: '日期',
      }

      let object_Desserts = Object.assign([], this.dessertsDisplay);
      object_Desserts.unshift(obj);

      const path = '/exportToExcelForStock';
      var payload= {
        blocks: object_Desserts,
        count: object_Desserts.length,
        name: this.currentUser.name,
      };
      axios.post(path, payload)
      .then((res) => {
        console.log("export into excel status: ", res.data.status, res.data.outputs)
        if (res.data.status) {
          this.showTosterForOK('庫存記錄('+ res.data.outputs + ')轉檔完成!')
          /*
          this.snackbar_color='#008184';
          this.snackbar=true;
          this.snackbar_info= '庫存記錄('+ res.data.outputs + ')轉檔完成!';
          this.snackbar_icon_color= "#ffffff";
          */
        } else {
          this.showTosterForError('存檔錯誤!')
          /*
          this.snackbar_color='red accent-2';
          this.snackbar=true;
          this.snackbar_info= '存檔錯誤!';
          this.snackbar_icon_color= '#adadad';
          */
        }
      })
      .catch((error) => {
        console.error(error);
        this.showTosterForError('錯誤! API連線問題...')
        /*
        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= '存檔錯誤!';
        this.snackbar_icon_color= '#adadad';
        */
      });
    },
    /*
    checkSelect(e) {
      let ck=e.includes('全部');
      console.log('Select... ', e, ck, this.isAllSelected);
      if (ck) {  //press全部, 且不是全部的狀態
        if (this.isAllSelected) {
          this.isAllSelected = false;
          this.selectedItems = [];
          for (let i=1; i<e.length; i++) {
            this.selectedItems.push(e[i])
          }
        } else {
          console.log('Select all...');
          this.selectedItems = [];
          for (let i=0; i<this.itemsForSelect.length; i++) {
            this.selectedItems.push(this.itemsForSelect[i])
          }
          this.isAllSelected = true;
        }
      } else if (this.isAllSelected) {  //取消全部, 且不是全部的狀態
        console.log('Remove all...');
        this.selectedItems = [];
        this.isAllSelected = false;
      } else {  //取消全部, 且不是全部的狀態
        console.log('Click some item...');
        this.selectedItems = [];
        for (let i=0; i<e.length; i++) {
          let jj=this.itemsForSelect.includes(e[i])
          console.log('item1...', jj);
          if (jj) {
            this.selectedItems.push(e[i])
            console.log('item2...', e[i]);
          }
        }
        console.log('length...', e.length, this.itemsForSelect.length);
        if (e.length==this.itemsForSelect.length-1) {
            this.selectedItems.unshift('全部')
            this.isAllSelected = true;
        }
      } //end else if

      console.log('item3...');

      if (this.selectedItems != []) {
        console.log('item4...');
        //this.dessertsDisplay = this.desserts.filter(val => this.selectedEmployers.includes(val.stockInTag_Employer));
        this.dessertsDisplay = this.dessertsDisplayForSelect.filter(val => this.selectedItems.includes(val.stkRecord_supplier));
      }
    },

    getExpand(value) {
      console.log("expand: ", value)
    },
    */
    filterOnlyCapsText(value, search, item) {
      return value != null &&
        search != null &&
        typeof value === 'string' &&
        value.toString().toLocaleUpperCase().indexOf(search) !== -1
    },

    getmSelect(item) {
      console.log("getmSelect: ",item);

      this.editedIndex = this.dessertsDisplay.map(object => object.spindleIn_workID).indexOf(item.spindleIn_workID);

      this.desserts[this.editedIndex].isGridChange=true;
      this.desserts[this.editedIndex].comment = item.comment;

      console.log("getmSelect, this.desserts[this.editedIndex]: ", this.desserts[this.editedIndex].comment);
    },

    getmComment(item) {
      console.log("getmComment: ",item);

      this.editedIndex = this.desserts.map(object => object.id).indexOf(item.id); //for dessertsDisplay
      console.log("getmComment, index: ", this.editedIndex, this.desserts[this.editedIndex].comment);

      this.commentForInventory=this.commentForInventory.trim()
      console.log("comment: ", this.commentForInventory, this.commentForInventory.length)
      if (this.commentForInventory.length != 0) {
        this.desserts[this.editedIndex].isGridChange=true;
        this.desserts[this.editedIndex].comment = this.commentForInventory;
        this.comment_items.unshift(this.commentForInventory);
        this.commentForInventory='' // 2023-07-13 add
      }
      console.log("getmComment, this.desserts[this.editedIndex]: ", this.desserts[this.editedIndex].comment);
    },

    updateStockInDataByInv() {
      console.log("updateStockInDataByInv, Axios post data...", this.desserts);

      const path = '/updateStockInDataByInv';
      var payload= {
        blocks: this.desserts,
        count: this.desserts.length,
        empID: this.currentUser.empID    //2023-07-13 add
      };
      axios.post(path, payload)
      .then((res) => {
        console.log("update inTag data status: ", res.data.status)
        if (res.data.status)
          this.showTosterForOK('資料更新完成!')
        else
          this.showTosterForError('存檔錯誤! ' + res.data.message)
      })
      .catch((error) => {
        console.error(error);
        this.showTosterForError('錯誤! API連線問題...');
      });

    },
    /*
    getSumForDisplay() {
      let result = [this.dessertsDisplay.reduce(function(agg, item) {
        agg[item.stkRecord_reagID] = (agg[item.stkRecord_reagID] || 0) + parseInt(item.stkRecord_inStock_count)
        return agg;
      }, {})]
      const temp_l=Object.keys(result[0]).length;

      for (let j = 0; j < temp_l; j++) {
        let kk = this.dessertsDisplay.find(element => {
          let temp=result.map(item => Object.keys(item)[j]);
          return element.stkRecord_reagID==temp[0];
        });

        let idx = this.dessertsDisplay.indexOf(kk);
        let temp_val=result.map(item => Object.values(item)[j]);

        this.dessertsDisplay[idx].stkRecord_sum=temp_val[0];
      }
    },
    */
    setRowBackground(item) {
      let targetDate1=0
      let targetDate2=0

      if (item.spindleStockOut_date != '') {
        const parts = item.spindleStockOut_date.split('/');
        const year = parseInt(parts[0]) + 1911; // 將民國年轉換為西元年
        const month = parseInt(parts[1]) - 1; // JavaScript 的月份從 0 開始
        const day = parseInt(parts[2]);
        targetDate1 = new Date(year, month, day);
      }

      if (item.spindleStockIn_period != '') {
        const parts = item.spindleStockIn_period.split('/');
        const year = parseInt(parts[0]) + 1911; // 將民國年轉換為西元年
        const month = parseInt(parts[1]) - 1; // JavaScript 的月份從 0 開始
        const day = parseInt(parts[2]);
        targetDate2 = new Date(year, month, day);
      }

      let have_date_out = false;
      if (targetDate1 > targetDate2 && targetDate1 !=0 && targetDate2 != 0) {
        // 出庫日期大於效期，設定 flag 為 true
        console.log('出庫日期大於效期');
        have_date_out = true;
      }

      let have_date_period = false;
      if (this.today > targetDate2 && targetDate1==0) {
        // 當天日期大於效期，設定 flag 為 true
        console.log('當天日期大於效期');
        have_date_period = true;
      }

      if (have_date_out && !have_date_period)
        return 'green-background';

      if (!have_date_out && have_date_period)
        return 'red-background';

      if (!have_date_out && have_date_period)
        return '';


      /*
      const rowClass1='red-background';
      const rowClass2='';
      let rowClass = (have_date_period) ? rowClass1 : rowClass2;

      return rowClass;
      */
    },

    save() {
      console.log('Dialog click save')
    },

    cancel() {
      console.log('Dialog click cancel')
    },

    open() {
      console.log('Dialog open')
    },

    close() {
      console.log('Dialog closed')
    },
    /*
    myFilter() {
      this.checkSafeStock();
    },
    */
    /*
    //查詢 4(針對安全存量)
    checkSafeStock() {
      let removedEl=[];
      let orangeEl= Object.assign([], this.dessertsDisplay);

      let c1=this.compareSafeStock; //blank: isNaN(c1)=true
      for (let i = 0; i< orangeEl.length && c1; i++) {
        let s_unit = orangeEl[i].stkRecord_s_unit;        //入庫單位
        let c_unit = orangeEl[i].stkRecord_c_unit;        //在庫單位
        let s_cnt = orangeEl[i].stkRecord_saftStock;      //安全存量
        let c_cnt = orangeEl[i].stkRecord_cnt;            //在庫數量
        let scale = c_cnt / orangeEl[i].stkRecord_scale;  //入出庫單位比例
        let result=s_unit.localeCompare(c_unit);
        //顯示庫存不足資料
        let c2=((result==0) && (c_cnt < s_cnt))?true:false;
        let c3=((result!=0) && (c_cnt < scale))?true:false;
        //console.log("stock: ", i, result, c2, c3, c_cnt, s_cnt, scale, orangeEl[i].stkRecord_reagID)
        if (c2 || c3)
          removedEl.push(orangeEl[i]);
      }

      if (removedEl.length!=0 && c1)
        this.initialize(removedEl);
      else
        this.initialize(orangeEl);
    },
    */
    permCloseFun() {
      this.permDialog = false
      console.log("press permission Close Button...");
      this.$router.push('/navbar');
    },
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
  //background-color:var(--navbar-header-color);
  background-color:#5a96cc;
}

::v-deep .v-data-table-header th {
  font-size: 0.9em !important;
}

::v-deep .v-data-table td {
  font-size: 12px !important;
}

::v-deep .v-label {
  /*font-size: 1em*/
  font-size: 14px;
}

::v-deep .v-label--active {
  /*font-size: 1em*/
  font-size: 14px;
  font-weight: bold;
}

::v-deep input::placeholder {
  font-size: 14px;
}
/*
::v-deep .v-text-field {
  width: 160px;
}
*/
::v-deep .v-input--selection-controls__input {
  margin-top: -8px;
}

::v-deep .v-input--checkbox {
  margin-top: 8px;
}
/*
::v-deep .v-text-field--box .v-input__slot, .v-text-field--outline .v-input__slot{
  min-height:36px !important;
  min-height: 36px !important;
  margin-top: 10px;
}
*/
::v-deep div.v-input__slot {
  min-height: 36px !important;
  margin-top: 14px;
  max-width: 140px !important;
}

::v-deep .v-input__prepend-outer {
  margin-right: 9px;
  margin-top: 14px;
}
/* for data table的header間距 start*/
::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  padding-left: 8px !important;
  padding-right: 0px !important;
}
::v-deep .v-data-table > .v-data-table__wrapper > table > tbody > tr > td {
  padding-left: 8px !important;
  padding-right: 0px !important;
}
/* */
/* for data table的header, 最後一個row的color start*/
::v-deep .sum_class span {
  color: #1f4788 !important;
}
/* */

/*
::v-deep div.v-input__control > div.v-input__slot > fieldset {
  width: 170px;
}
*/
//::v-deep div.v-input__control {
//  max-width: 140px !important;
//}
/* for excel按鍵 start*/
.excel_wrapper {
  position: relative;
  top: -4px !important;
  right: -72px !important;
  width: 90px !important;
}
/* */

/* for 關鍵字查詢 start*/
::v-deep div.v-input.style-0 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  max-width: 120px !important;  /*2023-06-02 modify 100px => 120px */
  width: 120px !important;      /* */
}

::v-deep div.v-input.style-0 > .v-input__control > .v-input__slot {
  max-width: 120px !important;  /*2023-06-02 modify 100px => 120px */
  width: 120px !important;      /* */
}
/* */
/*
::v-deep div.v-input.style-1 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  min-width: 350px !important;
  width: 350px !important;
}

::v-deep div.v-input.style-1 > .v-input__control > .v-input__slot {
  min-width: 350px !important;
  width: 350px !important;
}
*/
/* for 安全存量 start*/
::v-deep .myCheckbox {
  position: relative;
  top: -8px !important;
  right: -62px !important;
}
::v-deep .myCheckbox > .v-input__control > .v-input__slot > .v-text-field__slot > label{
  max-width: 120px !important;
  width: 120px !important;
}
::v-deep .myCheckbox > .v-input__control > .v-input__slot{
  max-width: 120px !important;
  width: 120px !important;
}
/* */
/* for 效期查詢 start*/
::v-deep .style-2 {
  position: relative;
  right: -15px !important;
}
::v-deep div.v-input.style-2 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  max-width: 70px !important;
  width: 70px !important;
}
::v-deep div.v-input.style-2 > .v-input__control > .v-input__slot {
  max-width: 70px !important;
  width: 70px !important;
}
/* */
/* for 入庫日期查詢 start*/
::v-deep div.v-input.style-3 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  max-width: 120px !important;
  width: 120px !important;
}
::v-deep div.v-input.style-3 > .v-input__control > .v-input__slot {
  max-width: 120px !important;
  width: 120px !important;
}
/* */
/*-- for v-select begin--*/
::v-deep .style-4 {
  position: relative;
  right: -28px !important;
  top: -8px !important;
}
::v-deep div.v-input.style-4 > .v-input__control >.v-input__slot > .v-select__slot > .v-select__selections > input {
  max-width: 100px !important;
  width: 120px !important;
  height: 40px !important;

  //text-overflow: ellipsis;
  //white-space: nowrap;

  overflow-y: hidden !important;
}
::v-deep div.v-input.style-4 > .v-input__control >.v-input__slot > .v-select__slot > .v-label {
  margin-top: 4px;
  top: 12px;
  font-size: 14px;;
}
::v-deep .v-list--dense .v-list-item, .v-list-item--dense {
  min-height: 30px !important;
  height: 30px !important;
}
::v-deep .v-select.v-input--dense .v-select__selection--comma {
  font-size: 14px !important;
  margin: 5px 4px 3px 0 !important;
}
::v-deep div.v-input.style-4 > .v-input__control > .v-input__slot {
  max-width: 100px !important;
  width: 120px !important;
  height: 40px !important;
  top: 10px !important;
  overflow-y: hidden !important;
}
::v-deep div.v-input.style-4 > .v-input__control > .v-input__slot > .v-select__slot > .v-select__selections {
  max-width: 100px !important;
  width: 120px !important;
  height: 40px !important;

  //text-overflow: ellipsis;
  //white-space: nowrap;

  overflow-y: hidden !important;
  margin-top: 12px !important;
}
/* */
::v-deep .v-data-table__expand-icon {
  color: red;
}

::v-deep .v-input.myText input {
  font-size: 0.7em;
}

/*-- 以顏色識別最後一筆資料 begin--*/
//::v-deep .v-data-table >.v-data-table__wrapper > table > tbody > tr:last-child {
//  background: #7DA79D;
//}
/* */
/*
::v-deep .v-select__selections {
  overflow-y: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-height: 50px;
}
*/
/*
small.msgErr {
  font-size: 80%;
  color: red;
  margin-top: -20px;
}
*/

::v-deep .v-list-item__title {
  font-size: 14px !important;
  font-weight:bold;
  //color: red;
}

.side {
    position: absolute;
    backface-visibility: hidden;
    width: 100%;
    height: 100%;
    display: flex;
    /*justify-content: center;
    align-items: center;*/
    /*font-size: 4em;
    font-weight: bold;*/
}

.default-side {
    transform: translateZ(20px);
}

.hover-side {
    transform: rotateX(90deg) translateZ(20px);
}


.flip_wrapper {
    perspective: 800px;
}

.flip_btn {
    position: relative;
    top: -18px !important;
    height: 20px;
    width: 130px;
    transform-style: preserve-3d;
    transition: transform 500ms ease-in-out;
    transform: translateZ(-20px);
}

.flip_btn:hover {
    transform: rotateX(-90deg) translateY(20px);
}

.excel_wrapper {
    position: relative;
    top: -14px !important;
    right: -40px !important;
    width: 90px !important;
}

::v-deep .red-background {
  background-color: #ff8080;
  //color: white;
}

::v-deep .green-background {
  background-color: #ccffe6;
  //color: white;
}

::v-deep .v-data-table-top-height {
  position:relative;
  height: 90px;
  //top: 10px;
}

::v-deep .records_container {
    display: flex; /* 使用 flexbox */
    align-items: center; /* 垂直置中 */
    gap: 20px; /* 設定元素之間的間距 */
    position: relative;
    left: 150px;
}

::v-deep  .square1 {
    width: 20px; /* 設定四方形的寬度 */
    height: 20px; /* 設定四方形的高度 */
    background-color:  #ff8080; /* 設定四方形的邊常及顏色 */
    //position: relative; /* 讓內容絕對定位相對於此元素 */
  }
  ::v-deep .square2 {
    width: 20px; /* 設定四方形的寬度 */
    height: 20px; /* 設定四方形的高度 */
    background-color: #ccffe6; /* 設定四方形的邊常及顏色 */
    //position: relative; /* 讓內容絕對定位相對於此元素 */
  }
</style>