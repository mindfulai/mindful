<template>
  <div>
    <nav-header :name='name'></nav-header>
    <div class="content">
      <div class="content_box">
        <h4>Review Sunday 04 Nov 2018</h4>

        <div class="content_box_inner">
          <form method="post" action="" class="basic">
            <b>Mood:Great</b>
            <ul class="mood_rate clearfix" id="select">
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
              <textarea rows="4" name="note" maxlength="240" class="form-control"></textarea>
            </div>
            <div class="form-group">
              <b>Custom tags:</b>
              <div class="clearfix taggle_holder">
                <input class="taggle_placeholder" style="opacity: 1;" placeholder="Enter tags...">
              </div>
              <div class="help-block">
                Use a comma (,) to separate tags
              </div>
            </div>
            <p>
              <button type="submit" name="submit" class="save" ><i class="fa fa-check"></i> Save
              </button>
              or <a>Cancel</a>
            </p>
          </form>
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
  methods: {
    selected(e, i) {
      var target = e.target;
      $(target)
        .removeClass("noselected")
        .addClass("selected")
        .siblings()
        .removeClass("selected")
        .addClass("noselected");
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
