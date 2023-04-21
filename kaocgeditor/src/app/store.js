import { configureStore } from '@reduxjs/toolkit';
import editorReducer from '../reducers.js';

export const store = configureStore({
  reducer: {
    editor: editorReducer,
  },
})