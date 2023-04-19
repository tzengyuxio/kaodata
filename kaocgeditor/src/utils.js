export function fileToImageDataArray(
  buffer,
  width,
  height,
  palette,
  halfHeight,
  count
) {
  const imageDataArray = [];

  const faceDataSize = halfHeight
    ? (width * height * 3) / 8 / 2
    : (width * height * 3) / 8;

  const faceCount =
    count === -1 ? Math.floor(buffer.byteLength / faceDataSize) : count;

  const colors = palette.map(hexToRgb);
  for (let i = 0; i < faceCount; i++) {
    const faceData = buffer.slice(i * faceDataSize, (i + 1) * faceDataSize);
    imageDataArray[i] = dataToImage(
      faceData,
      width,
      height,
      palette,
      halfHeight
    );
  }

  return imageDataArray;
}

function dataToImage(faceData, width, height, palette, halfHeight) {
  const image = new ImageData(width, height);
  const colorIndexes = toColorIndexes(faceData);
  for (let i = 0; i < colorIndexes.length; i++) {
    let color = palette[colorIndexes[i]];
    if (halfHeight) {
      let x = i % width;
      let y = Math.floor(i / width);
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

function toColorIndexes(data) {
  const groups = grouper(data, 3);
  const indexes = [];

  groups.forEach(function (element) {
    for (let i = 7; i >= 0; --i) {
      let n =
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

function hexToRgb(hex) {
  const r = parseInt(hex.substring(1, 3), 16);
  const g = parseInt(hex.substring(3, 5), 16);
  const b = parseInt(hex.substring(5, 7), 16);
  return [r, g, b];
}
