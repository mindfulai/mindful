<template>
    <header>
        <router-link class="left setting" to="/index"><i class="fa fa-th-large"></i></router-link>

        <div class="right">
            <!--<a class="search"><i class="fa fa-search"></i></a>-->
            <a class="login" @click="showBar">{{name}}</a>
        </div>
        
        <div class="mine_bar" v-show="isShow">
            <ul class="mine_bar_list">
                <li><router-link to="/authorize"><i class="fa fa-tasks"></i>&nbsp;&nbsp;&nbsp;Authorize</router-link></li>
                <li><a @click="logout"><i class="fa fa-sign-out"></i>&nbsp;&nbsp;&nbsp;Log out</a></li>
            </ul>
        </div>
    </header>
</template>

<script>
export default {
  data() {
    return {
      isShow: false
    };
  },
  props: ["name"],
  methods: {
    showBar() {
      this.isShow = !this.isShow;
    },
    logout() {
      //退出应用清空本地存储
      window.localStorage.removeItem("name");
      window.localStorage.removeItem("id");
      this.$router.push({
        path: "login"
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
