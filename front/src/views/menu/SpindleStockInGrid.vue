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
      <v-card width="98vw" class="pa-md-4 mt-n5 mx-lg-auto mb-n3">
        <v-data-table
          :headers="headersDisplay"
          :items="dessertsDisplay"
          :item-class="setRowBackground"
          :expanded.sync="expanded"
          :options.sync="pagination"
          item-key="id"
          show-expand
          dense
          style="position:relative; top:25px;"
          @current-items="currentItems"
        >
          <template v-slot:top>
            <div class="v-data-table-top-height">
              <v-toolbar flat>
                <v-toolbar-title>主軸入庫作業</v-toolbar-title>
                <v-divider class="mx-4" inset vertical />
                <v-subheader style="margin-bottom: 0px; height: 15px; font-size: 15px; font-weight: bold; position:relative; top:-15px; left:10px;">
                  <span>儲位區</span>
                </v-subheader>
              <!--
                <v-btn-toggle v-model="icon" dense borderless>
                  <v-btn value="left">
                    <span class="hidden-sm-and-down">A</span>
                    <v-icon right>mdi-format-align-left</v-icon>
                  </v-btn>

                  <v-btn value="center">
                    <span class="hidden-sm-and-down">B</span>
                    <v-icon right>mdi-format-align-center</v-icon>
                  </v-btn>

                  <v-btn value="right">
                    <span class="hidden-sm-and-down">C</span>
                    <v-icon right>mdi-format-align-right</v-icon>
                  </v-btn>

                  <v-btn value="justify">
                    <span class="hidden-sm-and-down">D</span>
                    <v-icon right>mdi-format-align-justify</v-icon>
                  </v-btn>
                </v-btn-toggle>
              -->
                <v-radio-group v-model="spindleStockIn_station" column class="top_radio_label" style="position:relative; top: 18px;">
                  <v-radio label="待跑合A區" color="red" value="1" style="margin-bottom: 0px;" />
                  <v-radio label="待校正B區" color="red" value="2" style="margin-bottom: 0px;" />
                  <v-radio label="待測試C區" color="red" value="3" style="margin-bottom: 0px;" />
                  <v-radio label="異常處理D區" color="red" value="4" style="margin-bottom: 0px;" />
                </v-radio-group>

                <v-subheader style="margin-bottom: 0px; height: 15px; font-size: 15px; font-weight: bold; position:relative; top:-15px; left:10px;">
                  <span>產品類別</span>
                </v-subheader>
                <v-radio-group
                  v-model="spindleStockIn_type"
                  @change="checkRadio"
                  column
                  class="top_radio_label">
                  <v-radio value="1" label="銑削/研磨主軸(自動換刀)" color="green" style="margin-bottom: 0px;" />
                  <v-radio value="2" label="研磨主軸(手動換刀)" color="green" style="margin-bottom: 0px;" />
                  <v-radio value="3" label="修砂主軸(手動換刀)" color="green" style="margin-bottom: 0px;" />
                </v-radio-group>

                <v-select
                  :items="spindleStockIn_cat_array"
                  label="型號"
                  style="position: relative;top: -5px; left: 25px; width: 150px; max-width: 150px;"
                  dense
                  outlined
                  v-model="spindleStockIn_cat"
                  @change="checkSelect"
                ></v-select>

                <v-subheader style="margin-bottom: 0px; height: 15px; font-size: 15px; font-weight: bold; position:relative; top:-15px; left:10px;">
                <span style="position:relative; left:25px;">效期</span>
                </v-subheader>
                <v-menu
                  v-model="fromDateMenuP"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  max-width="280px"
                  min-width="280px"
                  style="display: inline-block; vertical-align: middle;"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      placeholder="預計出庫日期"
                      prepend-icon="event"
                      readonly
                      :value="fromDateDispP"
                      v-model="fromDateTempP"
                      v-on="on"
                      style=" position:relative; left:25px; width: 150px !important; max-width:150px!important;"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    locale="zh-TW"
                    :min="minDate"
                    :max="maxDate"
                    v-model="fromDateValP"
                    no-title
                    @input="fromDateMenuP = false"
                  ></v-date-picker>
                </v-menu>
                <v-text-field
                  v-model="spindleStockIn_workID"
                  label="製令單號"
                  style="position: relative; left: 50px;width: 120px;max-width: 120px;"
                  single-line
                  :rules="rules"
                  counter
                  maxlength="11"
                  @keydown="handleKeyDown"
                ></v-text-field>
                <!--入庫確認dialog-->
                <v-dialog v-model="writeDialog" max-width="500px">
                  <v-card>
                    <v-card-title class="text-h5">確定入庫?</v-card-title>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="closeWriteDialog">取消</v-btn>
                      <!--<v-btn color="blue darken-1" text @click="write" :disabled='checkDataForSaveButton'>確定</v-btn>-->
                      <v-btn color="blue darken-1" text @click="write">確定</v-btn>
                      <v-spacer></v-spacer>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <!--入庫權限dialog-->
                <v-dialog v-show="rightDialog"
                  v-model="rightDialog"
                  transition="dialog-bottom-transition"
                  max-width="500"
                >
                  <v-card>
                    <v-toolbar
                      color="primary"
                      dark
                    >錯誤訊息!</v-toolbar>
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
            </div>
          </template>

          <template v-slot:no-data>
            <v-btn color="primary" @click="initialize">
              目前沒有資料, 重新讀取
            </v-btn>
          </template>

          <template v-slot:[`item.actions`]="{ item }">
              <v-icon
                v-show="item.isSelect"
                size="24"
                class="mr-2 custom-icon"
                @click="writeItem(item)"
                style="color: blue;"
              >
              mdi-table-plus
              </v-icon>
          </template>

          <!--剩餘數量總合欄位-->
          <template v-slot:item.count="props">
            <div>{{ sum_wip(props.item) }}</div>
          </template>

          <!--水位欄位-->
        <!--
          <template v-slot:item.spindleIn_workID="props">
            <v-text-field
              v-model="props.item.spindleIn_workID"
              style="width: 100px; position: relative; top: 18px;""
              @input="getmData(props.item)"
              outlined
              dense
              single-line
            ></v-text-field>
          </template>
        -->
          <template v-slot:expanded-item="{ headers, item, isExpanded }">
            <td v-if="item.aufnr.length" :colspan="headers.length">  <!-- 定義擴展內容 -->
                <template>
                  <v-simple-table dense fixed-header>
                    <template v-slot:default>
                      <thead>
                        <tr>
                          <th class="text-left">
                            製令單號(#)
                          </th>
                          <th class="text-left">
                            類別
                          </th>
                          <th class="text-left">
                            型號
                          </th>
                          <th class="text-left">
                            入庫人員
                          </th>
                          <th class="text-left">
                            入庫日期
                          </th>
                          <th class="text-left">
                            效期
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="(detail, index) in item.aufnr"
                          :key="index"
                          style="font-weight:bold;"
                        >
                          <td>{{ detail.spindleIn_workID }}</td>
                          <td>{{ detail.spindleStockIn_type }}</td>
                          <td>{{ detail.spindleStockIn_cat }}</td>
                          <td>{{ detail.spindleStockIn_employer }}</td>
                          <td>{{ detail.spindleStockIn_date }}</td>
                          <td>{{ detail.spindleStockIn_period }}</td>
                        </tr>
                      </tbody>
                    </template>
                  </v-simple-table>
                </template>

            </td>
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

import Common from '../../mixin/common.js';
import Key from '../../mixin/key.js';
import Notification from '../../mixin/notification.js'

import { _createCSSWithConstants } from '../../mixin/constant.js';

export default {
  name: 'SpindleStockInGrid',

  mixins: [Common, Key, Notification],

  mounted() {
    // 設定 window.onpopstate 的處理程序
    window.onpopstate = () => {
      console.log("press back button, good bye...");

      const userData = JSON.parse(localStorage.getItem('loginedUser'));
      userData.setting_items_per_page = this.pagination.itemsPerPage;
      localStorage.setItem('loginedUser', JSON.stringify(userData));
    };

    //this.toggleFromDateMenu();

    // 設定每180秒執行一次 myWork 函式
    //const timeValue=3 * 60 * 1000;
    //this.intervalId = setInterval(this.initialize, timeValue);
  },

  data: () => ({
    currentUser: { },
    permDialog: false,    //權限dialog, true:open
    rightDialog: false,   //無權限dialog, true:open
    dialog: false,
    writeDialog: false,

    pagination: {
      //itemsPerPage: 10,   //預設值, rows/per page
      //page: 1,
    },
    /*
    snackbar: false,
    snackbar_color: 'success',
    snackbar_right: true,
    snackbar_top: true,
    snackbar_info: '',
    snackbar_icon_color: '#adadad',
    */
    spindleStockIn_station: '0',
    spindleStockIn_type: '0',
    spindleStockIn_cat: '',
    spindleStockIn_workID: '',
    spindleStockIn_date: '',

    fromDateTempP: '',
    fromDateMenuP: {}, // 用於跟踪每個項目的 v-date-picker 狀態
    activeItemId: null, // 用於跟踪當前活動的項目 ID
    rules: [v => v.length <= 11 || '最大11位數字'],

    //資料表頭
    headersDisplay: [
      { text: 'ID', sortable: false, value: 'id', align: 'start', width: '5%'},
      { text: '儲位區', sortable: true, value: 'spindleStockIn_station'},
      { text: '層別', sortable: false, value: 'spindleStockIn_layout'},
      { text: '目前數量', sortable: false, value: 'count'},
      { text: 'Actions', sortable: false, value: 'actions', width: '25%'},
    ],

    temp_desserts: [],
    /*
    temp_desserts: [
      {
        'aufnr': [
          {
          'spindleIn_workID': '20240401',
          'spindleStockIn_type': '研磨主軸(手動換刀)' ,
          'spindleStockIn_cat': 'THG-150.01' ,
          'spindleStockIn_employer': '吳發財' ,
          'spindleStockIn_date': '2024/04/01' ,
          'spindleStockIn_period': '2024/04/03' ,
          'last': 1,
          },
          {
          'spindleIn_workID': '20240329',
          'spindleStockIn_type': '研磨主軸(手動換刀)' ,
          'spindleStockIn_cat': 'THG-150.01' ,
          'spindleStockIn_employer': '吳發財' ,
          'spindleStockIn_date': '2024/03/29' ,
          'spindleStockIn_period': '2024/04/01' ,
          'last': 1,
          },
        ],
        'id': 1,
        'spindleIn_station': '待跑合A區',
        'spindleIn_layout': 1,
        'spindleStockIn_total_size': 1,
        'isSelect':false,
      },
    ],
    */
    dessertsDisplay: [],
    desserts: [],
    expanded: [],

    search: '',
    headersSearch: [
      { text: '製令單號', sortable: true, value: 'spindleIn_workID' },
      { text: '狀態', sortable: true, value: 'spindleIn_runinState' }, //待跑合/待檢修
      { text: '類別 / 型號', sortable: true, value: 'spindleIn_type_and_cat' },
      { text: '效期', sortable: true, value: 'spindleIn_period' },
      { text: '入庫日期', sortable: true, value: 'spindleIn_date' },
      { text: '入庫人員', sortable: true, value: 'spindleIn_employer' },
    ],
    dessertsSearch: [],
    dessertsNew: {},
    //temp_dessertsSearch: [],

    spindleIndex: -1,
    editedIndex: -1,
    editedItem: {},

    intervalId: null,
    IDErrMsg: '',

    load_SingleTable_ok: false,
    load_2thTable_ok: false,
    load_3thTable_ok: false,

    tags: [
      "銑削/研磨主軸(自動換刀)",
      "研磨主軸(手動換刀)",
      "修砂主軸(手動換刀)",
    ],

    spindle_cat_array: ['TH-120.01(400V)','TH-120.02(230V)','TH-150.01(380V)','TH-150.02(220V)', 'THS-210.01(400V)', 'THS-255.01(400V)', 'THG-170.01(400V)', 'THAV-100', 'THSGD-H140', 'THSGD-H150'],

    clickMenuP: false,
    fromDateMenuP: false,
    fromDateValP: '',
    compareDate: '',
    minDate: "2012-07-01",
    maxDate: "2042-06-30",

    items: [],
    temp_items: [],
    temp_items_index: -1,
    spindle_isAll: false,

    spindleStockIn_workID_isOK: false,

    spindleStockIn_cat_array: [],

    return_type_cat: true,

    currentDisplayDesserts:[],
  }),

  computed: {
    checkDataForSaveButton() {
      if (parseInt(this.spindleStockIn_station)>0 && parseInt(this.spindleStockIn_type)>0 &&
          !!this.spindleStockIn_cat && !!this.spindleStockIn_workID && this.spindleStockIn_workID.length==11) {
        return false;
      } else {
        return true
      }
    },

    sum_wip() {
      return (item) => {
        let temp_sum=item.aufnr.reduce((total, item) => total + item.last, 0);  //累加
        return temp_sum;
      };
    },

    fromDateDispP() {
      if (this.fromDateTempP == '' && this.fromDateValP == '') {
        let curDate = new Date();

        let stockin_date = curDate;
        stockin_date.setDate(stockin_date.getDate());
        let stockin_date_val=stockin_date.toISOString().substr(0, 10);
        let parts = stockin_date_val.split('-');
        let year = parseInt(parts[0]); // 年份
        let month = parseInt(parts[1]); // 月份
        let day = parseInt(parts[2]); // 日份
        // 轉換年份為民國年格式
        let rocYear = year - 1911; // 將年份減去1911
        // 重新組合日期字串為民國年格式
        this.spindleStockIn_date = rocYear.toString() + '/' + month.toString().padStart(2, '0') + '/' + day.toString().padStart(2, '0');

        // 將當前日期加上7天
        curDate.setDate(curDate.getDate() + 7);
        // 格式化日期為 'YYYY-MM-DD' 字符串
        this.fromDateValP = curDate.toISOString().substr(0, 10);

        parts = this.fromDateValP.split('-');
        year = parseInt(parts[0]); // 年份
        month = parseInt(parts[1]); // 月份
        day = parseInt(parts[2]); // 日份
        // 轉換年份為民國年格式
        rocYear = year - 1911; // 將年份減去1911
        // 重新組合日期字串為民國年格式
        this.fromDateTempP = rocYear.toString() + '/' + month.toString().padStart(2, '0') + '/' + day.toString().padStart(2, '0');

        this.fromDateValP='';
        return;
      }

      if (this.clickMenuP) {
        if (!(this.fromDateTempP != '' && this.fromDateValP == '')) {
          let parts = this.fromDateValP.split('-');
          let year = parseInt(parts[0]);  // 年份
          let month = parseInt(parts[1]); // 月份
          let day = parseInt(parts[2]);   // 日份
          // 轉換年份為民國年格式
          let rocYear = year - 1911; // 將年份減去1911
          // 重新組合日期字串為民國年格式
          this.fromDateTempP = rocYear.toString() + '/' + month.toString().padStart(2, '0') + '/' + day.toString().padStart(2, '0');

          this.fromDateValP='';
        }
        this.clickMenuP=false;
        return;
      }

      if (this.fromDateTempP != '' && this.fromDateValP == '') {
        return;
      }
    },

    checkSpindleTypeAndCat() {
      this.return_type_cat = false;
      this.spindleIndex = -1;
      let temp_type = (this.spindleStockIn_type == "1") ?  '銑削/研磨主軸(自動換刀)': (this.spindleStockIn_type == "2") ? '研磨主軸(手動換刀)' : (this.spindleStockIn_type == "3") ? '修砂主軸(手動換刀)' : "";

      this.temp_items_index = this.temp_items.findIndex(o => o.spindle_cat == this.spindleStockIn_cat && o.spindle_type == temp_type);
      if (this.temp_items_index != -1) {
        this.return_type_cat = true;
        this.spindle_isAll=this.temp_items[this.temp_items_index].isAll
      }

      console.log("return_type_cat: ", this.return_type_cat);
      return this.return_type_cat;
    },
  },

  watch: {
    writeDialog (val) {
      val || this.closeWriteDialog()
    },

    fromDateMenuP(newValue, oldValue) {
      if (newValue && !oldValue)
        this.clickMenuP=false;
      if (!newValue && oldValue)
        this.clickMenuP=true;
    },

    spindleStockIn_workID(val) {
      let isRule = /[0-9]{11}$/;

      let result = this.spindleStockIn_workID.search(isRule);
      let len = this.spindleStockIn_workID.length
      let matchResult = false;
      this.spindleStockIn_workID_isOK=false;

      this.dessertsDisplay.forEach(item => {
        if (matchResult)
          return;
        item.aufnr.forEach(innerItem => {
          if (innerItem.spindleIn_workID == this.spindleStockIn_workID) {
            matchResult = true;
            return;
          }
        });
      });

      if (result != -1 && len==11) {
        if (matchResult)
          this.showTosterForError('錯誤! 製令單號重複...')
        else {
          //if (result != -1) {
            console.log("製令單號 ok...");

            this.spindleStockIn_workID_isOK=true;
            this.dessertsDisplay.forEach(item => {
              if (item.spindleStockIn_total_size < item.spindleStockIn_max_size) {

                if (this.spindle_isAll) {
                  item.isSelect = true;
                } else {
                  item.spindles.forEach(myItem => {
                    if (myItem.type == this.spindleStockIn_type && myItem.cat == this.spindleStockIn_cat) {
                      item.isSelect = true;
                      return;
                    }
                  });
                }
              }
            });
          //} //end if
        } //end else
      }
    },

    load_3thTable_ok(val) {
      if (val) {
        this.dessertsDisplay[this.editedIndex].spindleStockIn_total_size += 1;
        this.dessertsDisplay[this.editedIndex].count += 1;

        this.dessertsDisplay[this.editedIndex].aufnr.push(this.dessertsNew);

        this.spindleStockIn_station= '0',
        this.spindleStockIn_type = '0',
        this.spindleStockIn_cat= '',
        this.spindleStockIn_workID= '';

        this.load_3thTable_ok = true;
      }
    },

    load_2thTable_ok(val) {
      if (val) {
        let i_len = this.temp_items.length;
        let temp_array=[]
        for (let i = 0; i < i_len; i++) {
          temp_array.push(this.temp_items[i].spindle_cat);
        }
        this.spindleStockIn_cat_array = [...new Set(temp_array)];

        this.load_2thTable_ok=false;
      }
    },

    load_SingleTable_ok(val) {
      if (val) {
        let temp_str=''
        let temp_id=0;
        let i_len = this.temp_desserts.length
        for (let i = 0; i < i_len; i++) {
          //temp_id +=1;
          temp_str = (this.temp_desserts[i].spindleStockIn_station === 1) ? "待跑合A區" : (this.temp_desserts[i].spindleStockIn_station === 2) ? "待校正B區" : (this.temp_desserts[i].spindleStockIn_station === 3) ? "待測試C區" : (this.temp_desserts[i].spindleStockIn_station === 4) ? "異常處理D區" : "";
          this.temp_desserts[i].station=this.temp_desserts[i].spindleStockIn_station;
          this.temp_desserts[i].spindleStockIn_station=temp_str;
        }

        this.dessertsDisplay = Object.assign([], this.temp_desserts);  //copy編輯完成的後端資料, 以作table顯示用
        this.load_SingleTable_ok=false;
      } else {
        this.listOrderFromProcess();
      }
    },
  },

  created () {
    console.log("SpindleStockInGrid, created()...");

    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    console.log("currentUser, ", this.currentUser)
    if (this.currentUser.perm < 1) {
      this.permDialog=true;
    }

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page;

        // 初始化計數器
    this.vue_render_counter = 0;

    this.initAxios();
    this.initialize();
  },

  methods: {
    currentItems(val) {
      this.currentDisplayDesserts=val;
    },

    initialize() {
      console.log("initialize()...");

      this.listStockInGrids();
    },

    listStockInGrids() {
      console.log("listStockInGrids, Axios get data...");

      const path = '/listStockInGrids';
      this.load_SingleTable_ok = false;
      axios.get(path)
      .then((res) => {
        this.temp_desserts = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs, res.data.outputs.length);
        this.load_SingleTable_ok = true;    //true: dataTable的資料ok
      })
      .catch((error) => {
        console.error(error);
        this.showTosterForError('錯誤! API連線問題...');
      });

    },

    listSpindles() {
      console.log("listSpindles...")

      const path = '/listSpindles';
      this.load_2thTable_ok = false;
      axios.get(path)
      .then((res) => {
        this.temp_items = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_2thTable_ok = true;
      })
      .catch((error) => {
        console.error(error);
        this.showTosterForError('錯誤! API連線問題...');
      });
    },

    listOrderFromProcess() {
      console.log("listOrderFromProcess(), dessertsDisplay.length, ", this.dessertsDisplay.length);

      let i_len = this.dessertsDisplay.length;
      for (let i = 0; i < i_len; i++) {
        let j_len = this.dessertsDisplay[i].aufnr.length;

        for (let j = 0; j < j_len; j++) {
          let temp_obj = {
            "spindleIn_workID": this.dessertsDisplay[i].aufnr[j].spindleIn_workID,
            "spindleStockIn_type": this.dessertsDisplay[i].aufnr[j].spindleStockIn_type,
            "spindleStockIn_cat": this.dessertsDisplay[i].aufnr[j].spindleStockIn_cat,
            "spindleStockIn_employer": this.dessertsDisplay[i].aufnr[j].spindleStockIn_employer,
            "spindleStockIn_date": this.dessertsDisplay[i].aufnr[j].spindleStockIn_date,
            "spindleStockIn_period": this.dessertsDisplay[i].aufnr[j].spindleStockIn_period,
            "last": this.dessertsDisplay[i].aufnr[j].last,
          };
          //this.temp_dessertsSearch.push(temp_obj);
        }
      }
      this.load_2thTable_ok = false;
      this.listSpindles();
    },
    /*
    showTosterForError(msg) {
      //this.tosterOK = true;   //true: 顯示錯誤訊息畫面
      this.snackbar_color='red accent-2';
      this.snackbar=true;
      this.snackbar_info= msg;
      this.snackbar_icon_color= '#adadad';
    },
    */
    checkSelect() {
      console.log("checkSelect()...");

      if (!this.checkSpindleTypeAndCat) {
        let temp_type = (this.spindleStockIn_type == "1") ?  '銑削/研磨主軸(自動換刀)': (this.spindleStockIn_type == "2") ? '研磨主軸(手動換刀)' : (this.spindleStockIn_type == "3") ? '修砂主軸(手動換刀)' : "";
        let msg='錯誤! 沒有' + temp_type + ' / ' + this.spindleStockIn_cat
        this.showTosterForError(msg);
        this.spindleStockIn_cat='';
        this.spindleStockIn_type='0';
      }
    },

    checkRadio() {
      if (this.spindleStockIn_cat != '')
        this.checkSelect();
    },

    updateStock(object) {
      console.log("updateStock(), Axios post data, object, ", object)

      let temp_type = (this.spindleStockIn_type == "1") ?  '銑削/研磨主軸(自動換刀)': (this.spindleStockIn_type == "2") ? '研磨主軸(手動換刀)' : (this.spindleStockIn_type == "3") ? '修砂主軸(手動換刀)' : "";

      let temp_obj = {
        last: 1,
        spindleIn_workID: this.spindleStockIn_workID,
        spindleStockIn_cat: this.spindleStockIn_cat,
        spindleStockIn_date: this.spindleStockIn_date,
        spindleStockIn_employer: this.currentUser.empID + ' ' + this.currentUser.name,
        spindleStockIn_period: this.fromDateTempP,
        spindleStockIn_type: temp_type,
        spindleStockIn_total_size: object.count + 1,
      };
      console.log("click updateStock, temp_obj, ", temp_obj);

      this.dessertsNew = Object.assign({}, temp_obj);  //copy編輯完成的後端資料, 以作table顯示用

      this.spindleIndex = -1;
      this.temp_items.forEach(item => {
        if (item.spindle_cat == this.spindleStockIn_cat && item.spindle_type == temp_type) {
          this.spindleIndex = item.id;
          return;
        }
      });
      console.log("spindleIndex: ", this.spindleIndex);

      this.load_3thTable_ok= false;
      let payload = {
        work_id: this.spindleStockIn_workID,  //製令單號
        empID: this.currentUser.empID,        //員工編號
        spindle_id: this.spindleIndex,        //spindle table id
        stockin_date: this.spindleStockIn_date,       //入庫日
        stockin_period: this.fromDateTempP,           //效期
        grid_id: this.editedIndex+1,
        count: 1,   //入庫數
      }
      const path='/createStockInGrids';

      axios.post(path, payload)
      .then(res => {
        console.log("update data, status: ", res.data);
        this.load_3thTable_ok= true;
      })
      .catch(err => {
        console.error(err);
        this.showTosterForError('錯誤! API連線問題...');
      });
    },

    setRowBackground(item) {
      let current_index = this.currentDisplayDesserts.map(object => object.id).indexOf(item.id);
      /*
      let current_index = this.dessertsDisplay.map(object => object.id).indexOf(item.id);
      let total_rec = this.dessertsDisplay.length;
      let total_rec_per_page = this.pagination.itemsPerPage;
      if (this.pagination.itemsPerPage == -1)
        total_rec_per_page = total_rec;
      */
      let t1= document.getElementsByClassName("v-icon notranslate v-data-table__expand-icon v-icon--link mdi mdi-chevron-down theme--light")
      if (current_index != -1) { //沒有入庫資料
        if (item.aufnr.length == 0) { //沒有入庫資料
          this.$nextTick(() => {
            t1[current_index].classList.add('my-filter');
            //t1[current_index % total_rec_per_page].classList.add('my-filter');
          });
        } else {  //有入庫資料
          //const element = t1[current_index % total_rec_per_page];
          const element = t1[current_index];
          if (element && element.classList.contains('my-filter')) {
            // 如果元素包含 my-filter 類，則刪除它
            this.$nextTick(() => {
              element.classList.remove('my-filter');
            });
          }
        }
      }

      let temp_station = (this.spindleStockIn_station == "1") ?  '待跑合A區': (this.spindleStockIn_station == "2") ? '待校正B區' : (this.spindleStockIn_station == "3") ? '待測試C區' : (this.spindleStockIn_station == "4") ?  '異常處理D區': "";
      let have_type_cat = this.spindle_isAll;
      //console.log("item.spindleStockIn_total_size: ", item.spindleStockIn_total_size, item.spindleStockIn_max_size)
      if ((item.spindleStockIn_total_size < item.spindleStockIn_max_size) &&
          //this.vue_render_counter <= 4 &&
          this.spindleStockIn_station != '' && temp_station == item.spindleStockIn_station) {
        if (!have_type_cat) {
          //let temp_type = (this.spindleStockIn_type == "1") ?  '銑削/研磨主軸(自動換刀)': (this.spindleStockIn_type == "2") ? '研磨主軸(手動換刀)' : (this.spindleStockIn_type == "3") ? '修砂主軸(手動換刀)' : "";
          item.spindles.forEach(myItem => {
            if (this.spindleStockIn_type != '' && this.spindleStockIn_cat !='' &&
               myItem.type == this.spindleStockIn_type && myItem.cat == this.spindleStockIn_cat) {
              have_type_cat = true;
              return;
            }
          });
        }

        const rowClass1='red-background';
        const rowClass2='';
        let rowClass = (have_type_cat) ? rowClass1 : rowClass2;

        return rowClass;
      }
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
    /*
    handlePopstate(event) {
      // 在這裡處理歷史記錄操作的事件
      console.log('press back button, Popstate event:', event);
    },
    */
    closeWriteDialog() {
      console.log("closeWriteDialog()...");

      this.writeDialog = false
      this.$nextTick(() => {
        //this.spindleStockIn_station = '0';
        //this.spindleStockIn_type = '0';
        //this.spindleStockIn_cat = '';
        //this.spindleStockIn_workID = '';
      })
    },

    writeItem(item) {
      console.log("writeItem(), item, ", item);

      if (this.currentUser.perm >2) {
        this.rightDialog = true;
        return;
      }

      this.editedIndex = this.dessertsDisplay.indexOf(item);
      this.editedItem = Object.assign({}, item);
      console.log("writeItem(), ", item, this.editedIndex, this.editedItem);
      this.writeDialog = true;
    },

    write() {
      console.log("write()...")

      this.closeWriteDialog()

      this.updateStock(this.editedItem);
    },

    rightCloseFun() {
      console.log("rightCloseFun()...");

      this.rightDialog = false;
    },
  },

  beforeDestroy() {
    // 離開Vue之前, 清除interval
    clearInterval(this.intervalId);
    // 離開Vue之前, 清除 window.onpopstate 的處理程序
    window.onpopstate = null;
  },
}
</script>

<style>
:root {
  --bar: scroll;
}

html {
  overflow-y: var(--bar) !important;
}
</style>

<style lang="scss" scoped>
@import url(
  'https://fonts.googleapis.com/css?family=Noto+Sans+TC:400,500&display=swap&subset=chinese-traditional'
);

div.v-toolbar__title {
  margin: 0;
  font-family: "Noto Sans TC", "Microsoft Yahei", "微軟雅黑", sans-serif;
}

::v-deep .v-data-table-header {
  //background-color: #cdfadb;
  background-color:var(--navbar-header-color);
}

::v-deep .v-data-table-header th {
  font-size: 0.9em !important;
}

::v-deep .v-label {
  font-size: 0.9em
}
::v-deep .v-label--active {
  font-size: 0.9em;
  font-weight: bold;
}

::v-deep input::placeholder {
  font-size: 14px;
}

//::v-deep .v-data-table-header th:nth-child(1) i {
//  color: blue !important;
//}

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
  color: red!important;
}

