<template>
  <div>
    <nav>
      <button class="border ml-1" @click="currentTab = 'HomePage'">Home</button>
      <button class="border ml-1" @click="currentTab = 'AboutPage'">About</button>
      <button class="border ml-1" @click="currentTab = 'FontCode'">Font Code</button>
      <button class="border ml-1" @click="currentTab = 'ImageParser'">Image Parser</button>
    </nav>
    <component :is="currentTab"></component>
  </div>
</template>

<script>
import HomePage from './components/Home.vue'
import AboutPage from './components/About.vue'
import FontCode from './components/FontCode.vue'
import ImageParser from './components/ImageParser.vue'

export default {
  name: 'App',
  components: {
    HomePage,
    AboutPage,
    FontCode,
    ImageParser
  },
  data () {
    return {
      currentTab: 'ImageParser'
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
