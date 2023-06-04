<template>
  <div class="container flex">
    <div class="left-area flex flex-col w-1/2">
      <div class="small-block w-64 h-16 border border-gray-400">
        <div>載入檔案</div>
        <input type="file" @change="onFileChange" />
        <button @click="reset" class="ml-2">清除</button>
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
          <span v-for="(color, index) in colors" :key="index" class="">
            <input
              type="color"
              :value="color"
              class="w-16 h-9"
              disabled="true"
            />
            <span class="text-sm">{{ color }}</span>
          </span>
        </div>
      </div>
      <div class="parameter-block mt-4 border">
        <!-- 留空 -->
      </div>
    </div>
    <div class="flex right-area flex-grow flex-wrap border" ref="gallery">
      <!-- 留空 -->
    </div>
  </div>
</template>

<script>
import palettes from '../data/palettes.js'
import { unpackKao, colorIndexesToImage, hexToRGB } from '../utils/unpack.js'

export default {
  name: 'ImageParser',
  data () {
    return {
      fileBytes: null,
      selectedFile: null,
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
  },
  methods: {
    onFileChange (event) {
      this.selectedFile = event.target.files[0]
      if (this.selectedFile) {
        const reader = new FileReader()
        reader.onload = () => {
          this.fileBytes = new Uint8Array(reader.result)
          this.drawImages()
          console.log(this.fileBytes.length)
        }
        reader.onerror = (error) => {
          console.error('Load file error:', error)
        }
        reader.readAsArrayBuffer(this.selectedFile)
      } else {
        console.error("The selected file isn't a file.")
      }
    },
    reset () {
      const gallery = this.$refs.gallery
      gallery.innerHTML = ''
    },
    drawImages () {
      if (this.fileBytes) {
        const w = 64
        const h = 80
        let cursor = 0
        const colors = this.colors.map(hexToRGB)
        const gallery = this.$refs.gallery
        while (cursor < this.fileBytes.length) {
          const data = this.fileBytes.slice(cursor)
          const [colorIndexes, used] = unpackKao(data, w, h)
          cursor += used
          console.log(this.fileBytes.length, cursor, used)
          const imageData = colorIndexesToImage(colorIndexes, w, h, colors)

          const canvas = document.createElement('canvas')
          canvas.classList = 'm-0.5'
          canvas.width = w
          canvas.height = h
          canvas.getContext('2d').putImageData(imageData, 0, 0)
          gallery.appendChild(canvas)
        }
      } else {
        console.error("The selected file isn't a file.")
      }
    }
  },
  mounted () {
    this.drawImages()
  }
}
</script>
