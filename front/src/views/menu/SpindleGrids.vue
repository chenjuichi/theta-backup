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
      <v-card width="75vw" class="pa-md-4  mt-5 mx-lg-auto">
        <v-data-table
          :headers="headers"
          :items="desserts"
          class="elevation-1"
          :options.sync="pagination"
          :footer-props="{ itemsPerPageText: '每頁的資料筆數' }"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>主軸跑合儲位</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="980px" content-class="add_modalbox">
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
                          <v-radio-group v-model="editedItem.grid_type" hide-details row style="margin-top: 0; position: relative; left: 15px;">
                            <v-radio value="1" label="銑削/研磨主軸(自動換刀)"></v-radio>
                            <v-radio value="2" label="研磨主軸(手動換刀)"></v-radio>
                            <v-radio value="3" label="修砂主軸(手動換刀)"></v-radio>
                          </v-radio-group>
                        </v-col>
                        <v-col cols="12" md="4">    <!-- 2023-04-14 modify md=3 => md=4   -->
                          <v-select
                            :items="items"
                            label="型號"
                            style="position:relative; top: 10px;"
                            dense
                            outlined
                            v-model="editedItem.grid_cat"
                          ></v-select>
                        </v-col>
                        <v-col class="d-flex" cols="12" md="4">
                        </v-col>
                      </v-row>
                      <!-- 第2列-->
                      <template>
                        <v-card>
                          <v-card-text>
                            儲位別
                            <v-row class="v-data-table-top-height">
                              <v-col cols="12" md="8">
                                <v-radio-group v-model="editedItem.grid_station" row :class="{'v-input-disable': formTitle === '編輯資料'}">
                                  <v-radio label="待跑合A區" color="red" value="1" style="margin-bottom: 0px;" />
                                  <v-radio label="待校正B區" color="red" value="2" style="margin-bottom: 0px;" />
                                  <v-radio label="待測試C區" color="red" value="3" style="margin-bottom: 0px;" />
                                  <v-radio label="異常處理D區" color="red" value="4" style="margin-bottom: 0px;" />
                                </v-radio-group>
                              </v-col>

                              <v-col cols="12" md="2" style="position: relative; left: -70px;">
                                <div style="color: #007bff; font-weight: 800;">層別</div>
                                <vue-numeric-input
                                  v-model="editedItem.grid_layout"
                                  :min="1"
                                  :max="99"
                                  :step="1"
                                  :readonly="formTitle === '編輯資料'"
                                  :class="{'v-input-disable': formTitle === '編輯資料'}"
                                ></vue-numeric-input>
                              </v-col>

                              <v-col cols="12" md="2" style="position: relative; left: -10px;"">
                                <v-text-field
                                  v-model="editedItem.grid_max_size"
                                  outlined
                                  label="最大數量"
                                  type="number"
                                  min=1
                                  max=5
                                  @keydown="handleKeyDown"
                                >
                                </v-text-field>
                              </v-col>
                            </v-row>
                          </v-card-text>
                        </v-card>
                      </template>
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
                    <v-btn color="blue darken-1" text @click="removeGrid">刪除</v-btn>
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
            <v-icon class="mr-2" @click="editItem(item)" style="color: blue;" size="16">
              mdi-pencil
            </v-icon>
            <v-icon @click="deleteItem(item)" style="color: red;" size="16">
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
import VueNumericInput from 'vue-numeric-input';
import Notification from '../../mixin/notification.js'

import Common from '../../mixin/common.js'
import Key from '../../mixin/key.js'

import { _thetaSpindleTypeAndID } from '../../mixin/constant.js';
import { _createCSSWithConstants } from '../../mixin/constant.js';
import { _thetaSpindleTypes } from '../../mixin/constant.js';

