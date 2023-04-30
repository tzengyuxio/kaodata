import React from 'react';
import ReactGA from 'react-ga4';
import {useTranslation} from 'react-i18next';

import './App.css';
import Editor from './components/Editor';

ReactGA.initialize('G-1HF0Q4W96B');

function App() {
  const {t} = useTranslation();
  return (
    <div>
      <h2>{t('title')}</h2>
      <Editor />
    </div>
  );
}

export default App;
