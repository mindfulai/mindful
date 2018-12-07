<template>
  <div>
    <header>
        <router-link class="left return" to="/index"><i class="fa fa-chevron-left"></i></router-link>
        sentiment
    </header>
    <div class="content">
      <h4 class="content_header">FaceBook</h4>
      <div class="content_sentiment">
        <div class="content_sentiment_box">
          <p class="content_date">2018-12-06 08:34:23</p>
          <div class="content_inner">
            <p class="content_inner_p">北京天气很好，心情也不错！北京天气很好，心情也不错！北京天气很好，心情也不错！北京天气很好，心情也不错！北京天气很好，心情也不错！</p>
            <div class="score">score:<br><b>0.90</b></div>
          </div> 
          <div class="content_img">
            <div class="content_img_inner clearfix">
              <div class="img_part left"><img src="./../assets/user.png" alt=""></div>
              <div class="img_sentiment right">
                <div><p>happiness: <b>0.78</b></p><p>neutral: <b>0.01</b></p></div>
                <div><p>surprise : <b>0.08</b></p><p>disgust : <b>0.01</b></p></div>
                <div><p>contempt  : <b>0.01</b></p><p>anger   : <b>0.01</b></p></div>
                <div><p>sadness  : <b>0.01</b></p><p>fear    : <b>0.01</b></p></div>
              </div>
            </div>
          </div>
        </div>
        <div class="content_sentiment_box">
          <p class="content_date">2018-12-06 08:34:23</p>
          <div class="content_inner">
            <p class="content_inner_p">北京天气很好，心情也不错！</p>
            <div class="score">score:<br><b>0.90</b></div>
          </div> 
          <div class="content_sentiment_img">
            
          </div>
        </div>
        <div class="content_sentiment_box">
          <p class="content_date">2018-12-06 08:34:23</p>
          <!-- <div class="content_inner">
            <p class="content_inner_p">北京天气很好，心情也不错！</p>
            <div class="score">score:<br><b>0.90</b></div>
          </div>  -->
          <div class="content_img">
            <div class="content_img_inner clearfix">
              <div class="img_part left"><img src="./../assets/user.png" alt=""></div>
              <div class="img_sentiment right">
                <div><p>happiness: <b>0.78</b></p><p>neutral: <b>0.01</b></p></div>
                <div><p>surprise : <b>0.08</b></p><p>disgust : <b>0.01</b></p></div>
                <div><p>contempt  : <b>0.01</b></p><p>anger   : <b>0.01</b></p></div>
                <div><p>sadness  : <b>0.01</b></p><p>fear    : <b>0.01</b></p></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <h4 class="content_header">Twitter</h4>
      <div class="content_sentiment">
        <div class="content_sentiment_box">
          <p class="content_date">2018-12-06 08:34:23</p>
          <div class="content_inner">
            <p class="content_inner_p">北京天气很好，心情也不错！</p>
            <div class="score">score:<br><b>0.90</b></div>
          </div> 
          <div class="content_img">
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
          </div>
        </div>
        <div class="content_sentiment_box">
          <p class="content_date">2018-12-06 08:34:23</p>
          <div class="content_inner">
            <p class="content_inner_p">北京天气很好，心情也不错！</p>
            <div class="score">score:<br><b>0.90</b></div>
          </div> 
          <div class="content_sentiment_img">
            
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
      id: ""
    };
  },
  mounted() {
    this.name = window.localStorage.getItem("name");
    this.id = window.localStorage.getItem("id");
  },
  methods: {},
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
  padding: 0.2rem 0;
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
  margin-bottom: 0.2rem;
}
.content_inner_p {
  width: 80%;
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
