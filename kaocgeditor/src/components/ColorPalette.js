import PropTypes from 'prop-types';
import React, {useEffect, useState} from 'react';
import {useTranslation} from 'react-i18next';
import {useDispatch, useSelector} from 'react-redux';

import palettes from '../data/palettes';
import {setPaletteId} from '../reducers';

function ColorPicker(props) {
  const elementId = 'hexValue';

  const handleColorChange = (index, e) => {
    const updatedColors = [...colors];
    updatedColors[index] = e.target.value;
    setColors(updatedColors);
  };

  function handleMouseEnter(event) {
    const hex = event.target.value;
    const x = event.clientX;
    const y = event.clientY;
    props.setHexValue(hex);
    props.setShowHex(true);
    const hexElement = document.getElementById(elementId);
    hexElement.style.display = 'block';
    hexElement.style.position = 'fixed';
    hexElement.style.top = y - 36 + 'px';
    hexElement.style.left = x - 36 + 'px';
  }

  return (
    <div
      style={{display: 'inline-block', margin: '1px'}}
      onMouseMove={handleMouseEnter}
    >
      <input
        type="color"
        value={props.color}
        disabled
        style={{opacity: 100}}
        onChange={(e) => handleColorChange(index, e)}
      />
    </div>
  );
}
ColorPicker.propTypes = {
  index: PropTypes.number,
  color: PropTypes.string,
  setHexValue: PropTypes.func,
  setShowHex: PropTypes.func,
};

export default function ColorPalette() {
  const dispatch = useDispatch();
  const [showHex, setShowHex] = useState(false);
  const [hexValue, setHexValue] = useState('#000000');
  const [selectedPreset, setSelectedPreset] = useState(
      Object.keys(palettes)[0],
  );
  const [colors, setColors] = useState(palettes[selectedPreset].codes);
  const paletteId = useSelector((state) => state.editor.paletteId);
  const {t} = useTranslation();

  useEffect(() => {
    setSelectedPreset(paletteId);
    setColors(palettes[paletteId].codes);
  }, [paletteId]);

  const handlePresetChange = (e) => {
    dispatch(setPaletteId(e.target.value));
  };

  const handleReset = () => {
    dispatch(setPaletteId());
  };

  function handleMouseLeave() {
    setShowHex(false);
    const elementId = 'hexValue';
    const hexElement = document.getElementById(elementId);
    hexElement.style.display = 'none';
    console.log('handleMouseOut', elementId);
  }

  const presetOptions = Object.keys(palettes).map((presetKey) => {
    return (
      <option key={presetKey} value={presetKey}>
        {palettes[presetKey].name}
      </option>
    );
  });

  const colorInputs = colors.map((color, index) => {
    return (
      <React.Fragment key={index}>
        <ColorPicker
          index={index}
          color={color}
          setHexValue={setHexValue}
          setShowHex={setShowHex}
        />
        {(index + 1) % 4 === 0 && <br />}
      </React.Fragment>
    );
  });

  return (
    <div className="color-palette">
      <div onMouseLeave={handleMouseLeave}>{colorInputs}</div>
      <div
        id="hexValue"
        style={{
          display: showHex ? 'block' : 'none',
          position: 'absolute',
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          color: 'white',
          padding: '5px',
          borderRadius: '5px',
          fontSize: '14px',
        }}
      >
        {hexValue.toUpperCase()}
      </div>
      <br />
      <select value={selectedPreset} onChange={handlePresetChange}>
        {presetOptions}
      </select>
      <button onClick={handleReset} style={{marginLeft: '8px'}}>
        {t('buttons.reset')}
      </button>
    </div>
  );
}
