function grouper (arr, size, fillValue = null) {
  const groups = []
  for (let i = 0; i < arr.length; i += size) {
    groups.push(arr.slice(i, i + size))
  }
  if (fillValue !== null && groups.length * size < arr.length) {
    const fillLength = size - (arr.length % size)
    const fillArr = new Array(fillLength).fill(fillValue)
    groups.push([...arr.slice(groups.length * size), ...fillArr])
  }
  return groups
}

export function hexToRGB (hex) {
  const r = parseInt(hex.substring(1, 3), 16)
  const g = parseInt(hex.substring(3, 5), 16)
  const b = parseInt(hex.substring(5, 7), 16)
  return [r, g, b]
}

/**
 * Unpacks Kao encoded data into an array of color indexes and returns the size of the data.
 *
 * @param {ArrayBuffer} data - the Kao encoded data to be unpacked
 * @param {number} w - the width of the image in pixels
 * @param {number} h - the height of the image in pixels
 * @return {[number], number} an array of color indexes and the size of the unpacked data used
 */
export function unpackKao (data, w, h) {
  const dataSize = ((w * h) / 8) * 3
  if (data.length < dataSize) {
    return [null, 0, w, h]
  } else if (data.length > dataSize) {
    data = data.slice(0, dataSize)
  }

  // kaocgeditor: toColorIndexes
  const groups = grouper(data, 3)
  const indexes = []

  groups.forEach(function (element) {
    for (let i = 7; i >= 0; --i) {
      const n =
        (((element[0] >> i) & 1) << 2) |
        (((element[1] >> i) & 1) << 1) |
        ((element[2] >> i) & 1)
      indexes.push(n)
    }
  })

  return [indexes, dataSize, w, h]
}

export function unpackGrp (data) {
  const w = (data[1] << 8) | data[0]
  const h = (data[3] << 8) | data[2]
  if (w <= 0 || w > 800 || h <= 0 || h > 800) {
    console.log('unpackGrp: out of range', w, h)
    return [null, 0, w, h]
  }
  let pos = 4
  const expectedSize = w * h
  const indexes = []
  while (pos < data.length && indexes.length < expectedSize) {
    const b = data[pos++]
    if (b & 0x80) {
      const runSize = (b & 0x0f) + 1
      const runOffset =
        b & 0x40 ? (((b & 0x30) >> 4) + 1) * w : (((b & 0x30) >> 4) + 1) * 4
      for (let i = 0; i < runSize * 4; ++i) {
        indexes.push(indexes[indexes.length - runOffset])
      }
    } else {
      let b1 = b & 0xff
      let b2 = data[pos++]
      const count = ((b1 & 0xf0) >> 4) + 1
      const buf = []
      for (let i = 0; i < 4; ++i) {
        const d = ((b1 & 0x08) >> 1) | ((b2 & 0x80) >> 6) | ((b2 & 0x08) >> 3)
        buf.push(d)
        b1 = b1 << 1
        b2 = b2 << 1
      }
      for (let i = 0; i < count; ++i) {
        indexes.push(...buf)
      }
    }
  }
  //   console.log('unpackGrp: info', w, h, expectedSize, indexes.length)
  return [indexes, pos, w, h]
}

export function unpackNpk (data) {
  // first 6 bytes are 'NPK016'
  // next 2 bytes: unknown yet
  const sw = (data[9] << 8) | data[8] // screen width
  const sh = (data[11] << 8) | data[10] // screen height
  const w = (data[13] << 8) | data[12]
  const h = (data[15] << 8) | data[14]
  if (sw <= 0 || sw > 800 || sh <= 0 || sh > 800 || w > sw || h > sh) {
    console.log('unpackGrp: out of range(sw, sh, w, h)', sw, sh, w, h)
    return [null, 0, w, h]
  }
  // next 32 bytes: palette (not work)
  let pos = 0x30
  const expectedSize = w * h
  const indexes = []
  while (pos < data.length && indexes.length < expectedSize) {
    const flagBit = data[pos++]
    for (let i = 0; i < 8; ++i) {
      const flag = (flagBit & (0x1 << i)) >> i
      if (flag) {
        const b = data[pos++]
        const runSize = (b & 0x1f) + 1
        const runOffset =
          b & 0x80 ? (((b & 0x60) >> 5) + 1) * w : (((b & 0x60) >> 5) + 1) * 4
        for (let i = 0; i < runSize * 4; ++i) {
          indexes.push(indexes[indexes.length - runOffset])
        }
      } else {
        let b1 = data[pos++]
        let b2 = data[pos++]
        const buf = []
        for (let i = 0; i < 4; ++i) {
          const d =
            ((b1 & 0x80) >> 4) |
            ((b1 & 0x08) >> 1) |
            ((b2 & 0x80) >> 6) |
            ((b2 & 0x08) >> 3)
          buf.push(d)
          b1 = b1 << 1
          b2 = b2 << 1
        }
        indexes.push(...buf)
      }
    }
  }
  return [indexes, pos, w, h]
}

export function colorIndexesToImage (indexes, w, h, colors) {
  const image = new ImageData(w, h)
  if (colors.length < 16) {
    // workaround
    colors.push(...colors)
  }
  for (let i = 0; i < indexes.length; i++) {
    const color = colors[indexes[i]]
    image.data[i * 4] = color[0]
    image.data[i * 4 + 1] = color[1]
    image.data[i * 4 + 2] = color[2]
    image.data[i * 4 + 3] = 255
  }
  return image
}
