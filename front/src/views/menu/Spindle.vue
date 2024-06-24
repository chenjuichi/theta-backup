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
      <v-card width="100vw" class="pa-md-4  mt-5 mx-lg-auto">
        <v-data-table
          :headers="headers"
          :items="desserts"
          class="elevation-1"
          :options.sync="pagination"
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>主軸產品</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="800px" :content-class="temp_css">
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
                      <v-row>
                        <v-col cols="12" md="4">
                          <v-subheader style="margin-bottom: 0; height: 15px; font-size: 15px;">
                            <span>產品類別</span>
                          </v-subheader>
                          <v-radio-group
                            v-model="editedItem.spindle_type"
                            hide-details
                            row
                            style="margin-top: 0; position: relative; left: 15px;"
                            :class="{'v-input-disable': formTitle === '編輯資料'}"
                            >
                            <v-radio value="1" label="銑削/研磨主軸(自動換刀)" color="red" :readonly="formTitle === '編輯資料'"></v-radio>
                            <v-radio value="2" label="研磨主軸(手動換刀)" color="red" :readonly="formTitle === '編輯資料'"></v-radio>
                            <v-radio value="3" label="修砂主軸(手動換刀)" color="red" :readonly="formTitle === '編輯資料'"></v-radio>
                          </v-radio-group>
                        </v-col>
                        <v-col cols="12" md="4">    <!-- 2023-04-14 modify md=3 => md=4   -->
                          <v-select
                            :items="spindle_cat_array"
                            label="型號"
                            style="position:relative; top: 10px;"
                            dense
                            outlined
                            v-model="editedItem.spindle_cat"
                            :readonly="formTitle === '編輯資料'"
                            :class="{'v-input-disable': formTitle === '編輯資料'}"
                          ></v-select>
                        </v-col>
                        <v-col class="d-flex" cols="12" md="4"></v-col>
                      </v-row>

                      <!-- 第2列-->
                      <v-row>
                        <v-col cols="12" md="4">
                          <v-select
                            :items="spindle_outer_array"
                            label="主軸外徑(mm)"
                            style="position:relative; top: 10px;"
                            dense
                            outlined
                            v-model="editedItem.spindle_outer"
                          ></v-select>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-select
                            :items="spindle_inner_array"
                            label="前軸承內徑(mm)"
                            style="position:relative; top: 10px;"
                            dense
                            outlined
                            v-model="editedItem.spindle_inner"
                          ></v-select>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-select
                            :items="spindle_rpm_array"
                            label="最高轉速(rpm)"
                            style="position:relative; top: 10px;"
                            dense
                            outlined
                            v-model="editedItem.spindle_rpm"
                          ></v-select>
                        </v-col>
                      </v-row>
                      <!-- 第3列-->
                      <v-row>
                        <v-col cols="12" md="4">
                          <v-select
                            :items = "spindle_motor_array"
                            label="馬達規格"
                            style="position:relative; top: 10px;"
                            dense
                            outlined
                            v-model="editedItem.spindle_motor"
                          ></v-select>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-select
                            :items = "spindle_S1Kw_array"
                            label="馬達功率 S1(Kw)"
                            style="position:relative; top: 10px;"
                            dense
                            outlined
                            v-model="editedItem.spindle_kw"
                          ></v-select>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-select
                            :items = "spindle_S1Nm_array"
                            label="馬達扭力 S1(Nm)"
                            style="position:relative; top: 10px;"
                            dense
                            outlined
                            v-model="editedItem.spindle_nm"
                          ></v-select>
                        </v-col>
                      </v-row>
                      <!-- 第4列-->
                      <v-row>
                        <v-col cols="12" md="2">
                          <v-subheader style="margin-bottom: 0; height: 15px; font-size: 15px;">
                            <span>潤滑方式</span>
                          </v-subheader>
                          <v-radio-group v-model="editedItem.spindle_lubrication" hide-details column style="margin-top: 0; position: relative; left: 15px;">
                            <v-radio value="1" label="油氣潤滑"></v-radio>
                            <v-radio value="2" label="油脂潤滑"></v-radio>
                          </v-radio-group>
                        </v-col>
                        <v-col cols="12" md="6">
                          <v-subheader style="margin-bottom: 0; height: 15px; font-size: 15px;">
                            <span>冷卻方式</span>
                          </v-subheader>
                          <v-radio-group v-model="editedItem.spindle_cooling" hide-details row style="margin-top: 0; position: relative; left: 15px;">
                            <v-radio value="1" label="水冷" color="green"></v-radio>
                            <v-radio value="2" label="油冷" color="green"></v-radio>
                            <v-radio value="3" label="水冷/油冷" color="green"></v-radio>
                            <v-radio value="0" label="N/A" color="green"></v-radio>
                         </v-radio-group>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-select
                            :items="spindle_handles_array"
                            label="刀把介面"
                            style="position:relative; top: 10px;"
                            dense
                            outlined
                            v-model="editedItem.spindle_handle"
                          ></v-select>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">取消</v-btn>
                    <v-btn color="blue darken-1" text @click="save" :disabled='checkDataForSaveButton'>確定</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>

              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5">確定刪除這筆資料?</v-card-title>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="closeDelete">取消</v-btn>
                    <!--<v-btn color="blue darken-1" text @click="deleteItemConfirm">刪除</v-btn>-->
                    <v-btn color="blue darken-1" text @click="removeSpindle">刪除</v-btn>
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
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)" style="color: blue;">
              mdi-pencil
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
            <v-toolbar
              color="primary"
              dark
            >錯誤訊息!</v-toolbar>
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
import ListSpindles from '../../mixin/notification.js'

