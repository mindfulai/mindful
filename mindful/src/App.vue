<template>
  <div id="app">
    <transition name="fade"  mode="out-in">
      <router-view/>
    </transition>
  </div>
</template>

<script>
export default {
  name: "App"
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
.fade-enter {
  opacity: 0;
}
.fade-leave {
  opacity: 1;
}

.fade-enter-active {
  opacity: 1;
  transition: opacity 0.05s;
}
.fade-leave-active {
  opacity: 0;
  transition: opacity 0.05s;
}
</style>
