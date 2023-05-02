import React from 'react';
import {useTranslation} from 'react-i18next';
import {useDispatch} from 'react-redux';

import {setDithKern} from '../reducers';

export default function DithKernSelect() {
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
