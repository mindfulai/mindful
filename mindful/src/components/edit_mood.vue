<template>
  <div>
    <nav-header :name='name'></nav-header>
    <div class="content">
      <div class="content_box">
        <h4>{{date}}</h4>

        <div class="content_box_inner">
          <div class="basic">
            <b>Mood:</b>
            <ul class="mood_rate clearfix" id="mood_select">
              <li class="mood-1" @click="selected($event,1)">1</li>
              <li class="mood-2" @click="selected($event,2)">2</li>
              <li class="mood-3" @click="selected($event,3)">3</li>
              <li class="mood-4" @click="selected($event,4)">4</li>
              <li class="mood-5" @click="selected($event,5)">5</li>
              <!-- <li><a class="mood-1" @click="selected($event,1)">1</a></li>
              <li><a class="mood-2" @click="selected($event,2)">2</a></li>
              <li><a class="mood-3" @click="selected($event,3)">3</a></li>
              <li><a class="mood-4" @click="selected($event,4)">4</a></li>
              <li><a class="mood-5" @click="selected($event,5)">5</a></li> -->
            </ul>
            <div class="form-group">
              <b>Note:</b>
              <textarea rows="4" name="note" maxlength="240" class="form-control" v-model="note"></textarea>
            </div>
            <!-- <div class="form-group">
              <b>Custom tags:</b>
              <div class="clearfix taggle_holder">
                <input class="taggle_placeholder" style="opacity: 1;" placeholder="Enter tags...">
              </div>
              <div class="help-block">
                Use a comma (,) to separate tags
              </div>
            </div> -->
            <p>
              <button type="submit" name="submit" class="save" @click="save"><i class="fa fa-check"></i> Save
              </button>
              or <a class="cancel" @click="cancel">Cancel</a>
            </p>
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
      date: "",
      score: "",
      note: ""
    };
  },
  mounted() {
    this.name = window.localStorage.getItem("name");
    this.id = window.localStorage.getItem("id");
    this.date = this.formatDate(new Date());
  },
  methods: {
    //选择 mood
    selected(e, i) {
      this.score = i;
      var target = e.target;
      $(target)
        .removeClass("noselected")
        .addClass("selected")
        .siblings()
        .removeClass("selected")
        .addClass("noselected");
    },
    //保存数据
    save() {
      if (!(this.score || this.note)) {
        this.$toast("Mood or Note cannot all be empty");
        return;
      }
      this.$axios
        .post(this.api + "/user/" + this.id + "/mood/create", {
          detail: this.note,
          score: this.score
        })
        .then(res => {
          if (res.status == 200 && res.data.msg === "success") {
            this.$router.push({
              path: "/index"
            });
          } else {
            this.$toast("error: save failed! Please try again!");
          }
        })
        .catch(error => {
          this.$toast("Server error: save failed! Please try again!");
        });
    },
    //取消
    cancel() {
      $("#mood_select")
        .children("li")
        .removeClass("selected");
      $("#mood_select")
        .children("li")
        .removeClass("noselected");
      this.score = "";
      this.note = "";
    },
    //获取时间格式
    formatDate(date) {
      var year = date.getFullYear();
      var month = date.getMonth() + 1;
      var day = date.getDate();
      var weekDay = date.getDay();
      return [year, month, day].map(this.formatNumber).join("-");
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
.cancel {
  height: 100%;
}
</style>
