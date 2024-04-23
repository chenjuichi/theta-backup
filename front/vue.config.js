const path = require('path')

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://192.168.32.50:6080',  // 後端 host and port

        changeOrigin: true, // needed for virtual hosted sites
        ws:true,            // proxy websockets
        pathRewrite: {
          '^/api': ''       // remove base path
        }
      },
    },
    host: '0.0.0.0',
    disableHostCheck: true,   //Keep getting [WDS] Disconnected! error
  },

};


