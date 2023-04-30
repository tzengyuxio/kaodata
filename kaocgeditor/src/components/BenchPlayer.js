import PropTypes from 'prop-types';
import React, {useEffect, useState} from 'react';
import {useTranslation} from 'react-i18next';
import {useDispatch, useSelector} from 'react-redux';

import {base64EncArr} from '../base64.js';
import palettes from '../data/palettes.js';
import {modifyFace, updateKao} from '../reducers';
import {hexToRgb, imageToData} from '../utils';

/**
 * 可替補上場的頭像，一個包含圖片和「替換」按鈕的 React 組件。
 * 相對於出廠預設的先發頭像，角色類似於「替補」或「板凳球員」。
 * @param {Object} props - 組件的屬性。
 * @param {Blob} props.image - 從遊戲中讀取的圖片。
 * @param {function} props.onSubButtonClick - img 元素重繪完成後需要執行的回調函數。
 * @return {JSX.Element} BenchPlayer 組件。
 */
function BenchPlayer(props) {
  const [imageUrl, setImageUrl] = useState(null);
  const [isSubButtonDisabled, setIsSubButtonDisabled] = useState(true);
  const dispatch = useDispatch();
  const selectedIndex = useSelector((state) => state.editor.selectedFace);
  const colors = useSelector((state) => {
    const info = state.editor.gameInfos[state.editor.currentGame];
    return info ?
            info.palette.map(hexToRgb) :
            palettes.default.codes.map(hexToRgb);
  });
  const {t} = useTranslation();

  useEffect(() => {
    if (props.subFace) {
      const canvas = document.createElement('canvas');
      canvas.width = props.subFace.width;
      canvas.height = props.subFace.height;
      const ctx = canvas.getContext('2d');
      ctx.putImageData(props.subFace, 0, 0);
      const url = canvas.toDataURL();
      setImageUrl(url);
      setIsSubButtonDisabled(false);
    } else {
      console.log('useEffect: props.subFace is null');
    }
  }, [props.subFace]);

  const handleSubButtonClick = () => {
    dispatch(modifyFace(selectedIndex));
    // copy self image to selected face
    const faceData = imageToData(props.subFace, colors);
    dispatch(
        updateKao({
          index: selectedIndex,
          kao: base64EncArr(faceData),
          url: imageUrl,
        }),
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
        {t('button.substitute')}
      </button>
    </div>
  );
}
BenchPlayer.propTypes = {
  image: PropTypes.string,
  subFace: PropTypes.object,
};

export default BenchPlayer;
