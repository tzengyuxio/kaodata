import {createSlice} from '@reduxjs/toolkit';

export const editorSlice = createSlice({
  name: 'editor',
  initialState: {
    gameInfos: {},
    currentGame: '',
    kaoData: [], // 用來放每個頭像的 base64 data
    selectedFace: null,
    modifiedFace: [],
  },
  reducers: {
    selectGame: (state, action) => {
      state.currentGame = action.payload;
      state.kaoData = [];
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
export const {selectGame, selectFace, modifyFace, clearModified, setKaoData} =
  editorSlice.actions;

export default editorSlice.reducer;
