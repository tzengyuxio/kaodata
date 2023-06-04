<template>
  <div>
    <div>
      <label>
        <input type="radio" name="encoding" value="koeitw" checked /> KOEI-TW
      </label>
      <label>
        <input type="radio" name="encoding" value="shiftjis" /> Shift JIS
      </label>
    </div>
    <div>
      <label for="input1">輸入文字:</label>
      <input
        type="text"
        id="input1"
        v-model="inputText"
        @keyup.enter="encodeText"
      />
      <button @click="encodeText">轉換</button>
      <div>轉換結果: {{ encodedText }}</div>
    </div>
    <div>
      <label for="input2">輸入 hex string:</label>
      <input
        type="text"
        id="input2"
        v-model="inputHex"
        @keyup.enter="decodeText"
      />
      <button @click="decodeText">轉換</button>
      <div>轉換結果: {{ decodedText }}</div>
    </div>
  </div>
</template>

<script>
import Encoding from 'encoding-japanese'
import {
  orderToKOEITw,
  koeiTwToOrder,
  orderOfUnicode,
  orderToUnicode
} from '../utils/encoding-koeitw.js'

function addSpaceToText (text) {
  // 使用正則表達式來將每四個字符匹配到一個獨立的分組中
  const regex = /(.{4})/g
  // 將每四個字符替換為匹配分組中的字符和一個空格
  const newText = text.replace(regex, '$1 ')
  // 移除可能在最後添加的尾隨空格
  return newText.trim()
}

function koeiTwCodeToText (code) {
  const inputHexArray = code.replaceAll(' ', '').match(/.{1,2}/g)
  const inputUint8Array = new Uint8Array(inputHexArray.length)
  for (let i = 0; i < inputHexArray.length; i++) {
    inputUint8Array[i] = parseInt(inputHexArray[i], 16)
  }
  const outputArray = []
  for (let i = 0; i < inputUint8Array.length; i += 2) {
    const pair = new Uint8Array([inputUint8Array[i], inputUint8Array[i + 1]])
    const order = koeiTwToOrder(pair)
    outputArray.push(orderToUnicode(order))
  }
  return outputArray.join('')
}

function textToKOEITwCode (text) {
  const orders = text.split('').map((c) => orderOfUnicode(c))
  const koeiTwValues = orders.map((order) => orderToKOEITw(order))
  console.log(koeiTwValues)
  const koeiTwHexes = koeiTwValues.map((value) =>
    Array.from(value)
      .map((b) => b.toString(16).padStart(2, '0').toUpperCase())
      .join('')
  )
  return koeiTwHexes.join(' ')
}

/**
 * Converts the given text to Shift JIS encoded hex string.
 *
 * @param {string} text - the text to convert to Shift JIS encoded hex string.
 * @return {string} the Shift JIS encoded hex string representation of the input text.
 */
function textToShiftJISCode (text) {
  const unicodeArray = Encoding.stringToCode(text) // Convert string to code array
  const sjisArray = Encoding.convert(unicodeArray, {
    to: 'SJIS',
    from: 'UNICODE'
  })
  const encodedTextHexArray = Array.from(sjisArray, (byte) =>
    ('00' + byte.toString(16)).slice(-2).toUpperCase()
  )
  return addSpaceToText(encodedTextHexArray.join(''))
}

/**
 * Converts a hexadecimal code to plain text using the provided codec.
 *
 * @param {string} code - the hexadecimal code to be converted
 * @param {string} codec - the codec to be used for conversion
 * @return {string} the decoded plain text
 */
function codeToText (code, codec) {
  const shiftJISDecoder = new TextDecoder(codec)
  const inputHexArray = code.replaceAll(' ', '').match(/.{1,2}/g)
  const inputUint8Array = new Uint8Array(inputHexArray.length)
  for (let i = 0; i < inputHexArray.length; i++) {
    inputUint8Array[i] = parseInt(inputHexArray[i], 16)
  }

  const decodedText = shiftJISDecoder.decode(inputUint8Array.buffer)
  return decodedText
}

export default {
  name: 'FontCode',
  data () {
    return {
      inputText: '',
      encodedText: '',
      inputHex: '',
      decodedText: ''
    }
  },
  methods: {
    encodeText () {
      if (this.encoding() === 'shiftjis') {
        this.encodedText = textToShiftJISCode(this.inputText)
      } else {
        this.encodedText = textToKOEITwCode(this.inputText)
      }
    },
    decodeText () {
      if (this.encoding() === 'shiftjis') {
        this.decodedText = codeToText(this.inputHex, 'shift_jis')
      } else {
        this.decodedText = koeiTwCodeToText(this.inputHex)
      }
    },
    encoding () {
      const encodingRadios = document.getElementsByName('encoding')
      let selectedEncoding = 'koeitw'
      for (let i = 0; i < encodingRadios.length; i++) {
        if (encodingRadios[i].checked) {
          selectedEncoding = encodingRadios[i].value
          break
        }
      }

      return selectedEncoding
    }
  }
}
</script>
