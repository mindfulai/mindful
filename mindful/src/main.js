// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import axios from 'axios'
Vue.prototype.$axios = axios

//引入 mint-UI框架
import MintUI from 'mint-ui'
import 'mint-ui/lib/style.css'
Vue.use(MintUI)
//全局引入 facebook twitter 授权登录
// import hello from "hellojs/dist/hello.all";
// Vue.prototype.$hello = hello
//全局引入jquery
// import $ from 'jquery'
// Vue.prototype.$ = $

//全局引入echarts
import echarts from 'echarts'
Vue.prototype.$echarts = echarts

Vue.config.productionTip = false

import "@/assets/app.css"
Vue.prototype.api = ''
//Vue.prototype.api = "http://192.168.1.237:5000"
//Vue.prototype.api = 'https://mindful-ucb.herokuapp.com'
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
