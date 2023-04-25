import React from 'react';
import ReactGA from 'react-ga4';

import './App.css';
import Editor from './components/Editor';

ReactGA.initialize('G-1HF0Q4W96B');

function App() {
  return (
    <div>
      <h2>顏ＣＧ編輯器</h2>
      <Editor />
    </div>
  );
}

export default App;
