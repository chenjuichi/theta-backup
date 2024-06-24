import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    user_id: sessionStorage.getItem('user_id') || '00000000',
    sock_id: sessionStorage.getItem('sock_id') || '',
    local_ip: localStorage.getItem('local_ip') || '',
  },

  mutations: {
    updateUserID(state, user_id) {
      state.user_id = user_id;
      sessionStorage.setItem('user_id', user_id);  // Save to sessionStorage
    },
    updateSockID(state, sock_id) {
      state.sock_id = sock_id;
      sessionStorage.setItem('sock_id', sock_id);  // Save to sessionStorage
    },
    updateLocalIP(state, local_ip) {  // 添加 mutation
      state.local_ip = local_ip;
      localStorage.setItem('local_ip', local_ip);  // Save to localStorage
    },
    RESTORE_STATE(state) {
      const user_id = sessionStorage.getItem('user_id');
      const sock_id = sessionStorage.getItem('sock_id');
      const local_ip = localStorage.getItem('local_ip');
      if (user_id) {
        state.user_id = user_id;
      }
      if (sock_id) {
        state.sock_id = sock_id;
      }
      if (local_ip) {
        state.local_ip = local_ip;
      }
    },
    clearStorage(state) {
      state.user_id = '00000000';
      state.sock_id = '';
      state.local_ip = '';
      sessionStorage.setItem('user_id', '00000000');
      sessionStorage.setItem('sock_id', '');
      localStorage.setItem('local_ip', '');
    },
  },

  actions: {
    updateUserID({ commit }, user_id) {
      commit('updateUserID', user_id);
    },
    updateSockID({ commit }, sock_id) {
      commit('updateSockID', sock_id);
    },
    updateLocalIP({ commit }, local_ip) {
      commit('updateLocalIP', local_ip);
    },
    clearStorage({ commit }) {
      commit('clearStorage');
    },
  },

  getters: {
    user_id: state => state.user_id,
    sock_id: state => state.sock_id,
    local_ip: state => state.local_ip,  // 添加 getter
  },

  modules: {
  },

  strict: true
});

export default store;