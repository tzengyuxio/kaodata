<template>
  <div class="container flex">
    <div class="left-area flex flex-col w-1/2">
      <div class="small-block w-32 h-32 border border-gray-400">
        <button class="btn bt-blue">載入檔案</button>
      </div>
      <div class="color-picker-block mt-4 border">
        <select class="mb-2" ref="presets" v-model="selectedOption">
          <option
            v-for="option in options"
            :key="option.value"
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>
        <div class="color-btn-row flex justify-center items-center" ref="row">
          <input
            type="color"
            v-for="(color, index) in colors"
            :key="index"
            :value="color"
            class="w-12 h-12 m-1"
          />
        </div>
      </div>
      <div class="parameter-block mt-4 border">
        <!-- 留空 -->
      </div>
    </div>
    <div class="right-area flex-grow border">
      <!-- 留空 -->
    </div>
  </div>
</template>

<script>
import palettes from '../data/palettes.js'

export default {
  data () {
    return {
      selectedOption: 'default',
      options: Object.entries(palettes).map(([key, value]) => ({
        label: value.name,
        value: key
      }))
    }
  },
  computed: {
    colors () {
      console.log(palettes[this.selectedOption].codes)
      return palettes[this.selectedOption].codes
    }
  }
}
</script>
