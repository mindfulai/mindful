<template>
  <div>
    <header>
        <router-link class="left return" to="/index"><i class="fa fa-chevron-left"></i></router-link>
        sentiment
    </header>
    <div class="content">
      <!-- FaceBook -->
      <h4 class="content_header">FaceBook</h4>
      <div class="content_sentiment">
        <div class="content_sentiment_box" v-for="(item,index) in facebookData" :key="index">
          <p class="content_date">{{formatTime(new Date(item.created_at)).slice(0,-5)}}</p>
          <div class="content_inner">
            <p class="content_inner_p">{{item.content?item.content:""}}</p>
            <div class="score">score:<br><b>{{item.score.toFixed(2)}}</b></div>
          </div> 
          <!-- <div class="content_img">
            <div class="content_img_inner clearfix">
              <div class="img_part left"><img src="./../assets/user.png" alt=""></div>
              <div class="img_sentiment right">
                <div><p>happiness: <b>0.78</b></p><p>neutral: <b>0.01</b></p></div>
                <div><p>surprise : <b>0.08</b></p><p>disgust : <b>0.01</b></p></div>
                <div><p>contempt  : <b>0.01</b></p><p>anger   : <b>0.01</b></p></div>
                <div><p>sadness  : <b>0.01</b></p><p>fear    : <b>0.01</b></p></div>
              </div>
            </div>
          </div> -->
        </div>
      </div>
      <!-- Twitter -->
      <h4 class="content_header">Twitter</h4>
      <div class="content_sentiment">
        <div class="content_sentiment_box" v-for="(item,index) in twitterData" :key="index">
          <p class="content_date">{{formatTime(new Date(item.created_at)).slice(0,-5)}}</p>
          <div class="content_inner">
            <p class="content_inner_p">{{item.content?item.content:""}}</p>
            <div class="score">score:<br><b>{{item.score.toFixed(2)}}</b></div>
          </div> 
          <!-- <div class="content_img">
            <div class="content_img_inner clearfix">
              <div class="img_part left"><img src="./../assets/user.png" alt=""></div>
              <div class="img_sentiment right">
                <div><p>happiness: <b>0.78</b></p><p>neutral: <b>0.01</b></p></div>
                <div><p>surprise : <b>0.08</b></p><p>disgust : <b>0.01</b></p></div>
                <div><p>contempt  : <b>0.01</b></p><p>anger   : <b>0.01</b></p></div>
                <div><p>sadness  : <b>0.01</b></p><p>fear    : <b>0.01</b></p></div>
              </div>
            </div>
            <div class="content_img_inner clearfix">
              <div class="img_part left"><img src="./../assets/user.png" alt=""></div>
              <div class="img_sentiment right">
                <div><p>happiness: <b>0.78</b></p><p>neutral: <b>0.01</b></p></div>
                <div><p>surprise : <b>0.08</b></p><p>disgust : <b>0.01</b></p></div>
                <div><p>contempt  : <b>0.01</b></p><p>anger   : <b>0.01</b></p></div>
                <div><p>sadness  : <b>0.01</b></p><p>fear    : <b>0.01</b></p></div>
              </div>
            </div>
          </div> -->
        </div>
      </div>
      <!-- Mood -->
      <h4 class="content_header">Mood</h4>
      <div class="content_sentiment">
        <div class="content_sentiment_box" v-for="(item,index) in moodData" :key="index">
          <p class="content_date">{{formatTime(new Date(item.created_at)).slice(0,-5)}}</p>
          <div class="content_inner">
            <p class="content_inner_p">{{item.content?item.content:""}}</p>
            <div class="score">score:<br><b>{{item.score.toFixed(2)}}</b></div>
          </div> 
        </div>
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
      facebookData: [],
      twitterData: [],
      moodData: []
    };
  },
  mounted() {
    this.name = window.localStorage.getItem("name");
    this.id = window.localStorage.getItem("id");
    this.getFacebook();
    this.getTwitter();
    this.getMood();
  },
  methods: {
    getFacebook() {
      this.$axios
        .get(this.api + "/user/" + this.id + "/facebook/sentiment")
        .then(res => {
          if (res.status == 200) {
            this.facebookData = res.data;
          }
        });
    },
    getTwitter() {
      this.$axios
        .get(this.api + "/user/" + this.id + "/twitter/sentiment")
        .then(res => {
          if (res.status == 200) {
            this.twitterData = res.data;
          }
        });
    },
    getMood() {
      this.$axios
        .get(this.api + "/user/" + this.id + "/mood/sentiment")
        .then(res => {
          if (res.status == 200) {
            this.moodData = res.data;
          }
        });
    },
    //时间转换
    //日期带时区格式处理
    formatTime(date) {
      var year = date.getFullYear();
      var month = date.getMonth() + 1;
      var day = date.getDate();
      var hour = date.getHours();
      var minute = date.getMinutes();
      var second = date.getSeconds();
      return (
        [year, month, day].map(this.formatNumber).join("-") +
        " " +
        [hour, minute, second].map(this.formatNumber).join(":") +
        String(date).slice(
          String(date).indexOf("GMT") + 3,
          String(date).indexOf("GMT") + 8
        )
      );
    },
    //数字格式
    formatNumber(n) {
      n = n.toString();
      return n[1] ? n : "0" + n;
    }
  },
  components: {
    navHeader
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.return {
  position: absolute;
  height: 1.08rem;
  left: 0.3rem;
  color: #fff;
  font-size: 0.34rem;
}
.content_header {
  padding: 0.2rem;
  font-size: 0.32rem;
  background: #727983;
  color: #fff;
  border-top-left-radius: 0.1rem;
  border-top-right-radius: 0.1rem;
}

.content_sentiment {
  border-bottom-left-radius: 0.1rem;
  border-bottom-right-radius: 0.1rem;
  background: #fff;
  padding: 0 0.2rem;
  margin-bottom: 0.3rem;
}
.content_sentiment_box {
  border-bottom: 1px solid #e1e2e9;
  padding: 0.2rem 0 0;
}
.content_sentiment_box:last-of-type {
  border: none;
}
.content_date {
  padding: 0.1rem 0;
  font-size: 0.3rem;
  font-weight: 700;
}
.content_inner {
  position: relative;
  font-size: 0.3rem;
  padding: 0.1rem 0;
  margin-bottom: 0.1rem;
}
.content_inner_p {
  width: 80%;
  line-height: 0.6rem;
}
.score {
  text-align: center;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  right: 0.2rem;
}

.img_part {
  width: 1.5rem;
  height: 1.5rem;
  border: 1px solid #e1e2e9;
  border-radius: 0.1rem;
}
.img_part img {
  width: 100%;
}
.img_sentiment {
  padding: 0.1rem 0.3rem 0.1rem 0.4rem;
  width: 4.8rem;
  overflow: auto;
}
.img_sentiment div {
  width: 100%;
}
.img_sentiment p {
  float: left;
  font-size: 0.26rem;
  width: 50%;
}
</style>
