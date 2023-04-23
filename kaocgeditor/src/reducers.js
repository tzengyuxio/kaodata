import {createSlice} from '@reduxjs/toolkit';
import getGameInfos from './data/gameData';

export const editorSlice = createSlice({
  name: 'editor',
  initialState: {
    gameInfos: getGameInfos(),
    currentGame: '',
    fileLoaded: false,
    kaoData: [], // 用來放每個頭像的 base64 data
    kaoImgUrl: [], // 用來放每個頭像的 img url
    selectedFace: -1,
    modifiedFace: [],
    defaultPalette: [
      '#000000',
      '#55FF55',
      '#FF5555',
      '#FFFF55',
      '#5555FF',
      '#55FFFF',
      '#FF55FF',
      '#FFFFFF',
    ],
  },
  reducers: {
    selectGame: (state, action) => {
      state.currentGame = action.payload;
      state.selectedFace = null;
      state.fileLoaded = false;
      const gameInfo = state.gameInfos[action.payload];
      const faceCount = gameInfo ? gameInfo.names.length : 0;
      state.modifiedFace = Array(faceCount).fill(false);
      state.kaoData = Array(faceCount).fill('');
      state.kaoImgUrl = Array(faceCount).fill('');
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
    setKaoData: (state, action) => {
      state.kaoData = action.payload;
    },
    updateKao: (state, action) => {
      state.kaoData[action.payload.index] = action.payload.kao;
      state.kaoImgUrl[action.payload.index] = action.payload.url;
    },
    loadFileDone: (state) => {
      state.fileLoaded = true;
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
  loadFileDone,
} = editorSlice.actions;

export default editorSlice.reducer;
