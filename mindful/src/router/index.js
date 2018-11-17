import Vue from 'vue'
import Router from 'vue-router'
import login from '@/components/login'
import index from '@/components/index'
import authorize from '@/components/authorize'
import edit_mood from '@/components/edit_mood'

Vue.use(Router)

export default new Router({
  routes: [
    // {
    //   path: '/',
    //   name: 'index',
    //   component: index
    // },
    {
      path: '/',
      name: "login",
      component: login
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/index',
      name: 'index',
      component: index
    },
    {
      path: '/authorize',
      name: 'authorize',
      component: authorize
    },
    {
      path: '/edit_mood',
      name: 'edit_mood',
      component: edit_mood
    },
  ]
})
