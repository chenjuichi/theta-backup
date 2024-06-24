import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
//import '@mdi/font/css/materialdesignicons.css'
import '@mdi/font/css/materialdesignicons.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import '@fortawesome/fontawesome-free/css/all.css';
import '@fortawesome/fontawesome-free/js/all.js';

Vue.use(Vuetify, {
  icons: {
    //iconfont: 'mdi'
    iconfont: 'mdi' || 'md' || 'fa',
  },
})

Vue.config.productionTip = false
Vue.config.devtools = true;
/*
const savedState = sessionStorage.getItem('store');
//if (savedState) {
//  store.replaceState(Object.assign(store.state, JSON.parse(savedState)));
//}
if (savedState) {
//  store.commit('RESTORE_STATE', JSON.parse(savedState));
//}
  console.log('Restoring Vuex state from sessionStorage:', JSON.parse(savedState));
  store.commit('RESTORE_STATE', JSON.parse(savedState));
} else {
  console.log('No saved Vuex state found in sessionStorage.');
}
*/
//store.commit('RESTORE_STATE');
// 初始化 localStorage and sessionStorage
if (!sessionStorage.getItem('user_id')) {
  sessionStorage.setItem('user_id', '00000000');
}
if (!sessionStorage.getItem('sock_id')) {
  sessionStorage.setItem('sock_id', '');
}
if (!localStorage.getItem('local_ip')) {
  localStorage.setItem('local_ip', '');
}

new Vue({
  vuetify: new Vuetify(),
  router,
  store,
  render: h => h(App)
}).$mount('#app')
