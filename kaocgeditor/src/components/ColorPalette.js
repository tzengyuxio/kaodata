import React, {useState} from 'react';
import {useDispatch} from 'react-redux';

import palettes from '../data/palettes';
import {applyPalette} from '../reducers';

export default function ColorPalette() {
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

  const handleColorChange = (index, e) => {
    const updatedColors = [...colors];
    updatedColors[index] = e.target.value;
    setColors(updatedColors);
  };

  const handleReset = () => {
    const defaultPreset = Object.keys(presets)[0];
    setSelectedPreset(defaultPreset);
    setColors(presets[defaultPreset]);
    dispatch(applyPalette(defaultPreset, palettes[defaultPreset].codes));
  };

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
        <input
          type="color"
          value={color}
          disabled
          onChange={(e) => handleColorChange(index, e)}
        />
        {(index + 1) % 4 === 0 && <br />}
      </React.Fragment>
    );
  });

  return (
    <div>
      <select value={selectedPreset} onChange={handlePresetChange}>
        {presetOptions}
      </select>
      <button onClick={handleReset}>Reset</button>
      <br />
      {colorInputs}
    </div>
  );
}