::v-deep header {
  height: 48px !important;
  margin-top: 10px !important;
}

::v-deep .v-toolbar__content {
  height: 42px !important;
}

::v-deep .v-toolbar__title {
  height: 40px !important;
}

::v-deep tbody > tr td {
  overflow: hidden !important;
  max-height: 28px !important;
  line-height: 16px !important;
  white-space: nowrap !important;
  padding-left: 8px !important;
  padding-right: 0px !important;
}

::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  padding-left: 8px !important;
  padding-right: 0px !important;
  min-width: 40px !important;
}

::v-deep .fill-width {
  overflow-x: auto;
  flex-wrap: nowrap;
}

::v-deep .v-small-dialog__actions {
  text-align: center;
}

::v-deep div.v-input.style-0 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  max-width: 120px !important;
  width: 120px !important;
}

::v-deep div.v-input.style-0 > .v-input__control > .v-input__slot {
  max-width: 120px !important;
  width: 120px !important;
}

::v-deep .v-list--dense .v-list-item, .v-list-item--dense {
    min-height: 30px !important;
    height: 30px !important;
}

::v-deep .centered-input > .v-input__control> .v-input__slot > .v-text-field__slot > input {
  text-align: center;
}

::v-deep .v-tooltip__content {
  margin-top: -30px !important;
  font-size: 12px !important;
}

::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  padding-left: 8px !important;
  padding-right: 0px !important;
  text-align: start !important;
}

::v-deep td:nth-last-child(2) .v-text-field__prefix {
  color:#1f4788;
  font-size: 12px;
}
/*
::v-deep .v-data-table__wrapper > table > tbody > tr {
  height: 18px;
}
*/
::v-deep .v-data-table__wrapper > table > tbody > tr > td:nth-last-child(2) > .v-input > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  text-align: start;
}

.side {
    position: absolute;
    backface-visibility: hidden;
    width: 100%;
    height: 100%;
    display: flex;
}

.default-side {
    transform: translateZ(20px);
}

.hover-side {
    transform: rotateX(90deg) translateZ(20px);
}

::v-deep .red-background {
  background-color: #ff8080;
  //color: white;
}

::v-deep .my-filter {
  display: none;
  visibility: hidden;
  //background-color: green;
}

::v-deep .top_radio_label {
  font-weight: bold !important;
}

::v-deep .custom-icon {
  background-color: #ff8080;
  //color: white;
  //padding: 10px;
}

::v-deep .v-data-table-top-height {
  position:relative;
  height: 90px;
  top: 10px;
}
</style>