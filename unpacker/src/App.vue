<template>
 <div>
    <nav>
      <button @click="currentTab = 'HomePage'">Home</button>
      <button @click="currentTab = 'AboutPage'">About</button>
      <button @click="currentTab = 'FontCode'">Font Code</button>
    </nav>
    <component :is="currentTab"></component>
  </div>
</template>

<script>
import HomePage from './components/Home.vue';
import AboutPage from './components/About.vue';
import FontCode from './components/FontCode.vue';

export default {
	name: 'App',
	components: {
		HomePage,
		AboutPage,
		FontCode,
	},
	data() {
		return {
			currentTab: 'FontCode',
		};
	},
};
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
