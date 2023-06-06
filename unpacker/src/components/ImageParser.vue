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
        <OffsetInfos />
      </div>
    </div>
    <div class="flex right-area flex-grow flex-wrap border" ref="gallery">
      <!-- 留空 -->
    </div>
  </div>
</template>

<script>
import OffsetInfos from './OffsetInfos.vue'
import palettes from '../data/palettes.js'
import {
  unpackKao,
  unpackGrp,
  unpackNpk,
  colorIndexesToImage,
  hexToRGB
} from '../utils/unpack.js'

export default {
  name: 'ImageParser',
  components: { OffsetInfos },
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
      this.reset()
      this.selectedFile = event.target.files[0]
      if (this.selectedFile) {
        const reader = new FileReader()
        reader.onload = () => {
          this.fileBytes = new Uint8Array(reader.result)
          this.drawImages()
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
      const unpackers = { kao: unpackKao, npk: unpackNpk, grp: unpackGrp }
      if (this.fileBytes) {
        let cursor = 0
        const colors = this.colors.map(hexToRGB)
        const gallery = this.$refs.gallery
        let unpacker = null
        while (cursor < this.fileBytes.length) {
          const data = this.fileBytes.slice(cursor)
          if (unpacker === null) {
            const type = this.guessType(data)
            console.log('guess type: ', type)
            unpacker = unpackers[type]
          }
          const [colorIndexes, used, w, h] = unpacker(data, 64, 80)
          if (colorIndexes === null) {
            break
          }
          console.log('drawImages:', this.fileBytes.length, cursor, used, w, h)
          cursor += used
          const imageData = colorIndexesToImage(colorIndexes, w, h, colors)

          const canvas = document.createElement('canvas')
          canvas.classList = 'image-canvas m-0.5'
          canvas.width = w
          canvas.height = h
          canvas.style.width = w + 'px'
          canvas.style.height = h + 'px'
          canvas.getContext('2d').putImageData(imageData, 0, 0)
          gallery.appendChild(canvas)
        }
      } else {
        console.error("The selected file isn't a file.")
      }
    },
    guessType (data) {
      const header = String.fromCharCode(...data.slice(0, 4))
      if (header.startsWith('NPK')) {
        return 'npk'
      }
      const w = (data[1] << 8) | data[0]
      const h = (data[3] << 8) | data[2]
      if (w > 0 && w <= 800 && h > 0 && h <= 600) {
        return 'grp'
      }
      return 'kao'
    }
  },
  mounted () {
    this.drawImages()
  }
}
</script>
