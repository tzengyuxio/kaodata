import RgbQuant from 'rgbquant';

import palettes from './data/palettes';

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
  const colorIndexes = toColorIndexes(faceData);
  return colorIndexesToImage(colorIndexes, width, height, colors, halfHeight);
}

export function colorIndexesToImage(
    colorIndexes,
    width,
    height,
    colors,
    halfHeight,
) {
  const image = new ImageData(width, height);
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
 * 將 RGBA 排列的 ImageData, 依照 colors 內容轉換成 IndexArray
 * @param {ImageData} imageData
 * @param {Array} colors [[r,g,b], ...]
 * @return {Array} [0, 1, 2, ...]
 */
export function rgbImageToIndexArray(imageData, colors) {
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

  return indexData;
}

/**
 * 將 IndexArray 轉換成 FaceData(960 or 1920 bytes, 可以直接寫入 kaodata 的資料)
 * @param {Array} indexArray
 * @return {Uint8Array}
 * @example
 * const indexArray = [0, 1, 2, 3, 4, 5, 6, 7];
 * const faceData = indexArrayToFaceData(indexArray);
 * console.log(faceData); // Uint8Array(3) [15, 51, 85]
 *                        // ([0x0F, 0x33, 0x55])
 *                        // ([0b00001111, 0b00110011, 0b01010101])
 */
export function indexArrayToFaceData(indexArray) {
  const bytes = new Uint8Array((indexArray.length / 8) * 3);

  for (let i = 0; i < indexArray.length; i += 8) {
    const byteOffset = (i / 8) * 3;
    let byte1 = 0;
    let byte2 = 0;
    let byte3 = 0;

    for (let j = 0; j < 8; j++) {
      const bit = (indexArray[i + j] & 0b100) >> 2; // 取第一個 bit
      byte1 += bit << (7 - j); // 注意 byte1 需要反轉過來
    }
    bytes[byteOffset] = byte1;

    for (let j = 0; j < 8; j++) {
      const bit = (indexArray[i + j] & 0b010) >> 1; // 取第二個 bit
      byte2 += bit << (7 - j);
    }
    bytes[byteOffset + 1] = byte2;

    for (let j = 0; j < 8; j++) {
      const bit = indexArray[i + j] & 0b001; // 取第三個 bit
      byte3 += bit << (7 - j);
    }
    bytes[byteOffset + 2] = byte3;
  }

  return bytes;
}

/**
 * 將 ImageData 轉換成 FaceData
 * @param {ImageData} imageData
 * @param {Array} colors
 * @return {Uint8Array}
 */
export function imageToData(imageData, colors) {
  const indexData = rgbImageToIndexArray(imageData, colors);

  // 將 indexData 轉換成 3 bytes 一組的 FaceData
  const bytes = indexArrayToFaceData(indexData);

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

export function usedColorsOfUint8Array(buffer) {
  const colors = new Set();
  const colorCount = {};
  for (let i = 0; i < buffer.length; i += 4) {
    const color = buffer.slice(i, i + 3);
    colors.add(color.toString());
    if (color.toString() in colorCount) {
      colorCount[color.toString()] += 1;
    } else {
      colorCount[color.toString()] = 1;
    }
  }
  console.log(colorCount);
  return colors;
}

export function usedColorsOfImageData(imageData) {
  return usedColorsOfUint8Array(imageData.data);
}

function findClosestColorIndex(colors, targetColor, skipIndexes = []) {
  let closestIndex = 0;
  let closestDist = Number.MAX_VALUE;

  for (let i = 0; i < colors.length; i++) {
    if (skipIndexes.includes(i)) continue;

    // 計算與目標顏色之間的距離
    const dist = Math.sqrt(
        Math.pow(colors[i][0] - targetColor[0], 2) +
                Math.pow(colors[i][1] - targetColor[1], 2) +
                Math.pow(colors[i][2] - targetColor[2], 2),
    );

    // 如果比當前的距離更接近目標顏色，則更新索引和距離
    if (dist < closestDist) {
      closestIndex = i;
      closestDist = dist;
    }
  }

  return closestIndex;
}

function calculateColorDistance(colors1, colors2) {
  let totalDistance = 0;
  for (let i = 0; i < colors1.length; i++) {
    let distance = Number.MAX_VALUE;
    for (let j = 0; j < colors2.length; j++) {
      const [r1, g1, b1] = colors1[i];
      const [r2, g2, b2] = colors2[j];
      const d = (r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2;
      if (d == 0) {
        distance = 0;
        break;
      } else if (d < distance) {
        distance = d;
      }
    }
    totalDistance += distance;
  }
  return totalDistance;
}

function findClosestPalette(targetPalette) {
  // iterate over palettes
  let closestPalette = null;
  let closestDistance = Number.MAX_VALUE;
  Object.values(palettes).forEach((palette) => {
    if (closestDistance == 0) return;
    const comparePalette = palette.codes.map(hexToRgb);
    const distance = calculateColorDistance(targetPalette, comparePalette);
    if (distance < closestDistance) {
      closestDistance = distance;
      closestPalette = palette.id;
    }
  });
  return [closestPalette, closestDistance];
}

function convertSetToArray(set) {
  const arr = [];
  set.forEach((value) => {
    const colors = value.split(',');
    arr.push(colors.map((color) => parseInt(color)));
  });
  return arr;
}

// return array of index in half size
function colorIndexesInHalfHeight(colorIndexes, width) {
  const arr = Array(colorIndexes.length / 2);
  colorIndexes.map((colorIndex, index) => {
    const x = index % width;
    const y = Math.floor(index / width);
    if (y % 2 == 0) {
      const i = Math.floor(y / 2) * width + x;
      arr[i] = colorIndex;
    }
  });

  return arr;
}

// return an array for ImageData which is double height
function doubleArray(origin, width) {
  const target = [];
  for (let i = 0; i < origin.length; i++) {
    target.push(origin[i]);
    if ((i + 1) % (4 * width) == 0) {
      target.push(...origin.slice(i - 4 * width + 1, i + 1));
    }
  }
  return target;
}

export function paletteConvertTable(palette) {
  const KOEI_PALETTE = [
    [0, 0, 0],
    [85, 255, 85],
    [255, 85, 85],
    [255, 255, 85],
    [85, 85, 255],
    [85, 255, 255],
    [255, 85, 255],
    [255, 255, 255],
  ];
  const table = Array(8); // rgbQuant paltte index -> KOEI Kao palette index
  const blackIndex = findClosestColorIndex(palette, [0, 0, 0]);
  const whiteIndex = findClosestColorIndex(palette, [255, 255, 255]);
  table[blackIndex] = 0;
  table[whiteIndex] = 7;
  const skipIndexes = [0, 7];
  for (let i = 0; i < 8; i++) {
    if (i === blackIndex || i === whiteIndex) continue;
    const idx = findClosestColorIndex(
        KOEI_PALETTE,
        palette[i],
        skipIndexes,
    );
    table[i] = idx;
    skipIndexes.push(idx);
  }
  return table;
}

export function doColorQuntization(imageData, palette, dithKern, halfHeight) {
  const imgData = new ImageData(
      new Uint8ClampedArray(imageData.data),
      imageData.width,
      imageData.height,
  );
  const opts = {
    colors: 8,
    method: 1, // histogram method, 2: within subregions; 1: global
    initColors: 56, // if method = 1
    dithKern: dithKern,
    dithDelta: 0.075,
    palette: palette,
  };
  const q = new RgbQuant(opts);
  q.sample(imgData);
  // reduce() retType: 1 - Uint8Array; 2 - Indexed array
  const out = q.reduce(imgData);
  const arr = new Uint8ClampedArray(out.buffer);
  return new ImageData(arr, imgData.width, imgData.height);
}

/**
 * 將圖像依所需比例裁切後，轉換為 ImageData
 * @param {HTMLImageElement} image
 * @param {*} sx 裁切起始 x 座標
 * @param {*} sy 裁切起始 y 座標
 * @param {*} sw 裁切寬度
 * @param {*} sh 裁切高度
 * @param {*} dx 繪製起始 x 座標
 * @param {*} dy 繪製起始 y 座標
 * @param {*} dw 繪製寬度
 * @param {*} dh 繪製高度
 * @return {ImageData}
 */
export function cropImgToImageData(image, sx, sy, sw, sh, dx, dy, dw, dh) {
  console.log('cropImgToImageData', sx, sy, sw, sh, dx, dy, dw, dh);
  // 創建 canvas, draw image on canvas
  const canvas = document.createElement('canvas');
  canvas.width = dw;
  canvas.height = dh;
  // 將圖像繪製到 canvas 上下文中
  const ctx = canvas.getContext('2d');
  ctx.drawImage(image, sx, sy, sw, sh, dx, dy, dw, dh);
  // 獲取 ImageData 對象
  return ctx.getImageData(0, 0, dw, dh);
}

export class SubstitudeImage {
  constructor(imageData, imageDataHH) {
    const usedColors = usedColorsOfImageData(imageData);
    const usedColorsHH = usedColorsOfImageData(imageDataHH);
    this.isIndexedColor = usedColors.size <= 8;
    this.imageData = new ImageData(
        new Uint8ClampedArray(imageData.data),
        imageData.width,
        imageData.height,
    );
    this.imageDataHH = imageDataHH ?
            new ImageData(
                new Uint8ClampedArray(imageDataHH.data),
                imageDataHH.width,
                imageDataHH.height,
            ) :
            null;
    this.colorIndexes = [];
    this.appliedImageData = [];
    console.log(
        'usedColors',
        usedColors,
        usedColorsHH,
        this.isIndexedColor,
    );
    if (this.isIndexedColor) {
      const usedPalette = convertSetToArray(usedColors);
      const [paletteId, distance] = findClosestPalette(usedPalette);
      console.log('paletteId, distance', paletteId, distance);
      // TODO(yuxioz): if distance is not zero, do color quantization again
      const colors = palettes[paletteId].codes.map(hexToRgb);
      this.colorIndexes = rgbImageToIndexArray(this.imageData, colors);
    }
  }

  /**
     * 判斷是否直接使用 this.colorIndexes
     * @param {boolean} halfHeight
     * @return {boolean}
     */
  isUseColorIndex() {
    return this.isIndexedColor && this.colorIndexes.length > 0;
  }

  /**
     * 依照指定的調色盤，重新產生圖片
     * @param {Array} palette
     * @param {boolean} halfHeight
     * @return {ImageData}
     */
  applyPalette(palette, halfHeight = false) {
    if (this.isUseColorIndex()) {
      const colorIndexes = halfHeight ?
                colorIndexesInHalfHeight(
                    this.colorIndexes,
                    this.imageData.width,
                ) :
                this.colorIndexes;
      return colorIndexesToImage(
          colorIndexes,
          this.imageData.width,
          this.imageData.height,
          palette,
          halfHeight,
      );
    } else if (halfHeight) {
      // do color quantization again.
      const imageDataHH = doColorQuntization(
          this.imageDataHH,
          palette,
          'FloydSteinberg',
          halfHeight,
      );
      const newData = doubleArray(imageDataHH.data, 64);
      console.log(
          'actual length',
          newData.length,
          imageDataHH.data.length,
      );
      console.log(
          'ecpected length',
          imageDataHH.width * imageDataHH.height * 4 * 2,
      );
      const imageData = new ImageData(
          new Uint8ClampedArray(newData),
          imageDataHH.width,
          imageDataHH.height * 2,
      );
      this.appliedImageData = new ImageData(
          new Uint8ClampedArray(imageDataHH.data),
          imageDataHH.width,
          imageDataHH.height,
      );
      return imageData;
    } else {
      // do color quantization again.
      const imageData = doColorQuntization(
          this.imageData,
          palette,
          'FloydSteinberg',
          halfHeight,
      );
      this.appliedImageData = new ImageData(
          new Uint8ClampedArray(imageData.data),
          imageData.width,
          imageData.height,
      );
      return imageData;
    }
  }

  getFaceData(colors, halfHeight) {
    if (this.isUseColorIndex()) {
      const colorIndexes = halfHeight ?
                colorIndexesInHalfHeight(
                    this.colorIndexes,
                    this.imageData.width,
                ) :
                this.colorIndexes;
      return indexArrayToFaceData(colorIndexes);
    } else if (halfHeight) {
      return imageToData(this.appliedImageData, colors);
    } else {
      return imageToData(this.appliedImageData, colors);
    }
  }
}

// TODOs:
// 6. disk 支援
// 7. 更詳細 instruction: show-pic, view-in-game, update-pic
// 8. 替換按鈕的 enable
