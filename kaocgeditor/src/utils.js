export function fileToImageDataArray(
    buffer,
    width,
    height,
    palette,
    halfHeight,
    count,
) {
  const imageDataArray = []; // list of ImageData

  const faceDataSize = halfHeight ?
    (width * height * 3) / 8 / 2 :
    (width * height * 3) / 8;

  const faceCount =
    count === -1 ? Math.floor(buffer.byteLength / faceDataSize) : count;

  const colors = palette.map(hexToRgb);
  for (let i = 0; i < faceCount; i++) {
    const faceData = buffer.slice(i * faceDataSize, (i + 1) * faceDataSize);
    imageDataArray[i] = dataToImage(
        faceData,
        width,
        height,
        colors,
        halfHeight,
    );
  }

  return imageDataArray;
}

export function dataToImage(faceData, width, height, colors, halfHeight) {
  const image = new ImageData(width, height);
  const colorIndexes = toColorIndexes(faceData);
  for (let i = 0; i < colorIndexes.length; i++) {
    const color = colors[colorIndexes[i]];
    if (halfHeight) {
      const x = i % width;
      const y = Math.floor(i / width);
      let idx = (2 * y * width + x) * 4;
      image.data[idx] = color[0];
      image.data[idx + 1] = color[1];
      image.data[idx + 2] = color[2];
      image.data[idx + 3] = 255;
      idx = ((2 * y + 1) * width + x) * 4;
      image.data[idx] = color[0];
      image.data[idx + 1] = color[1];
      image.data[idx + 2] = color[2];
      image.data[idx + 3] = 255;
    } else {
      image.data[i * 4] = color[0];
      image.data[i * 4 + 1] = color[1];
      image.data[i * 4 + 2] = color[2];
      image.data[i * 4 + 3] = 255;
    }
  }
  return image;
}

/**
 * 將 ImageData 轉換成 FaceData(索引值陣列)
 * @param {ImageData} imageData
 * @param {Array} colors
 * @return {Uint8Array}
 */
export function imageToData(imageData, colors) {
  const indexData = [];

  for (let i = 0; i < imageData.data.length; i += 4) {
    const r = imageData.data[i];
    const g = imageData.data[i + 1];
    const b = imageData.data[i + 2];
    const colorIndex = colors.findIndex(
        ([rc, gc, bc]) => rc === r && gc === g && bc === b,
    );
    indexData.push(colorIndex != -1 ? colorIndex : 0);
  }

  // 將 indexData 轉換成 3 bytes FaceData
  const bytes = new Uint8Array((indexData.length / 8) * 3);

  for (let i = 0; i < indexData.length; i += 8) {
    const byteOffset = (i / 8) * 3;
    let byte1 = 0;
    let byte2 = 0;
    let byte3 = 0;

    for (let j = 0; j < 8; j++) {
      const bit = (indexData[i + j] & 0b100) >> 2; // 取第一個 bit
      byte1 += bit << (7 - j); // 注意 byte1 需要反轉過來
    }
    bytes[byteOffset] = byte1;

    for (let j = 0; j < 8; j++) {
      const bit = (indexData[i + j] & 0b010) >> 1; // 取第二個 bit
      byte2 += bit << (7 - j);
    }
    bytes[byteOffset + 1] = byte2;

    for (let j = 0; j < 8; j++) {
      const bit = indexData[i + j] & 0b001; // 取第三個 bit
      byte3 += bit << (7 - j);
    }
    bytes[byteOffset + 2] = byte3;
  }

  return bytes;
}

function toColorIndexes(data) {
  const groups = grouper(data, 3);
  const indexes = [];

  groups.forEach(function(element) {
    for (let i = 7; i >= 0; --i) {
      const n =
        (((element[0] >> i) & 1) << 2) |
        (((element[1] >> i) & 1) << 1) |
        ((element[2] >> i) & 1);
      indexes.push(n);
    }
  });

  return indexes;
}

function grouper(arr, size, fillValue = null) {
  const groups = [];
  for (let i = 0; i < arr.length; i += size) {
    groups.push(arr.slice(i, i + size));
  }
  if (fillValue !== null && groups.length * size < arr.length) {
    const fillLength = size - (arr.length % size);
    const fillArr = new Array(fillLength).fill(fillValue);
    groups.push([...arr.slice(groups.length * size), ...fillArr]);
  }
  return groups;
}

export function hexToRgb(hex) {
  const r = parseInt(hex.substring(1, 3), 16);
  const g = parseInt(hex.substring(3, 5), 16);
  const b = parseInt(hex.substring(5, 7), 16);
  return [r, g, b];
}

export function usedColorsOfImageData(imageData) {
  const colors = new Set();
  for (let i = 0; i < imageData.data.length; i += 4) {
    const color = imageData.data.slice(i, i + 3);
    colors.add(color.toString());
  }
  return colors;
}
