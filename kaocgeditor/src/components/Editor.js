import PropTypes from 'prop-types';
import React, {useState} from 'react';
import {useTranslation} from 'react-i18next';

import '../styles/Editor.css';
import BenchPlayer from './BenchPlayer.js';
import CreditInfo from './CreditInfo.js';
import FaceFigureContainer from './FaceFigureContainer.js';
import Settings from './Settings.js';
import UploadImage from './UploadImage.js';

function DithKernSelect({options, onChange}) {
  return (
    <select onChange={onChange}>
      {options.map((value) => (
        <option key={value} value={value}>
          {value}
        </option>
      ))}
    </select>
  );
}
DithKernSelect.propTypes = {
  options: PropTypes.arrayOf(PropTypes.string).isRequired,
  onChange: PropTypes.func.isRequired,
};

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
  const [dithKern, setDithKern] = useState('FloydSteinberg');
  const {t} = useTranslation();

  const handleDithKernSelectChange = (event) => {
    setDithKern(event.target.value);
  };

  const dithKernList = [
    'None',
    'FloydSteinberg',
    'FalseFloydSteinberg',
    'Stucki',
    'Atkinson',
    'Jarvis',
    'Burkes',
    'Sierra',
    'TwoSierra',
    'SierraLite',
  ];

  return (
    <div className="container">
      <div className="grid-container parent">
        <div className="locale">
          <LanguageSelect className="locale" />
        </div>
        <Settings />
        <div className="configuration outline-block child">
          <div className="tab-label">{t('tabs.color')}</div>
          <span>抖色演算法：</span>
          <DithKernSelect
            options={dithKernList}
            onChange={handleDithKernSelectChange}
          />
          {/* <ColorPalette /> */}
        </div>
        <div className="preview outline-block">
          <div className="tab-label">{t('tabs.substitute')}</div>
          <UploadImage dithKern={dithKern} setSubFace={setSubFace} />
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
