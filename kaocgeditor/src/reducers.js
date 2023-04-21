import {createSlice} from '@reduxjs/toolkit';

export const editorSlice = createSlice({
  name: 'editor',
  initialState: {
    gameInfos: {},
    currentGame: '',
    selectedFace: '',
    modifiedFace: [],
  },
  reducers: {
    selectGame: (state, action) => {
      state.currentGame = action.payload;
    },
    selectFace: (state) => {},
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
  },
});

// Action creators are generated for each case reducer function
export const {selectGame, selectFace, modifyFace, clearModified} =
  editorSlice.actions;

export default editorSlice.reducer;
