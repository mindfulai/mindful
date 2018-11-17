<template>
    <div class="login_box">
      <div class="login_header">Login</div>
      <!-- <fb:login-button class="login" scope="public_profile,email,user_posts"   onlogin="checkLoginState()"></fb:login-button> -->
      <!-- <a class="login" @click="login('facebook',{scope:'user_posts,email'})"> Login with Facebook<a class="facebook_logo"><i class="fa fa-facebook-square"></i></a>  -->
      <!-- https://pocoweb-mindful.herokuapp.com -->
      <a class="login" href="/login/facebook"> Login with Facebook<a class="facebook_logo"><i class="fa fa-facebook-square"></i></a> 
      </a>
    </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  // mounted() {
  //   this.$hello.init({
  //     facebook: "176320989922581",
  //     twitter: ""
  //   });
  // },
  methods: {
    // login(network, options) {
    //   var that = this;
    //   var provider = this.$hello(network);
    //   provider.login(options).then(
    //     res => {
    //       //授权 facebook 登录后发送信息给后端
    //       console.log(res);
    //       // that.$axios
    //       //   .get(that.api + "/debug", {
    //       //     params: { access_token: res.authResponse.access_token }
    //       //   })
    //       //   .then(res => {
    //       //     console.log(res);
    //       //   });
    //       provider.api("me", "get").then(res => {
    //         console.log(res);
    //       });
    //       // provider.api("me/share", "get").then(res => {
    //       //   console.log(res);
    //       // });
    //       // this.$router.push({
    //       //   path: "/index"
    //       // });
    //     },
    //     e => {
    //       console.log(e);
    //     }
    //   );
    // }
    // goHome() {
    //   this.$axios
    //     .get(this.api + "/login/facebook")
    //     .then(res => {
    //       alert(res);
    //       if (res.status == 200) {
    //       }
    //     })
    //     .catch(res => {
    //       console.log(res);
    //     });
    // },
    // checkLoginState() {
    //   FB.getLoginStatus(function(response) {
    //     console.log(response);
    //     this.statusChangeCallback(response);
    //   });
    // },
    // statusChangeCallback(response) {
    //   if (response.status === "connected") {
    //     //登陆状态已连接
    //     fbToken = response.authResponse.accessToken;
    //     this.getUserInfo();
    //   } else if (response.status === "not_authorized") {
    //     //未经授权
    //     console.log("facebook未经授权");
    //   } else {
    //     console.log("不是登陆到Facebook;不知道是否授权");
    //   }
    // },
    // getUserInfo() {
    //   FB.api("/me", function(response) {
    //     //response.id / response.name
    //     console.log("Successful login for: " + response.name);
    //     //把用户token信息交给后台
    //     self.location = "/home/login.fbLogin.do?accessToken=" + fbToken;
    //   });
    // }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.login_box {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  background: #333a45;
  /* background: #4e7ca0; */
}
.login_header {
  position: absolute;
  top: 35%;
  left: 0;
  text-align: center;
  font-size: 0.5rem;
  color: #fff;
  width: 100%;
}
.login {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 0.4rem;
  width: 80%;
  text-align: center;
  height: 1rem;
  line-height: 1rem;
  /* background: #95b0c6; */
  background: rgba(255, 255, 255, 0.4);
  color: #fff;
  border-radius: 0.2rem;
  z-index: 100;
}
.facebook_logo {
  float: right;
  margin-right: 0.4rem;
}
i {
  font-size: 0.5rem;
  color: #fff;
}
</style>
