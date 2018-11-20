<template>
  <div>
    <nav-header :name="name"></nav-header>
    <div class="tabs">
      <div class="tab" :class="activeTab=='day'?'active':''" @click="changeTab('day')">Day</div>
      <div class="tab" :class="activeTab=='week'?'active':''" @click="changeTab('week')">Week</div>
      <div class="tab" :class="activeTab=='month'?'active':''"  @click="changeTab('month')">Month</div>
    </div>
    <div class="content index_content">
      <!--<div class="date">
        <div class="arrow left"><i class="fa fa-angle-left"></i></div>
        2018-11-05
        <div class="arrow right"><i class="fa fa-angle-right"></i></div>
      </div>-->
      <transition name="fade" mode="in-out">
        <!-- day Tab -->
        <div v-show="activeTab=='day'"> 
          <!--Facebook-->
          <div class="content_box">
            <h4>FaceBook</h4>

            <div class="content_box_inner">
              <div class="line clearfix">
                <div class="left left_table">
                  <table class="table">
                    <tbody>
                    <tr>
                      <td class="left" valign="bottom"><b>{{posts}}</b> FB posts</td>
                      <td class="right" valign="bottom"></td>
                    </tr>
                    <tr>
                      <td colspan="2" class="percent-bg">
                        <div class="percent-meter" style="width: 0%; background-color: #4E7CA0"></div>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                  <!-- <table class="table">
                    <tbody>
                    <tr>
                      <td class="left" valign="bottom"><b>0</b> FB reactions</td>
                      <td class="right" valign="bottom"></td>
                    </tr>
                    <tr>
                      <td colspan="2" class="percent-bg">
                        <div class="percent-meter" style="width: 0%; background-color: #4E7CA0"></div>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                  <table class="table">
                    <tbody>
                    <tr>
                      <td class="left" valign="bottom"><b>0</b> FB comments</td>
                      <td class="right" valign="bottom"></td>
                    </tr>
                    <tr>
                      <td colspan="2" class="percent-bg">
                        <div class="percent-meter" style="width: 0%; background-color: #4E7CA0"></div>
                      </td>
                    </tr>
                    </tbody>
                  </table> -->
                </div>
                <div class="right right_icon">
                  <i class="fa fa-facebook-square FB"></i>
                </div>
              </div>
              <div class="connector">
                <i class="fa fa-exchange"></i>
                FaceBook
              </div>
              <div class="chart">
              </div>
            </div>
          </div>
          <!--Twitter-->
          <div class="content_box">
            <h4>Twitter</h4>

            <div class="content_box_inner">
              <div class="line clearfix">
                <div class="left left_table">
                  <table class="table">
                    <tbody>
                    <tr>
                      <td class="left" valign="bottom"><b>{{tweets}}</b> tweets</td>
                      <!--<td class="right" valign="bottom"><b>0</b> avg</td>-->
                    </tr>
                    <tr>
                      <td colspan="2" class="percent-bg">
                        <div class="percent-meter" style="width: 0%; background-color: #55acee"></div>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                  <table class="table">
                    <tbody>
                    <tr>
                      <td class="left" valign="bottom"><b>{{mentions}}</b> mentions</td>
                      <!--<td class="right" valign="bottom"><b>0</b> avg</td>-->
                    </tr>
                    <tr>
                      <td colspan="2" class="percent-bg">
                        <div class="percent-meter" style="width: 0%; background-color: #55acee"></div>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </div>
                <div class="right right_icon">
                  <i class="fa fa-twitter-square"></i>
                  <!--<i class="fa fa-facebook-square"></i>-->
                </div>
              </div>
              <div class="connector">
                <i class="fa fa-exchange"></i>
                Twitter
                <!-- <a class="authorize">Authorize</a> -->
              </div>
              <div class="chart">
              </div>
            </div>
          </div>
          <!--Mood-->
          <div class="content_box">
            <h4>Mood</h4>

            <div class="content_box_inner">
              <div class="mood">
                <div class="mood_number mood_active">5</div>
              </div>
              <router-link class="edit_mood" to="/edit_mood">
                <i class="fa fa-pencil"></i>
                Rate day
              </router-link>
              <div class="connector">
                <i class="fa fa-exchange"></i>
                Android
              </div>
              <div class="chart">

              </div>
            </div>
          </div>
          <!--Events-->
          <!-- <div class="content_box">
            <h4>Events</h4>

            <div class="content_box_inner">
              <div class="line clearfix">
                <div class="left left_table">
                  <table class="table">
                    <tbody>
                    <tr>
                      <td class="left" valign="bottom"><b>0</b> today</td>
                      <td class="right" valign="bottom"></td>
                    </tr>
                    <tr>
                      <td colspan="2" class="percent-bg">
                        <div class="percent-meter" style="width: 0%; background-color: #E1546C"></div>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                  <table class="table">
                    <tbody>
                    <tr>
                      <td class="left" valign="bottom"><b>00:00</b> in events</td>
                      <td class="right" valign="bottom"></td>
                    </tr>
                    <tr>
                      <td colspan="2" class="percent-bg">
                        <div class="percent-meter" style="width: 0%; background-color: #E1546C"></div>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </div>
                <div class="right right_icon">
                  <i class="fa fa-file-text events"></i>
                </div>
              </div>
              <div class="connector">
                <i class="fa fa-exchange"></i>
                Events
              </div>
              <div class="chart">
              </div>
            </div>
          </div> -->
          <!--Location-->
          <div class="content_box">
            <h4>Location</h4>

            <div class="content_box_inner">
              
                <a style="display:block;height:100%;" target="_blank" href="https://google.com/maps/@37.87,-122.26,16z">
                  <img style="width:100%;" src="https://api.mapbox.com/styles/v1/joshsharp/cjmfw5rw71t0m2rrwsj8ywbi1/static/-122.26,37.87,12,0/360x160?access_token=pk.eyJ1Ijoiam9zaHNoYXJwIiwiYSI6ImNqbHJta2ozMjA2b20zc3RhNTFuMm4zZGEifQ.sN74U85oG02UI3juN-NZtA" alt="Map">
                </a>
              <div class="connector">
                <i class="fa fa-exchange"></i>
                Android
              </div>
              <div class="chart">
              </div>
            </div>
          </div>
          <!--Weather-->
          <div class="content_box">
            <h4>Weather</h4>
      
            <div class="content_box_inner">
              <div class="line clearfix">
                <div class="left left_table">
                  <div class="temp"> <span class="min_temp">{{daily.temperatureMin}}</span> / <span class="max_temp">{{daily.temperatureMax}}</span> ℃</div>
                  <ul class="weather_tab clearfix">
                    <li>Precipitation <span class="weather_num">{{daily.precipIntensity}}</span></li>
                    <li>Air pressure <span  class="weather_num">{{daily.pressure}}</span></li>
                    <li>Cloud cover <span  class="weather_num">{{daily.cloudCover}}</span></li>
                    <li>Humidity <span class="weather_num">{{daily.humidity}}</span></li>
                    <li>Wind speed <span  class="weather_num">{{daily.windSpeed}}</span></li>
                    <li>Day length <span class="weather_num">{{daily.dailyLength}}</span></li>
                  </ul>
                  <p class="weather_summary">{{daily.summary}}</p>
                </div>
                <div class="right right_icon">
                  <i class="fa fa-sun-o weather"></i>
                </div>
              </div>
              <div class="connector">
                <i class="fa fa-exchange"></i>
                Dark Sky
              </div>
              <div class="chart">
              </div>
            </div>
          </div>
        </div>
      </transition>
      <transition name="fade" mode="in-out">
        <!-- week Tab -->
        <div v-show="activeTab=='week'">
          <!--Facebook-->
          <div class="content_box">
            <h4>Totals posts for this week</h4>

            <div class="content_box_inner">
              <div class="line clearfix">
                <div class="left left_table">
                  <table class="table">
                    <tbody>
                    <tr>
                      <td class="left" valign="bottom"><b>{{posts}}</b> FB posts</td>
                      <td class="right" valign="bottom"></td>
                    </tr>
                    <tr>
                      <td colspan="2" class="percent-bg">
                        <div class="percent-meter" style="width: 0%; background-color: #4E7CA0"></div>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </div>
                <div class="right right_icon">
                  <i class="fa fa-facebook-square FB"></i>
                </div>
              </div>
            </div>
          </div>
          <!--Twitter-->
          <div class="content_box">
            <h4>Totals tweets and mentions for this week</h4>

            <div class="content_box_inner">
              <div class="line clearfix">
                <div class="left left_table">
                  <table class="table">
                    <tbody>
                    <tr>
                      <td class="left" valign="bottom"><b>{{tweets}}</b> tweets</td>
                    </tr>
                    <tr>
                      <td colspan="2" class="percent-bg">
                        <div class="percent-meter" style="width: 0%; background-color: #55acee"></div>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                  <table class="table">
                    <tbody>
                    <tr>
                      <td class="left" valign="bottom"><b>{{mentions}}</b> mentions</td>
                    </tr>
                    <tr>
                      <td colspan="2" class="percent-bg">
                        <div class="percent-meter" style="width: 0%; background-color: #55acee"></div>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </div>
                <div class="right right_icon">
                  <i class="fa fa-twitter-square"></i>
                </div>
              </div>
            </div>
          </div> 
          <!-- others -->
          <div class="content_box">
            <h4>Totals others for this week</h4>
            
            <div class="content_box_inner">
              <!-- week -->
              <div class="calendar_wrapper">
                <div class="week_day">
                  <div class="weeklist">MON</div>
                  <div class="weeklist">TUE</div>
                  <div class="weeklist">WED</div>
                  <div class="weeklist">THU</div>
                  <div class="weeklist">FRI</div>
                  <div class="weeklist">SAT</div>
                  <div class="weeklist">SUN</div>
                </div>
              </div>
              <!-- facebook -->
              <!-- <div class="line bottom_border">
                <h3 class="chart_header"><i class="fa fa-facebook-square facebook_icon"></i>FaceBook</h3>
                <p class="chart_totals"><b>{{posts}}</b> facebook posts</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in signDays" :key="index" >{{item == null ? '' : item.normalday}}
                  </div>
                </div>
              </div> -->
              <!-- twitter -->
              <!-- <div class="line">
                <h3 class="chart_header"><i class="fa fa-twitter-square twitter_icon"></i>Twitter</h3>
                <p class="chart_totals"><b>{{tweets}}</b> tweets</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in signDays" :key="index" >{{item == null ? '' : item.normalday}}
                  </div>
                </div>
              </div> -->
              <!-- mood -->
              <div class="line">
                <h3 class="chart_header">Mood</h3>
                <!-- <p class="chart_totals"><b>{{tweets}}</b> tweets</p> -->
                <div class="month_day">
                  <div v-for="(item,index) in moods" :key="index" class="day_list ">
                    <a class=" chart_number mood_number" :class="'mood-'+item.mood">{{item.mood==''?'no rate':''}}</a>
                    
                  </div>
                </div>
              </div>
              <!-- events -->
              <div class="line bottom_border">
                <h3 class="chart_header"><i class="fa fa-file-text events_icon"></i>Events</h3>
                <p class="chart_totals"><b>{{event}}</b> events</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in events" :key="index" :class="item.events?'events_active':''" >{{item == null ? '' : item.events}}
                  </div>
                </div>
              </div>
              <!-- weather -->
              <div class="line">
                <h3 class="chart_header"><i class="fa fa-sun-o weather_icon"></i>Weather</h3>
                <p class="chart_totals">Max temp</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in maxTemp" :key="index" :class="item.temp?'max_temp_active':''">{{item == null ? '' : item.temp}}
                  </div>
                </div>
                <p class="chart_totals">Min temp</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in minTemp" :key="index" :class="item.temp?'min_temp_active':''">{{item == null ? '' : item.temp}} 
                  </div>
                </div>
                <p class="chart_totals">Precipitation</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in Precip" :key="index" :class="item.precip?'precip_active':''">{{item == null ? '' : item.precip}}
                  </div>
                </div>
                <p class="chart_totals">Air pressure</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in press" :key="index" :class="item.press?'press_active':''">{{item == null ? '' : item.press}}
                  </div>
                </div>
                <p class="chart_totals">Cloud cover</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in cloud" :key="index" :class="item.cloud?'cloud_active':''">{{item == null ? '' : item.cloud}}
                  </div>
                </div>
                <p class="chart_totals">Humidity</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in humid" :key="index" :class="item.humid?'humid_active':''">{{item == null ? '' : item.humid}}
                  </div>
                </div>
                <p class="chart_totals">Wind speed</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in wind" :key="index" :class="item.wind?'wind_active':''">{{item == null ? '' : item.wind}}
                  </div>
                </div>
                <p class="chart_totals">Day length</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in dayLength" :key="index" :class="item.day_length?'day_length_active':''">{{item == null ? '' : item.day_length}}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
      <transition name="fade" mode="in-out">
        <!-- month Tab -->
        <div v-show="activeTab=='month'">
          <!--Facebook-->
          <div class="content_box">
            <h4>Totals posts for this month</h4>

            <div class="content_box_inner">
              <div class="line clearfix">
                <div class="left left_table">
                  <table class="table">
                    <tbody>
                    <tr>
                      <td class="left" valign="bottom"><b>{{posts}}</b> FB posts</td>
                      <td class="right" valign="bottom"></td>
                    </tr>
                    <tr>
                      <td colspan="2" class="percent-bg">
                        <div class="percent-meter" style="width: 0%; background-color: #4E7CA0"></div>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </div>
                <div class="right right_icon">
                  <i class="fa fa-facebook-square FB"></i>
                </div>
              </div>
            </div>
          </div>
          <!--Twitter-->
          <div class="content_box">
            <h4>Totals tweets and mentions for this month</h4>

            <div class="content_box_inner">
              <div class="line clearfix">
                <div class="left left_table">
                  <table class="table">
                    <tbody>
                    <tr>
                      <td class="left" valign="bottom"><b>{{tweets}}</b> tweets</td>
                      <!--<td class="right" valign="bottom"><b>0</b> avg</td>-->
                    </tr>
                    <tr>
                      <td colspan="2" class="percent-bg">
                        <div class="percent-meter" style="width: 0%; background-color: #55acee"></div>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                  <table class="table">
                    <tbody>
                    <tr>
                      <td class="left" valign="bottom"><b>{{mentions}}</b> mentions</td>
                      <!--<td class="right" valign="bottom"><b>0</b> avg</td>-->
                    </tr>
                    <tr>
                      <td colspan="2" class="percent-bg">
                        <div class="percent-meter" style="width: 0%; background-color: #55acee"></div>
                      </td>
                    </tr>
                    </tbody>
                  </table>
                </div>
                <div class="right right_icon">
                  <i class="fa fa-twitter-square"></i>
                  <!--<i class="fa fa-facebook-square"></i>-->
                </div>
              </div>
              <!-- <div class="connector">
                <i class="fa fa-exchange"></i>
                Twitter 
              </div> -->
            </div>
          </div>
          <!-- moods/events -->
          <div class="content_box">
            <h4>Totals moods and events for this month</h4>
            
            <div class="content_box_inner">
              <!-- week -->
              <div class="calendar_wrapper">
                <div class="week_day">
                  <div class="weeklist">MON</div>
                  <div class="weeklist">TUE</div>
                  <div class="weeklist">WED</div>
                  <div class="weeklist">THU</div>
                  <div class="weeklist">FRI</div>
                  <div class="weeklist">SAT</div>
                  <div class="weeklist">SUN</div>
                </div>
                <div class="month_day" v-for="(signDay,index) in signDays" :key="index">
                  <div class="day_list"  v-for="(item,index) in signDay" :key="index" >
                    <a class="mood_a" v-if="item == null ? '' : item.normalday" :class="item.moodday?'mood-4':''">{{item == null ? '' : item.normalday}}</a>
                    <!-- <p class="event_p" v-if="item == null ? '' : item.normalday" :class="item.eventday?'events_active':''">{{item.event}}</p> -->
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- others -->
          <div class="content_box">
            <h4>Totals weather for this month</h4>
            
            <div class="content_box_inner">
              <!-- week -->
              <div class="calendar_wrapper">
                <div class="week_day">
                  <div class="weeklist">MON</div>
                  <div class="weeklist">TUE</div>
                  <div class="weeklist">WED</div>
                  <div class="weeklist">THU</div>
                  <div class="weeklist">FRI</div>
                  <div class="weeklist">SAT</div>
                  <div class="weeklist">SUN</div>
                </div>
              </div>
              <!-- weather -->
              <div class="line">
                <h3 class="chart_header"><i class="fa fa-sun-o weather_icon"></i>Weather</h3>
                <p class="chart_totals">Max temp</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in maxTemp" :key="index" :class="item.temp?'max_temp_active':''">{{item == null ? '' : item.temp}}
                  </div>
                </div>
                <p class="chart_totals">Min temp</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in minTemp" :key="index" :class="item.temp?'min_temp_active':''">{{item == null ? '' : item.temp}} 
                  </div>
                </div>
                <p class="chart_totals">Precipitation</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in Precip" :key="index" :class="item.precip?'precip_active':''">{{item == null ? '' : item.precip}}
                  </div>
                </div>
                <p class="chart_totals">Air pressure</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in press" :key="index" :class="item.press?'press_active':''">{{item == null ? '' : item.press}}
                  </div>
                </div>
                <p class="chart_totals">Cloud cover</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in cloud" :key="index" :class="item.cloud?'cloud_active':''">{{item == null ? '' : item.cloud}}
                  </div>
                </div>
                <p class="chart_totals">Humidity</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in humid" :key="index" :class="item.humid?'humid_active':''">{{item == null ? '' : item.humid}}
                  </div>
                </div>
                <p class="chart_totals">Wind speed</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in wind" :key="index" :class="item.wind?'wind_active':''">{{item == null ? '' : item.wind}}
                  </div>
                </div>
                <p class="chart_totals">Day length</p>
                <div class="month_day">
                  <div class="day_list chart_number"  v-for="(item,index) in dayLength" :key="index" :class="item.day_length?'day_length_active':''">{{item == null ? '' : item.day_length}}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
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
      activeTab: "day",
      tweets: 0, //twitter中tweets
      mentions: 0, //twitter中metions
      posts: 0, //facebook中posts
      daily: {}, //weather 当天数据

      signDays: null,
      moods: [
        { mood: 5 },
        { mood: 2 },
        { mood: "" },
        { mood: 4 },
        { mood: "" },
        { mood: 1 },
        { mood: "" }
      ],
      event: 1,
      events: [
        { events: 1 },
        { events: "" },
        { events: "" },
        { events: "" },
        { events: "" },
        { events: "" },
        { events: "" }
      ],
      maxTemp: [
        { temp: "23℃" },
        { temp: "" },
        { temp: "21℃" },
        { temp: "" },
        { temp: "18℃" },
        { temp: "19℃" },
        { temp: "" }
      ],
      minTemp: [
        { temp: "13℃" },
        { temp: "" },
        { temp: "11℃" },
        { temp: "" },
        { temp: "8℃" },
        { temp: "9℃" },
        { temp: "" }
      ],
      Precip: [
        { precip: "0.01" },
        { precip: "" },
        { precip: "0.005" },
        { precip: "" },
        { precip: "0.0" },
        { precip: "" },
        { precip: "0.0" }
      ],
      press: [
        { press: "1.016" },
        { press: "1.028" },
        { press: "" },
        { press: "1.020" },
        { press: "" },
        { press: "1.017" },
        { press: "" }
      ],
      cloud: [
        { cloud: "13%" },
        { cloud: "" },
        { cloud: "3%" },
        { cloud: "5%" },
        { cloud: "20%" },
        { cloud: "1.017" },
        { cloud: "" }
      ],
      humid: [
        { humid: "49%" },
        { humid: "" },
        { humid: "43%" },
        { humid: "57%" },
        { humid: "" },
        { humid: "60%" },
        { humid: "40%" }
      ],
      wind: [
        { wind: "0.8" },
        { wind: "0.3" },
        { wind: "1.1" },
        { wind: "" },
        { wind: "1.9" },
        { wind: "0.6" },
        { wind: "" }
      ],
      dayLength: [
        { day_length: "10:28" },
        { day_length: "10:18" },
        { day_length: "" },
        { day_length: "09:50" },
        { day_length: "09:45" },
        { day_length: "" },
        { day_length: "09:38" }
      ]
    };
  },
  mounted() {
    this.name = this.$route.query.name || window.localStorage.getItem("name");
    this.id = this.$route.query.id || window.localStorage.getItem("id");
    window.localStorage.setItem("name", this.name);
    window.localStorage.setItem("id", this.id);
    this.changeTab("day");
  },
  methods: {
    changeTab(i) {
      this.activeTab = i;
      var date = this.formatTime(new Date());
      this.getTwitter(date, i);
      this.getFacebook(date, i);
      if (i == "day") {
        this.getWeather();
      }
      if (i == "month") {
        var getToday = new Date();
        var todayDate = getToday.getDate();
        var todayMonth = getToday.getMonth() + 1;
        var todayYear = getToday.getFullYear();
        this.buildCal(todayYear, todayMonth, [1, 4, 7, 13], [2, 6, 9, 14]);
      }
    },
    //获取 twitter
    getTwitter(date, i) {
      this.$axios
        .get(this.api + "/twitter/" + this.id + "/summary", {
          params: { datetime: date, period: i }
        })
        .then(res => {
          if (res.status == 200) {
            this.tweets = res.data.tweets;
            this.mentions = res.data.mentions;
          }
        });
    },
    //获取 facebook
    getFacebook(date, i) {
      this.$axios
        .get(this.api + "/facebook/" + this.id + "/summary", {
          params: { datetime: date, period: i }
        })
        .then(res => {
          if (res.status == 200) {
            this.posts = res.data.posts;
          }
        });
    },
    //获取 天气
    getWeather() {
      var that = this;
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          function(position) {
            var longitude = position.coords.longitude;
            var latitude = position.coords.latitude;
            that.$axios
              .post(
                that.api + "/user/" + that.id + "/location_and_weather/create",
                {
                  longitude: longitude,
                  latitude: latitude
                }
              )
              .then(res => {
                if (res.status == 200) {
                  that.daily = res.data.data[0];
                  that.daily.dailyLength = that.dailyLength(
                    that.daily.sunsetTime,
                    that.daily.sunriseTime
                  );
                }
              });
          },
          function(e) {
            that.$toast({
              message: "Error : " + e.message,
              duration: 5000
            });
          }
        );
      } else {
        that.$toast("Sorry Browser not support!");
      }
    },
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
    },
    //day length = 日落时间戳-日出时间戳
    dailyLength(sunsetTime, sunriseTime) {
      return (
        parseInt((sunsetTime - sunriseTime) / 3600) +
        ":" +
        parseInt(((sunsetTime - sunriseTime) % 3600) / 60) +
        ":" +
        ((sunsetTime - sunriseTime) % 3600) % 60
      );
    },
    //月份调用
    buildCal(iYear, iMonth, moodDay, eventDay) {
      var aMonth = new Array();
      aMonth[0] = new Array(7);
      aMonth[1] = new Array(7);
      aMonth[2] = new Array(7);
      aMonth[3] = new Array(7);
      aMonth[4] = new Array(7);
      aMonth[5] = new Array(7);
      var dCalDate = new Date(iYear, iMonth - 1, 1);
      //判断当前月份第一天周几
      var iDayOfFirst = dCalDate.getDay();
      //判断当前月份有多少天
      var curMonthDays = new Date(
        dCalDate.getFullYear(),
        dCalDate.getMonth() + 1,
        0
      ).getDate();
      //console.log("本月共有 " + curMonthDays + " 天");
      //console.log("本月第一天周 " + iDayOfFirst);
      var iDaysInMonth = (iMonth, iYear);
      var iVarDate = 1;

      var d, w;
      for (d = iDayOfFirst - 1; d < 7; d++) {
        if (moodDay.indexOf(iVarDate) > -1) {
          //console.log(111);
          aMonth[0][d] = {
            moodday: 1,
            normalday: iVarDate
          };
        } else {
          //console.log(22);
          aMonth[0][d] = {
            moodday: false,
            normalday: iVarDate
          };
        }
        if (eventDay.indexOf(iVarDate) > -1) {
          aMonth[0][d].eventday = true;
        } else {
          aMonth[0][d].eventday = false;
        }
        iVarDate++;
      }
      //处理每月第一天出现位置
      for (w = 1; w < 6; w++) {
        for (d = 0; d < 7; d++) {
          if (iVarDate <= iDaysInMonth) {
            if (moodDay.indexOf(iVarDate) > -1) {
              aMonth[w][d] = {
                moodday: true,
                normalday: iVarDate
              };
            } else {
              aMonth[w][d] = {
                moodday: false,
                normalday: iVarDate
              };
            }
            if (eventDay.indexOf(iVarDate) > -1) {
              aMonth[w][d].eventday = true;
            } else {
              aMonth[w][d].eventday = false;
            }
            if (iVarDate == curMonthDays) {
              this.signDays = aMonth;
              return aMonth;
            } else {
              iVarDate++;
            }
          }
        }
      }
    }
  },
  components: {
    navHeader
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.fade-enter {
  opacity: 0;
}
.fade-leave {
  opacity: 1;
}
.fade-enter-active {
  transition: opacity 0.5s;
}
.fade-leave-active {
  opacity: 0;
  transition: opacity 0.5s;
}

.calendar_wrapper {
  height: auto;
}

.week_day,
.month_day {
  width: 100%;
  display: flex;
}

.weeklist,
.day_list {
  position: relative;
  flex: 1;
  font-size: 0.3rem;
  text-align: center;
  line-height: 0.8rem;
}
.month_day {
  border-bottom: 1px solid #e1e2e9;
}
.line {
  padding: 0.2rem 0;
}
.bottom_border {
  border-bottom: 0.03rem solid #e1e2e9;
}
.chart_header {
  padding: 0 0.2rem;
  line-height: 0.6rem;
  font-size: 0.32rem;
}
.chart_header i {
  font-size: 0.4rem;
  margin-right: 0.2rem;
}
.facebook_icon {
  color: #4e7ca0;
}
.twitter_icon {
  color: #55acee;
}
.events_icon {
  color: #e1546c;
}
.weather_icon {
  color: #ffcc01;
}
.chart_totals {
  line-height: 0.5rem;
  font-size: 0.3rem;
  color: #6f7680;
  margin-bottom: 0.1rem;
}
.chart_totals b {
  font-weight: 900;
}
.chart_number {
  line-height: 0.18rem;
  background: #dbdce5;
  font-size: 0.16rem;
  color: #6f7680;
  border-radius: 0.06rem;
}
.mood_number {
  display: inline-block;
  height: 0.8rem;
  width: 0.8rem;
  border-radius: 50%;
  text-align: center;
  line-height: 0.8rem;
  background: #dbdce5;
}
.facebook_number {
  background: #4e7ca0;
  color: #fff;
}
.twitter_number {
  background: #55acee;
  color: #fff;
}

.day_list {
  padding: 0 0.05rem;
}

.event_p {
  height: 0.2rem;
  line-height: 0.2rem;
  background: #dbdce5;
  font-size: 0.2rem;
  text-align: right;
  padding-right: 0.1rem;
}
.mood_a {
  display: inline-block;
  height: 0.6rem;
  width: 0.6rem;
  border-radius: 50%;
  text-align: center;
  line-height: 0.6rem;
  background: #dbdce5;
}
.mood-1 {
  background: #df3e3e;
  color: #fff;
}
.mood-2 {
  background: #df953e;
  color: #fff;
}
.mood-3 {
  background: #b1d020;
  color: #fff;
}
.mood-4 {
  background: #68db36;
  color: #fff;
}
.mood-5 {
  background: #00b50d;
  color: #fff;
}
.events_active {
  background: #e1546c;
  color: #fff;
}
.max_temp_active {
  background: #ff73a5;
  color: #fff;
}
.min_temp_active {
  background: #ff6f6f;
  color: #fff;
}
.precip_active {
  background: #ffa06c;
  color: #fff;
}
.press_active {
  background: #ffd46c;
  color: #fff;
}
.cloud_active {
  background: #6cff7e;
  color: #fff;
}
.humid_active {
  background: #94ff73;
  color: #fff;
}
.wind_active {
  background: #68db36;
  color: #fff;
}
.day_length_active {
  background: #00b50d;
  color: #fff;
}
</style>
