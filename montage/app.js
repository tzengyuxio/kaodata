const fileInput = document.getElementById("fileInput");
const canvas = document.getElementById("canvas");
// const canvas2 = document.getElementById("canvas2");
// const context2 = canvas2.getContext('2d');

fileInput.addEventListener("change", (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.readAsArrayBuffer(file);

  reader.onload = (event) => {
    const arrayBuffer = event.target.result;
    const dataView = new DataView(arrayBuffer);
    const uint8Buffer = new Uint8Array(arrayBuffer);

    canvas.width = 64 * 16;
    canvas.height = 80 * 14;

    var faceDataSize = 960;
    const ctx = canvas.getContext("2d");
    for (let i = 0; i < 219; i++) {
      var pos = i * faceDataSize;
      var posX = (i % 16) * 64;
      var posY = Math.floor(i / 16) * 80;
      // console.log("put image at", i, posX, posY);
      var faceData = uint8Buffer.slice(pos, pos + faceDataSize);
      faceImage = dataToImage(faceData);
      ctx.putImageData(faceImage, posX, posY);
      // context2.putImageData(faceImage, 0, 0)
    }
  };
});

function dataToImage(data) {
  const imageData = new ImageData(64, 80);
  var colorIndexes = toColorIndexes(data);

  var colors = [
    [0, 0, 0],
    [85, 255, 85],
    [255, 85, 85],
    [255, 255, 85],
    [85, 85, 255],
    [85, 255, 255],
    [255, 85, 255],
    [255, 255, 255],
  ];

  for (i = 0; i < colorIndexes.length; i++) {
    let x = i % 64;
    let y = Math.floor(i / 64);
    var c = colors[colorIndexes[i]];
    // let idx = Math.ceil(i / 64) * 64 * 2 + (i % 64);
    let idx = (2 * y * 64 + x) * 4;
    imageData.data[idx] = c[0];
    imageData.data[idx + 1] = c[1];
    imageData.data[idx + 2] = c[2];
    imageData.data[idx + 3] = 255;
    idx = ((2 * y + 1) * 64 + x) * 4;
    imageData.data[idx] = c[0];
    imageData.data[idx + 1] = c[1];
    imageData.data[idx + 2] = c[2];
    imageData.data[idx + 3] = 255;
    // if (i < 0) {
    //   console.log('idx: ', i, idx, colorIndexes.length);
    // }
  }
  return imageData;
}

function toColorIndexes(data) {
  var groups = grouper(data, 3);

  var indexes = [];
  groups.forEach(function (element) {
    for (i = 7; i >= 0; --i) {
      n =
        (((element[0] >> i) & 1) << 2) |
        (((element[1] >> i) & 1) << 1) |
        ((element[2] >> i) & 1);
      indexes.push(n);
    }
  });

  // console.log("toColorIndexes", indexes[0], indexes[1], indexes[2], indexes[4]);

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
