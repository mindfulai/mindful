<template>
  <div>
    <nav-header :name="name"></nav-header>
    <div class="content">
  <h3 class="connect_authorize">CONNECT AUTHORIZE</h3>
  <div class="authorize_box">
    <div class="authorize_meta">
      Twitter &nbsp;&nbsp;<i class="fa fa-twitter twitter_logo"></i>
    </div>
    <ul>
      <li><a href="#">TRACKS</a><strong>Tweets,metions</strong></li>
      <li><a href="#">REQUIRES</a><strong>Twitter account</strong></li>
      <li><a href="#">PROVIDING</a><strong>Tweets</strong></li>
    </ul>
    <!-- https://pocoweb-mindful.herokuapp.com -->
    <a  v-if="!twitter_auth" class="authorize_connect" href="/twitter/authorize">
      <i class="fa fa-plus"></i>&nbsp;
      Authorize
    </a>
    <a v-if="twitter_auth" class="authorize_connect">
      Authorized
    </a>
    <!-- <div class="authorize_connect"  @click="connect('twitter')">
      <i class="fa fa-plus"></i>&nbsp;
      Connect
    </div> -->
  </div>
  <div class="authorize_box">
    <div class="authorize_meta facebook">
      facebook <!--<i class="fa fa-facebook"></i>-->
    </div>
    <ul>
      <li><a href="#">TRACKS</a><strong>Posts, comments, reactions</strong></li>
      <li><a href="#">REQUIRES</a><strong>Facebook account</strong></li>
      <li><a href="#">PROVIDING</a><strong>Facebook posts</strong></li>
    </ul>
    <a  v-if="!facebook_auth" class="authorize_connect">
      <i class="fa fa-plus"></i>&nbsp;
      Authorize
    </a>
    <a v-if="facebook_auth" class="authorize_connect">
      Authorized
    </a>
  </div>
</div>
  </div>
</template>

<script>
import navHeader from "@/components/header";
export default {
  name: "index",
  data() {
    return {
      name: "",
      id: "",
      facebook_auth: false,
      twitter_auth: false
    };
  },
  mounted() {
    this.name = window.localStorage.getItem("name");
    this.id = window.localStorage.getItem("id");
    this.getAuthorize();
  },
  // mounted() {
  //   this.$hello.init({
  //     twitter: "devnDViKMhTY4J5AwVKW7NewW"
  //   });
  // },
  methods: {
    getAuthorize() {
      this.$axios
        .get(this.api + "/user/" + this.id + "/authorized")
        .then(res => {
          if (res.status == 200) {
            this.facebook_auth = res.data.facebook_auth;
            this.twitter_auth = res.data.twitter_auth;
          }
        });
    }
  },
  components: {
    navHeader
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
