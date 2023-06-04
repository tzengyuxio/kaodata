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
    return [null, 0]
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

  return [indexes, dataSize]
}

export function colorIndexesToImage (indexes, w, h, colors) {
  const image = new ImageData(w, h)
  for (let i = 0; i < indexes.length; i++) {
    const color = colors[indexes[i]]
    image.data[i * 4] = color[0]
    image.data[i * 4 + 1] = color[1]
    image.data[i * 4 + 2] = color[2]
    image.data[i * 4 + 3] = 255
  }
  return image
}
