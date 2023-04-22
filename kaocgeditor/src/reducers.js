import {createSlice} from '@reduxjs/toolkit';
import RgbQuant from 'rgbquant';
import getGameInfos from './data/gameData';
import {hexToRgb} from './utils';

function resizeImage(image, width, height) {
  // 創建 Canvas 對象
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;

  // 繪製 Image 對象到 Canvas 上
  const ctx = canvas.getContext('2d');
  ctx.drawImage(image, 0, 0, width, height);

  // 將 Canvas 轉換為 Image 對象
  const resizedImage = new Image();
  resizedImage.src = canvas.toDataURL();

  return resizedImage;
}

export const editorSlice = createSlice({
  name: 'editor',
  initialState: {
    gameInfos: getGameInfos(),
    currentGame: '',
    kaoData: [], // 用來放每個頭像的 base64 data
    selectedFace: null,
    modifiedFace: [],
    subFace: null, // 用來放替換頭像的 base64 data
  },
  reducers: {
    selectGame: (state, action) => {
      state.currentGame = action.payload;
      state.kaoData = [];
      state.selectedFace = null;
      state.modifiedFace = Array(1024).fill(false);
    },
    selectFace: (state, action) => {
      if (action.payload === state.selectedFace) {
        state.selectedFace = '';
      } else {
        state.selectedFace = action.payload;
      }
    },
    modifyFace: (state, action) => {
      state.modifiedFace = [
        ...state.modifiedFace.slice(0, action.payload),
        true,
        ...state.modifiedFace.slice(action.payload + 1),
      ];
    },
    clearModified: (state) => {
      state.modifiedFace = Array(1024).fill(false);
    },
    setKaoData: (state, action) => {
      state.kaoData = action.payload;
    },
    updateKao: (state, action) => {
      state.kaoData[action.payload.index] = action.payload.data;
    },
    updateSubFace: (state, action) => {
      const img = new Image();
      img.src = action.payload;
      const cvs = document.createElement('canvas');
      const ctx = cvs.getContext('2d');
      cvs.width = 64;
      cvs.height = 80;
      ctx.drawImage(img, 0, 0, 64, 80);
      // const scale = Math.max(64 / img.width, 80 / img.height);
      // const w = img.width * scale;
      // const h = img.height * scale;
      const resizedImage = resizeImage(img, 64, 80);
      // console.log('resizedImage size', w, h);
      // console.log('types 2: ', typeof action.payload, typeof resizedImage);

      // palette
      // let palette = [];
      // if (state.currentGame) {
      //   palette = state.gameInfos[state.currentGame].palette.map(hexToRgb);
      // }
      const palette = state.currentGame ?
        state.gameInfos[state.currentGame].palette.map(hexToRgb) :
        [
          '#000000',
          '#55FF55',
          '#FF5555',
          '#FFFF55',
          '#5555FF',
          '#55FFFF',
          '#FF55FF',
          '#FFFFFF',
        ].map(hexToRgb);

      // rgb quant
      const opts = {
        colors: 8,
        method: 1,
        dithKern: 'Atkinson',
        palette: palette,
      };
      const q = new RgbQuant(opts);
      state.subFace = q.reduce(resizedImage);
    },
  },
});

// Action creators are generated for each case reducer function
export const {
  setGameInfos,
  selectGame,
  selectFace,
  modifyFace,
  clearModified,
  setKaoData,
  updateKao,
  updateSubFace,
} = editorSlice.actions;

export default editorSlice.reducer;