import { _createCSSWithConstants } from '../../mixin/constant.js';
import { _thetaSpindleTypes } from '../../mixin/constant.js';
import { _thetaSpindleOuters } from '../../mixin/constant.js';
import { _thetaSpindleMotorType } from '../../mixin/constant.js';
import { _thetaHandles } from '../../mixin/constant.js';
import { _thetaSpindleS1Kw } from '../../mixin/constant.js';
import { _thetaSpindleS1Nm } from '../../mixin/constant.js';


export default {
  name: 'Spindle',

  mixins: [Common, Notification, ListSpindles],

  mounted() {
    // if back button is pressed
    window.onpopstate = () => {
      console.log("press back button, good bye...");

      const userData = JSON.parse(localStorage.getItem('loginedUser'));
      userData.setting_items_per_page = this.pagination.itemsPerPage;
      localStorage.setItem('loginedUser', JSON.stringify(userData));
    };
  },

  data: () => ({
    currentUser: { },
    permDialog: false,
    rightDialog: false,
    /*
    snackbar: false,
    snackbar_color: 'success',
    snackbar_right: true,
    snackbar_top: true,
    snackbar_info: '',
    snackbar_icon_color: '#adadad',
    */
    dialog: false,
    dialogDelete: false,

    pagination: {
      //itemsPerPage: 10,   //預設值, rows/per page
      //page: 1,
    },

    //tosterOK: false,
    //toster_pos_x: 1000,
    //toster_pos_y: 400,
    //toster_delay:3,

	  //IDErrMsg: '',
    //nameErrMsg: '',
    //scaleErrMsg: '',
    //stockErrMsg: '',
    //firstEdit: true,

    //資料表頭
    headers: [
      { text: '產品類別', sortable: true, value: 'spindle_type', width: '15%' },
      { text: '型號', sortable: true, value: 'spindle_cat', width: '10%' },
      { text: '主軸外徑(mm)', sortable: false, value: 'spindle_outer', width: '5%' },
      { text: '軸承內徑(mm)', sortable: false, value: 'spindle_inner', width: '5%' },
      { text: '最高轉速(rpm)', sortable: false, value: 'spindle_rpm', width: '5%' },
      { text: '馬達', sortable: false, value: 'spindle_motor', width: '12%' },
      { text: '馬達功率S1(kW)', sortable: false, value: 'spindle_kw', width: '6%' },
      { text: '馬達扭力S1(Nm)', sortable: false, value: 'spindle_nm', width: '6%' },
      { text: '軸承潤滑', sortable: false, value: 'spindle_lubrication', width: '7%' },
      { text: '主軸冷卻', sortable: false, value: 'spindle_cooling', width: '8%' },
      { text: '刀把介面', sortable: false, value: 'spindle_handle', width: '15%' },
      { text: 'Actions', sortable: false, value: 'actions', width: '6%' },
    ],

    desserts: [],
    temp_desserts: [],

    //suppliers: [],
    //temp_suppliers: [],

    //products: [],         //slide-item的主要產品資料
    //temp_products: [],
    //products_for_spindleType: [],

    //temp_departments: [],

    //product_item: '',
    //selectProduct: false,

    editedIndex: -1,
    editedItem: {
      id: 0,
      spindle_type: '1',
      spindle_cat: '',
      spindle_outer: '',
      spindle_inner: '',
      spindle_lubrication: '1',
      spindle_rpm: '',
      spindle_motor: '',
      spindle_kw: '',
      spindle_nm: '',
      spindle_cooling: '1',
      spindle_handle: '',
    },
    defaultItem: {
      id: 0,
      spindle_type: '1',
      spindle_cat: '',
      spindle_outer: '',
      spindle_inner: '',
      spindle_lubrication: '1',
      spindle_rpm: '',
      spindle_motor: '',
      spindle_kw: '',
      spindle_nm: '',
      spindle_cooling: '1',
      spindle_handle: '',
    },

    //newItem: '',
    reagents: [],

    load_SingleTable_ok: false,

    spindle_cat_array: [],
    spindle_inner_array: [],
    spindle_rpm_array: [],

    spindle_lubrication: '1',
    spindle_cooling: '1',
    spindle_outer_array: [],
    spindle_motor_array: [],
    spindle_S1Kw_array: [],
    spindle_S1Nm_array: [],
    spindle_handles_array: [],
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? '新增資料' : '編輯資料'
    },

    checkDataForSaveButton() {
      if (!!this.editedItem.spindle_type && !!this.editedItem.spindle_cat &&
          !!this.editedItem.spindle_outer && !!this.editedItem.spindle_inner && !!this.editedItem.spindle_rpm &&
           !!this.editedItem.spindle_motor && !!this.editedItem.spindle_kw && !!this.editedItem.spindle_nm &&
          !!this.editedItem.spindle_lubrication && !!this.editedItem.spindle_cooling && !!this.editedItem.spindle_handle) {
        return false;
      } else {
        return true
      }
    },
  },

  watch: {
    dialog (val) {
      //!val || this.fieldFocus();
      val || this.close();
    },

    dialogDelete (val) {
      val || this.closeDelete()
    },
    /*
    load_5thTable_ok(val) {
      if (val) {
        this.reagents = Object.assign([], this.temp_departments);
        let temp_reagents = this.reagents.map(function(p) {  //
          return p.dep_name;
        });
        this.reagents = [...new Set(temp_reagents)];  //去除重複項目

        this.load_5thTable_ok=false;
        this.listReagents();
      }
    },


    load_4thTable_ok(val) {
      if (val) {
        this.suppliers = Object.assign([], this.temp_suppliers);
        //this.editedItem.reag_product=this.product_item;
        //this.editedItem.reag_supplier=this.product_item;
        this.selectProduct=false
        this.load_4thTable_ok=false;
      }
    },


    load_3thTable_ok(val) {
      if (val) {
        this.products = Object.assign([], this.temp_products);
        this.load_3thTable_ok=false;
      }
    },


    load_2thTable_ok(val) {
      if (val) {
        this.suppliers = Object.assign([], this.temp_suppliers);
        console.log("this.suppliers: ", this.suppliers)
        this.load_2thTable_ok=false;
        this.listProducts();
      }
    },
    */
    load_SingleTable_ok(val) {
      if (val) {
        this.desserts = Object.assign([], this.temp_desserts);

        this.listDotEnv();

        this.load_SingleTable_ok=false;
      }
    }
  },

  created () {
    //_createCSSWithConstants();

    this.products_for_spindleType = Object.assign([], _thetaSpindleTypes);

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
      this.listSpindles();    // 20230406  modify
    },

    listDotEnv() {
      console.log("listDotEnv()...")

      const path = '/listDotEnv';
      axios.get(path)
      .then((res) => {
        this.spindle_cat_array=[...res.data.spindle_cat1, ...res.data.spindle_cat2, ...res.data.spindle_cat3];
        this.spindle_outer_array=[...res.data.spindle_outer1, ...res.data.spindle_outer2];
        this.spindle_inner_array=[...res.data.spindle_inner1, ...res.data.spindle_inner2];
        this.spindle_rpm_array=[...res.data.spindle_rpm1, ...res.data.spindle_rpm2];
        this.spindle_motor_array=[...res.data.spindle_motor1, ...res.data.spindle_motor2];
        this.spindle_S1Kw_array=[...res.data.spindle_S1Kw1, ...res.data.spindle_S1Kw2];
        this.spindle_S1Nm_array=[...res.data.spindle_S1Nm1, ...res.data.spindle_S1Nm2];
        this.spindle_handles_array=[...res.data.spindle_handles1, ...res.data.spindle_handles2, ...res.data.spindle_handles3, ...res.data.spindle_handles4, ...res.data.spindle_handles5];
        //console.log("GET ok, value: ", res.data.spindle_outer);
      })
      .catch((error) => {
        console.error(error);
        this.showTosterForError('錯誤! API連線問題...')
      });
    },

    listSpindles() {
      console.log("listSpindles()...")

      const path = '/listSpindles';
      this.load_SingleTable_ok=false;
      axios.get(path)
      .then((res) => {
        this.temp_desserts = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_SingleTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.showTosterForError('錯誤! API連線問題...');
      });
    },
    /*
    fieldFocus() {
        this.tosterOK=false;
        this.IDErrMsg='';
        this.nameErrMsg='';
        this.scaleErrMsg='';
        this.stockErrMsg = '';
        this.selectProductErrMsg='';
    },

    fieldCheck() {
      console.log("fieldCheck...")

      if (this.editedItem.reag_product=="") {
        //this.selectProduct=true;
        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= '請先選擇資材類別!';
        this.snackbar_icon_color= '#adadad';
      }
    },
    */
    editItem(item) {
      console.log("editItem (), ", item)

      if (this.currentUser.perm >2) {
        this.rightDialog = true;
        return;
      }

      this.editedIndex = this.desserts.indexOf(item)
      let tmp_item = Object.assign({}, item)

      let t1 = item.spindle_type.trim();
      let t2 = item.spindle_cooling.trim();
      let t3 = item.spindle_lubrication.trim();
      let t4 = item.spindle_motor.trim();
      tmp_item.spindle_type = (t1 == '銑削/研磨主軸(自動換刀)') ? "1" : (t1 == '研磨主軸(手動換刀)') ? "2" : (t1 == '修砂主軸(手動換刀)') ? "3" : "0";
      tmp_item.spindle_cooling = (t2 == '水冷/油冷') ? "3" : (t1 == '油冷') ? "2" : (t1 == '水冷') ? "1" : "0";
      tmp_item.spindle_lubrication = (t3 == '油氣潤滑') ? "1" : "2";
      tmp_item.spindle_motor = (t4 == '') ? "空白" : t4;
      this.spindle_cat_array.push(tmp_item.spindle_cat);
      this.spindle_outer_array.push(tmp_item.spindle_outer);
      this.spindle_inner_array.push(tmp_item.spindle_inner);
      this.spindle_rpm_array.push(tmp_item.spindle_rpm);
      this.spindle_motor_array.push(tmp_item.spindle_motor);
      this.spindle_S1Kw_array.push(tmp_item.spindle_kw);
      this.spindle_S1Nm_array.push(tmp_item.spindle_nm);
      this.spindle_handles_array.push(tmp_item.spindle_handle);

      this.spindle_motor_array.push(tmp_item.spindle_motor);
      this.spindle_cat_array = [...new Set(this.spindle_cat_array)];  //去除重複項目
      this.spindle_outer_array = [...new Set(this.spindle_outer_array)];
      this.spindle_inner_array = [...new Set(this.spindle_inner_array)];
      this.spindle_rpm_array = [...new Set(this.spindle_rpm_array)];
      this.spindle_S1Kw_array = [...new Set(this.spindle_S1Kw_array)];
      this.spindle_S1Nm_array = [...new Set(this.spindle_S1Nm_array)];
      this.spindle_handles_array = [...new Set(this.spindle_handles_array)];

      this.editedItem = Object.assign({}, tmp_item)
      console.log("editedIndex, item, tmp_item, editedItem: ",this.editedIndex,  item, tmp_item, this.editedItem);

      this.dialog = true;
    },

    deleteItem (item) {
      console.log("deleteItem(), ", item);

      if (this.currentUser.perm >2) {
        this.rightDialog = true;
        return;
      }

      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },
    /*
    deleteItemConfirm() {
      this.removeSpindle();

      //if (!this.tosterOK) {
        this.desserts.splice(this.editedIndex, 1)
        console.log("deleteItem: ", this.editedItem);

        this.closeDelete()
      //}
    },
    */
    close() {
      console.log("close()...");

      this.dialog = false
      //this.IDErrMsg='';
      //this.nameErrMsg='';
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    closeDelete() {
      console.log("closeDelete()...");

      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    removeSpindle() {
      console.log("removeSpindle()...");

      const path='/removeSpindle';
      let payload = Object.assign({}, this.editedItem);
      axios.post(path, payload)
      .then(res => {
        console.log("remove spindle status: ", res.data.status);
        if (res.data.status) {
          this.editedItem = Object.assign({}, this.defaultItem); //清空 editedItem

          this.desserts.splice(this.editedIndex, 1);

          this.closeDelete();
        } else {
          this.showTosterForError(res.data.message);
        }
      })
      .catch(err => {
        console.error(err)
        this.showTosterForError('錯誤! API連線問題...')
      });
    },

    save() {
      console.log("save(), ", this.editedIndex);

      let tmp_str2 = (this.editedItem.spindle_type === '1') ? "銑削/研磨主軸(自動換刀)" : (this.editedItem.spindle_type === '2') ? "研磨主軸(手動換刀)" : (this.editedItem.spindlegrid_type === '3') ? "修砂主軸(手動換刀)" : "";
      //let exists = this.desserts.some(obj => obj.spindle_type == tmp_str2 && obj.spindle_cat == this.editedItem.spindle_cat);

      //if (exists) {
      //  this.showTosterForError('錯誤! 資料重複!')
      //} else {
        let newArr = {}
        Object.assign(newArr, this.editedItem)
        newArr.spindle_motor=(newArr.spindle_motor=='空白')?'':newArr.spindle_motor;
        if (this.editedIndex == -1) {       //add
            this.createSpindle(newArr);
            //newArr.spindle_motor=(newArr.spindle_motor=='空白')?'':newArr.spindle_motor;
            this.desserts.push(newArr);
        } else {                            //edit
          this.updateSpindle(newArr);
          newArr.spindle_type=tmp_str2;
          Object.assign(this.desserts[this.editedIndex], newArr);
        }
      //}
      this.close();
    },

    updateSpindle(object) {  //編輯資料
      console.log("updateSpindle(), ", object);

      const path='/updateSpindle';
      let payload = Object.assign({}, object);
      axios.post(path, payload)
      .then(res => {
        console.log("updateSpindle status: ", res.data.status)
        if (res.data.status) {
          this.editedItem = Object.assign({}, this.defaultItem) //清空 editedItem
        } else {
          this.showTosterForError(res.data.status)
        }
      })
      .catch(err => {
        console.error(err);
        this.showTosterForError('錯誤! API連線問題...')
      });
    },

    createSpindle(object) {
      console.log("createSpindle(), ", object);

      const path='/createSpindle';
      let payload = Object.assign({}, object);
      axios.post(path, payload)
      .then(res => {
        console.log("save spindle data status: ", res.data.status)
        if (res.data.status) {
          this.editedItem = Object.assign({}, this.defaultItem) //清空 editedItem
        } else {
          let tmp_str2 = (this.editedItem.grid_type === '1') ? "銑削/研磨主軸(自動換刀)" : (this.editedItem.grid_type === '2') ? "研磨主軸(手動換刀)" : (this.editedItem.grid_type === '3') ? "修砂主軸(手動換刀)" : "";
          this.showTosterForError('錯誤! 沒有' + tmp_str2 + '/'+ this.editedItem.grid_cat + '主軸資料!')
        }
      })
      .catch(err => {
        console.error(err);
        this.showTosterForError('錯誤! API連線問題...')
      });
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
    /*
    resetQueue() {
      this.reag_catalog.selected_item = this.newItem;
      //this.editedItem.reag_catalog = this.reag_catalog.selected_item
      //let temp=this.reag_catalog.length;
      //this.reagents.splice(temp-2, 0, this.newItem);
      this.reagents.unshift(this.reag_catalog.selected_item);
    },

    resetQueueIn() {
      this.editedItem.reag_In_unit = this.newItemIn;
      //let temp=this.newItemIn.length;
      //this.InUnits.splice(temp-2, 0, this.newItem);
      this.InUnits.unshift(this.editedItem.reag_In_unit);
    },

    resetQueueOut() {
      this.editedItem.reag_Out_unit = this.newItemOut;
      //let temp=this.newItemIn.length;
      //this.InUnits.splice(temp-2, 0, this.newItem);
      this.OutUnits.unshift(this.editedItem.reag_Out_unit);
    },

    setRowStyleForRragent(item) {
      return 'style-for-data-table';
    },
    */
    permCloseFun() {
      console.log("press permission Close Button...");

      this.permDialog = false
      this.$router.push('/navbar');
    },

    rightCloseFun() {
      console.log("press permission Close Button...");

      this.rightDialog = false
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

::v-deep .v-data-table-header th:nth-last-child(1) span {
  color: #1f4788 !important;
}
::v-deep .v-data-table-header th:nth-last-child(11) span {
  color: #1f4788 !important;
}
::v-deep .v-data-table-header th:nth-last-child(12) span {
  color: #1f4788 !important;
}

small.msgErr {
  font-size: 80%;
  color: red;
  margin-top: -10px;
}

::v-deep .add_modalbox > .v-card {
    background: rgba(170, 209, 183, 0.37);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(4.8px);
    -webkit-backdrop-filter: blur(4.8px);
    border: 1px solid rgba(170, 209, 183, 1);
}

::v-deep .v-input-disable {
    background-color: #f0f0f0;
    color: gray;
}
</style>