import React, {useState} from 'react';
import {useTranslation} from 'react-i18next';

import '../styles/Editor.css';
import BenchPlayer from './BenchPlayer.js';
import Configs from './Configs';
import CreditInfo from './CreditInfo.js';
import FaceFigureContainer from './FaceFigureContainer.js';
import Settings from './Settings.js';
import UploadImage from './UploadImage.js';

function LanguageSelect() {
  const {i18n} = useTranslation();
  const languages = [
    {id: 'zh_tw', name: '繁體中文'},
    {id: 'zh_cn', name: '简体中文'},
    {id: 'ja', name: '日本語'},
  ];
  return (
    <select onChange={(e) => i18n.changeLanguage(e.target.value)}>
      {languages.map((lang) => (
        <option key={lang.id} value={lang.id}>
          {lang.name}
        </option>
      ))}
    </select>
  );
}

function Editor() {
  const [subFace, setSubFace] = useState(null); // rgbQuant 的結果
  const {t} = useTranslation();

  return (
    <div className="container">
      <div className="grid-container parent">
        <div className="locale">
          <LanguageSelect className="locale" />
        </div>
        <Settings />
        <Configs />
        <div className="preview outline-block">
          <div className="tab-label">{t('tabs.substitute')}</div>
          <UploadImage setSubFace={setSubFace} />
                    →
          <BenchPlayer subFace={subFace} />
        </div>
        {/* <div className="grid-item one"></div> */}
        <CreditInfo />
      </div>
      <hr />
      <FaceFigureContainer />
      <div className="clipboard">
        <h2>Clipboard</h2>
        <div className="image-grid"></div>
        <button className="copy">Copy</button>
        <button className="cut">Cut</button>
      </div>
    </div>
  );
}

export default Editor;
