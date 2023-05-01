import PropTypes from 'prop-types';
import React, {useState} from 'react';
import {useDispatch} from 'react-redux';

import palettes from '../data/palettes';
import {applyPalette} from '../reducers';

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
  const [showHex, setShowHex] = useState(false);
  const [hexValue, setHexValue] = useState('#000000');
  const [selectedPreset, setSelectedPreset] = useState(
      Object.keys(palettes)[0],
  );
  const [colors, setColors] = useState(palettes[selectedPreset].codes);

  const dispatch = useDispatch();

  const handlePresetChange = (e) => {
    const presetKey = e.target.value;
    setSelectedPreset(presetKey);
    setColors(palettes[presetKey].codes);
    dispatch(applyPalette(presetKey, palettes[presetKey].codes));
  };

  const handleReset = () => {
    const defaultPreset = Object.keys(presets)[0];
    setSelectedPreset(defaultPreset);
    setColors(presets[defaultPreset]);
    dispatch(applyPalette(defaultPreset, palettes[defaultPreset].codes));
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
      <select value={selectedPreset} onChange={handlePresetChange}>
        {presetOptions}
      </select>
      <button onClick={handleReset}>Reset</button>
      <br />
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
    </div>
  );
}
