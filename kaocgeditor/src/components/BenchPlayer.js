import PropTypes from 'prop-types';
import React, {useEffect, useState} from 'react';
import {useTranslation} from 'react-i18next';
import {useDispatch, useSelector} from 'react-redux';

import {base64EncArr} from '../base64.js';
import palettes from '../data/palettes.js';
import {modifyFace, updateKao} from '../reducers';
import {hexToRgb} from '../utils';

/**
 * 可替補上場的頭像，一個包含圖片和「替換」按鈕的 React 組件。
 * 相對於出廠預設的先發頭像，角色類似於「替補」或「板凳球員」。
 * @param {Object} props - 組件的屬性。
 * @param {function} props.onSubButtonClick - img 元素重繪完成後需要執行的回調函數。
 * @return {JSX.Element} BenchPlayer 組件。
 */
function BenchPlayer(props) {
  const [imageUrl, setImageUrl] = useState(null);
  const [isSubButtonDisabled, setIsSubButtonDisabled] = useState(true);
  const dispatch = useDispatch();
  const selectedIndex = useSelector((state) => state.editor.selectedFace);
  const gameInfo = useSelector((state) => {
    const info = state.editor.gameInfos[state.editor.currentGame];
    return info ? info : null;
  });
  const colors = gameInfo ?
        gameInfo.palette.codes.map(hexToRgb) :
        palettes.default.codes.map(hexToRgb);
  const halfHeight = gameInfo ? gameInfo.halfHeight : false;
  const paletteId = useSelector((state) => state.editor.paletteId);
  const {t} = useTranslation();

  useEffect(() => {
    if (props.subImage) {
      const newImageData = props.subImage.applyPalette(
          palettes[paletteId].codes.map(hexToRgb),
          halfHeight,
      );
      const canvas = document.createElement('canvas');
      canvas.width = props.subImage.imageData.width;
      canvas.height = props.subImage.imageData.height;
      const ctx = canvas.getContext('2d');
      ctx.putImageData(newImageData, 0, 0);
      const url = canvas.toDataURL();
      setImageUrl(url);
      setIsSubButtonDisabled(false);
    } else {
      console.log('useEffect: props.subFace is null');
    }
  }, [paletteId, props.subImage]);

  const handleSubButtonClick = () => {
    dispatch(modifyFace(selectedIndex));
    // copy self image to selected face
    const kaoData = base64EncArr(
        props.subImage.getFaceData(colors, halfHeight),
    );
    dispatch(
        updateKao({index: selectedIndex, kao: kaoData, url: imageUrl}),
    );
  };

  return (
    <div className="bench-player">
      {imageUrl && (
        <img src={imageUrl} alt="image" className="bench-player-img" />
      )}
      {!imageUrl && <div className="bench-player-box"></div>}
      <button
        className="sub-button"
        disabled={isSubButtonDisabled || selectedIndex < 0}
        onClick={handleSubButtonClick}
      >
        {t('buttons.substitute')}
      </button>
    </div>
  );
}
BenchPlayer.propTypes = {
  subImage: PropTypes.object,
};

export default BenchPlayer;