export default {
  name: 'SpindleGrids',

  mixins: [Common, Key, Notification],

  components: {
    VueNumericInput,
  },

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
    currentUser: {},

    items: [],
    temp_items: [],

    //temp_product: [],
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

    //disbtn: false,

    pagination: {
      //itemsPerPage: 10,   //預設值, rows/per page
      //page: 1,
    },

    tosterOK: false,
    toster_pos_x: 1000,
    toster_pos_y: 400,
    toster_delay:3,

    IDErrMsg: '',
    supNameErrMsg: '',
    supContactErrMsg: '',
    supPhoneErrMsg: '',
    supAddressErrMsg: '',

    //資料表頭
    headers: [
      //{ text: 'ID', value: 'id' },
      { text: '儲位別', sortable: true, value: 'grid_station' },
      { text: '層別', sortable: true, value: 'grid_layout' },
      { text: '類別 / 型號', sortable: true, value: 'grid_type_and_cat' },
      { text: '最大數量', sortable: false, value: 'grid_max_size' },
      { text: 'Actions', sortable: false, value: 'actions' },
    ],

    desserts: [],
    temp_desserts: [],

    editedIndex: -1,
    editedItem: {
      id: 0,
      //s_id: 0,
      grid_station: '1',
      grid_layout: 1,
      grid_type: '0',
      grid_cat: '',
      grid_max_size: '5',
    },
    defaultItem: {
      id: 0,
      //s_id: 0,
      grid_station: '1',
      grid_layout: 1,
      grid_type: '0',
      grid_cat: '',
      grid_max_size: '5',
    },

    load_SingleTable_ok: false,
    load_2thTable_ok: false,
    load_3thTable_ok: false,
    load_4thTable_ok: false,

    spindle_type: '1',
    spindle_cnt: 1,
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? '新增資料' : '編輯資料'
    },

    checkDataForSaveButton() {
      //if (!!this.editedItem.grid_station && !!this.editedItem.grid_layout && !!this.editedItem.grid_type &&
      //    !!this.editedItem.grid_max_size && this.editedItem.grid_cat.length >0) {
      if (!!this.editedItem.grid_station && !!this.editedItem.grid_layout) {
        return false;
      } else {
        return true
      }
    },

    filtered_spindle_cnt: {
      get() {
        console.log("this.editedItem.grid_max_size", this.editedItem.grid_max_size)
        return this.editedItem.grid_max_size;
      },

      set(value) {
        // 將輸入的值限制在1至5的範圍內
        const numValue = parseInt(value);
        console.log("this.editedItem.grid_max_size", numValue)
        if (!isNaN(numValue) && numValue >= 1 && numValue <= 5) {
          this.editedItem.grid_max_size = numValue;
          console.log("this.editedItem.grid_max_size", this.editedItem.grid_max_size)
        }
      },
    },
  },

  watch: {
    dialog(val) {
      //!val || this.fieldFocus();
      val || this.close();
    },

    dialogDelete(val) {
      val || this.closeDelete()
    },

    load_SingleTable_ok(val) {
      if (val) {
        this.listOrderFromProcess();
        this.load_SingleTable_ok=false;

        this.listSpindles();
      }
    },

    load_2thTable_ok(val) {
      if (val) {
        let i_len = this.temp_items.length;
        let temp_array=[]
        for (let i = 0; i < i_len; i++) {
          temp_array.push(this.temp_items[i].spindle_cat);
        }
        //console.log("temp_array ", temp_array)
        this.items = [...new Set(temp_array)];
        //this.items = Object.assign([], this.temp_items);
        this.load_2thTable_ok=false;
      }
    },

    load_3thTable_ok(val) {
      if (val) {
        Object.assign(this.desserts[this.editedIndex], this.editedItem)

        this.editedItem = Object.assign({}, this.defaultItem)

        this.close();

        this.load_3thTable_ok = false;
      }
    },
  },

  created() {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm == 0) {
      this.permDialog=true;
    }

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.temp_product = [..._thetaSpindleTypeAndID];

    this.initAxios();
    this.listGrids();
    //this.initialize()
  },

  methods: {
    initialize() {
      //this.load_SingleTable_ok=false;
      this.listGrids();
    },

    listGrids() {
      console.log("listGrids()...")

      const path = '/listGrids';
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

    listSpindles() {
      console.log("listSpindles()...")

      const path = '/listSpindles';
      this.load_2thTable_ok=false;
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
      console.log("listOrderFromProcess()...");

      let temp_array = [];
      let i_len = this.temp_desserts.length;
      //let j_len = 0;
      console.log("i_len:", i_len);
      for (let i = 0; i < i_len; i++) {
        let temp_obj = {
          "id": this.temp_desserts[i].id,
          //"s_id": this.temp_desserts[i].s_id,
          "grid_station": this.temp_desserts[i].station,
          "grid_layout": this.temp_desserts[i].layout,
          "grid_type_and_cat": this.temp_desserts[i].type_and_cat,
          "grid_max_size": this.temp_desserts[i].max_size,
        };

        temp_array.push(temp_obj);
      }

      this.desserts = Object.assign([], temp_array);
    },
    /*
    fieldFocus() {
      this.IDErrMsg = '';
      this.supNameErrMsg = '';
      this.supContactErrMsg = '';
      this.supPhoneErrMsg = '';
      this.supAddressErrMsg = '';
    },
    */
    editItem(item) {
      console.log("editItem(), ", item);

      if (this.currentUser.perm >2) {
        this.rightDialog = true;
        return;
      }

      this.editedIndex = this.desserts.indexOf(item)
      let tmp_item = Object.assign({}, item)

      tmp_item.grid_station = (item.grid_station == '待跑合A區') ? "1" : (item.editedItem.grid_station == '待校正B區') ? "2" : (item.editedItem.grid_station == '待校正C區') ? "3" : (item.editedItem.grid_station == '異常處理D區') ? "4" : "1";
      let tk=' / '
      let [t1, t2] = item.grid_type_and_cat.trim().split(tk);
      tmp_item.grid_type = (t1 == '銑削/研磨主軸(自動換刀)') ? "1" : (t1 == '研磨主軸(手動換刀)') ? "2" : (t1 == '修砂主軸(手動換刀)') ? "3" : "0";
      tmp_item.grid_cat = t2;

      this.editedItem = Object.assign({}, tmp_item)
      console.log("editItem, editedIndex, item, tmp_item, editedItem: ",this.editedIndex,  item, tmp_item, this.editedItem);

      this.dialog = true;
    },

    deleteItem(item) {
      console.log("deleteItem(), ", item);

      if (this.currentUser.perm >2) {
        this.rightDialog = true;
        return;
      }

      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    close() {
      console.log("close()...");

      this.dialog = false
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

    removeGrid() {
      console.log("removeGrid()...");

      const path='/removeGrid';
      let payload = Object.assign({}, this.editedItem);
      this.load_3thTable_ok=false;
      axios.post(path, payload)
      .then(res => {
        console.log("remove grid status: ", res.data.status);
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

    save() {
      console.log("save(), ", this.editedIndex);

      let tmp_str1 = (this.editedItem.grid_station === '1') ? "待跑合A區" : (this.editedItem.grid_station === '2') ? "待校正B區" : (this.editedItem.grid_station === '3') ? "待測試C區" : (this.editedItem.grid_station === '4') ? "異常處理D區" : "";
      let tmp_str2 = (this.editedItem.grid_type === '1') ? "銑削/研磨主軸(自動換刀)" : (this.editedItem.grid_type === '2') ? "研磨主軸(手動換刀)" : (this.editedItem.grid_type === '3') ? "修砂主軸(手動換刀)" : "";
      let newArr = {
        grid_station: tmp_str1,
        grid_layout: this.editedItem.grid_layout.toString(),
        grid_type_and_cat: tmp_str2 + ' / ' + this.editedItem.grid_cat,
        grid_max_size: this.editedItem.grid_max_size,
      };
      let exists = this.desserts.some(obj => obj.grid_station == newArr.grid_station && obj.grid_layout == newArr.grid_layout && obj.grid_type_and_cat == newArr.grid_type_and_cat);
      //console.log("比較: ", exists, this.editedIndex, newArr, this.desserts)

      if (exists) {
        this.showTosterForError('錯誤! 資料重複!')
      } else {
        if (this.editedIndex == -1) {       //add
            this.createGrid(this.editedItem);
            this.desserts.push(newArr);
        } else {                            //edit
          this.updateGrid(this.editedItem);
          Object.assign(this.desserts[this.editedIndex], newArr);
        }
      }
      this.close();
    },

    updateGrid(object) {  //編輯資料
      console.log("updateGrid(), ", object);

      const path='/updateGrid';
      let payload = Object.assign({}, object);
      this.load_3thTable_ok=false;
      axios.post(path, payload)
      .then(res => {
        console.log("updateGrid status: ", res.data.status)
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

    createGrid(object) {
      console.log("createGrid(), ", object);

      const path='/createGrid';
      let payload = Object.assign({}, object);
      axios.post(path, payload)
      .then(res => {
        console.log("save grid data status: ", res.data.status)
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
    permCloseFun () {
      this.permDialog = false
      console.log("press permission Close Button...");
      this.$router.push('/navbar');
    },

    rightCloseFun() {
      this.rightDialog = false
      console.log("press permission Close Button...");
      //this.$router.push('/navbar');
    },

    handleKeyDown(event) {
      console.log("handleKeyDown , 1", this.editedItem.grid_max_size)
      // 檢查按鍵是否為負號或超出範圍
      const numValue = parseInt(event.target.value + event.key);
      if (isNaN(numValue) || numValue < 1 || numValue > 5) {
        console.log("handleKeyDown , 2", this.editedItem.grid_max_size)
        // 阻止事件的預設行為，即不允許輸入
        event.preventDefault();
      }
    },
  },
}
</script>

<style lang="scss" scoped>
@import url('https://fonts.googleapis.com/css?family=Noto+Sans+TC:400,500&display=swap&subset=chinese-traditional'
);

div.v-toolbar__title {
  margin: 0;
  font-family: "Noto Sans TC", "Microsoft Yahei", "微軟雅黑", sans-serif;
}

::v-deep .v-data-table-header {
  background-color:var(--navbar-header-color);
}

::v-deep .v-data-table-header th {
  font-size: 1em !important;
}

::v-deep .v-data-table-header th:nth-last-child(1) {
  font-size: 0.8em !important;
}

small.msgErr {
  font-size: 80%;
  color: red;
  top: -20px;
  position: relative;
}

::v-deep .style-1 td {
  padding-left: 8px !important;
  padding-right: 0px !important;
}

::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  padding-left: 8px !important;
  padding-right: 0px !important;
  text-align: start !important;
}

::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th:nth-last-child(2) {
  text-align: center !important;
}

::v-deep .v-data-table-header th:nth-last-child(1) span {
  color: #1f4788 !important;
}

::v-deep .style-1 td:nth-last-child(2) > span {
  margin-left: 4px !important;
  margin-right: 0px !important;
  margin-top: 4px !important;
  margin-bottom: 4px !important;
  border-style: solid !important;
  border-color: coral !important;
}

::v-deep .style-1 td:nth-child(2) {
  font-size: 10px !important;
}
::v-deep .style-1 td:nth-child(4) {
  font-size: 10px !important;
}

/*
::v-deep .add_modalbox > .v-card {
    background: rgba(170, 209, 183, 0.37);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(4.8px);
    -webkit-backdrop-filter: blur(4.8px);
    border: 1px solid rgba(170, 209, 183, 1);
}

::v-deep div[role=combobox].v-input__slot {
    background: rgba(170, 209, 183, 0.37) !important;
}

::v-deep div[role=listbox].v-list.v-select-list {
  background: rgba(170, 209, 183, 1) !important;
}
*/

::v-deep .v-label {
  font-size: 1em;
}
::v-deep .v-label--active {
  font-size: 1.2em;
  font-weight: 800;
  color: #007bff;
}

::v-deep .v-input-disable {
    background-color: #f0f0f0;
    color: gray;
}

::v-deep .v-data-table-top-height {
  position:relative;
  //height: 90px;
  top: 10px;
}
</style>