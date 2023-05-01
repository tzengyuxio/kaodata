import React from 'react';
import {useTranslation} from 'react-i18next';
import {useDispatch} from 'react-redux';

import {setDithKern} from '../reducers';
import TabLabel from './TabLabel';

function DithKernSelect() {
  const dispatch = useDispatch();
  const {t} = useTranslation();
  const handleDithKernSelectChange = (e) => {
    dispatch(setDithKern(e.target.value));
  };

  const dithKernList = [
    'None',
    'FloydSteinberg',
    // 'FalseFloydSteinberg',
    'Stucki',
    'Atkinson',
    'Jarvis',
    'Burkes',
    'Sierra',
    'TwoSierra',
    'SierraLite',
  ];

  return (
    <div>
      <label htmlFor="dithKernSelect">{t('label.dith-kern')}</label>
      <select id="dithKernSelect" onChange={handleDithKernSelectChange}>
        {dithKernList.map((value) => (
          <option key={value} value={value}>
            {value}
          </option>
        ))}
      </select>
    </div>
  );
}

export default function Configs() {
  return (
    <div className="configuration outline-block child">
      <TabLabel labelKey="tabs.color" />
      <DithKernSelect />
      {/* <ColorPalette /> */}
    </div>
  );
}
