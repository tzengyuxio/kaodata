import {createSlice} from '@reduxjs/toolkit';
import getGameInfos from './data/gameData';

export const editorSlice = createSlice({
  name: 'editor',
  initialState: {
    gameInfos: getGameInfos(),
    currentGame: '',
    kaoData: [], // 用來放每個頭像的 base64 data
    selectedFace: null,
    modifiedFace: [],
    subFace: null, // 用來放替換頭像的 base64 data
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
} = editorSlice.actions;

export default editorSlice.reducer;
