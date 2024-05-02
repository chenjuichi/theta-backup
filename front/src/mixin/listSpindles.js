import axios from 'axios';
import aa from './notification';

export default {
    data: function () {
      return {
        listSpindles_isOK: false,
        listSpindles_outputs: [],
      }
    },

    methods: {
      listSpindles() {
        console.log("listSpindles()...")

        const path = '/listSpindles';
        this.listSpindles_isOK = false;
        axios.get(path)
        .then((res) => {
          this.listSpindles_outputs = res.data.outputs;
          console.log("GET ok, total records:", res.data.outputs.length);
          this.listSpindles_isOK = true;
        })
        .catch((error) => {
          console.error(error);
          aa.methods.showTosterForError.call(this, '錯誤! API連線問題...');
        });
      },
    }
}

