import {createSlice} from '@reduxjs/toolkit';

import getGameInfos from './data/gameInfos';
import palettes from './data/palettes';

export const editorSlice = createSlice({
  name: 'editor',
  initialState: {
    gameInfos: getGameInfos(),
    currentGame: '',
    fileLoaded: false,
    kaoData: [], // 用來放每個頭像(koei 8色編碼, 960 or 1920 bytes)的 base64 data
    kaoImgUrl: [], // 用來放每個頭像的 img url
    selectedFace: -1,
    modifiedFace: [],
    dithKern: 'None',
    paletteId: palettes.default.id,
  },
  reducers: {
    selectGame: (state, action) => {
      state.currentGame = action.payload;
      state.selectedFace = -1;
      state.fileLoaded = false;
      const gameInfo = state.gameInfos[action.payload];
      const faceCount = gameInfo ? gameInfo.faceNames.length : 0;
      state.modifiedFace = Array(faceCount).fill(false);
      state.kaoImgUrl.map((url) => URL.revokeObjectURL(url));
      state.kaoData = Array(faceCount).fill('');
      state.kaoImgUrl = Array(faceCount).fill('');
      state.paletteId = gameInfo ?
                gameInfo.palette.id :
                palettes.default.id;
    },
    selectFace: (state, action) => {
      if (action.payload === state.selectedFace) {
        state.selectedFace = -1;
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
    updateKao: (state, action) => {
      state.kaoData[action.payload.index] = action.payload.kao;
      state.kaoImgUrl[action.payload.index] = action.payload.url;
    },
    loadFileDone: (state) => {
      state.fileLoaded = true;
    },
    applyPalette: (state, action) => {
      // do nothing
    },
    setDithKern: (state, action) => {
      state.dithKern = action.payload;
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
  updateKao,
  loadFileDone,
  applyPalette,
  setDithKern,
} = editorSlice.actions;

export default editorSlice.reducer;
