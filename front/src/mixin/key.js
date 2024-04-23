
export default {
    data: function () {
      return {

      }
    },

    methods: {
      handleKeyDown(event) {
        // 檢查按鍵是否為負號或超出範圍
        const numValue = parseInt(event.target.value + event.key);
        if (isNaN(numValue)) {
          console.log("handleKeyDown... Not number!")
          // 阻止事件的預設行為，即不允許輸入
          event.preventDefault();
        }
      },
    }
}

