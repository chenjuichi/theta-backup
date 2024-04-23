
import axios from 'axios'

export default {
    data: function () {
      return {
        snackbar: false,
        snackbar_color: 'success',
        snackbar_right: true,
        snackbar_top: true,
        snackbar_info: '',
        snackbar_icon_color: '#adadad',
      }
    },

    methods: {
      showTosterForError(msg) {
        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= msg;
        this.snackbar_icon_color= '#adadad';
      },

      showTosterForOK(msg) {
        this.snackbar_color='#008184';
        this.snackbar=true;
        this.snackbar_info= msg;
        this.snackbar_icon_color= "#ffffff";
      },
    }
}

