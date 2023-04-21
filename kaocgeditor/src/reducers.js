import { createSlice } from "@reduxjs/toolkit";

export const editorSlice = createSlice({
  name: "editor",
  initialState: {
    gameInfos: {},
    currentGame: "",
    selectedFace: "",
    modifiedFace: [],
  },
  reducers: {
    selectGame: (state, action) => {
        state.currentGame = action.payload;
    },
    selectFace: (state) => {},
    modifyFace: (state) => {},
  },
});

// Action creators are generated for each case reducer function
export const { selectGame, selectFace, modifyFace } = editorSlice.actions;

export default editorSlice.reducer;
