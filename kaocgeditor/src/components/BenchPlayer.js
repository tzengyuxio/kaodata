import React, {useState, useEffect} from 'react';
import PropTypes from 'prop-types';

/**
 * 可替補上場的頭像，一個包含圖片和「替換」按鈕的 React 組件。
 * 相對於出廠預設的先發頭像，角色類似於「替補」或「板凳球員」。
 * @param {Object} props - 組件的屬性。
 * @param {Blob} props.image - 從遊戲中讀取的圖片。
 * @param {function} props.onSubButtonClick - img 元素重繪完成後需要執行的回調函數。
 * @return {JSX.Element} ImageWithButton 組件。
 */
function BenchPlayer(props) {
  const [imageUrl, setImageUrl] = useState(null);
  const [isSubButtonDisabled, setIsSubButtonDisabled] = useState(true);

  useEffect(() => {
    if (props.subFace) {
      console.log('useEffect: props.subFace has value');
      const canvas = document.createElement('canvas');
      canvas.width = props.subFace.width;
      canvas.height = props.subFace.height;
      const ctx = canvas.getContext('2d');
      ctx.putImageData(props.subFace, 0, 0);
      const url = canvas.toDataURL();
      if (url.length < 512) {
        console.log('url too short: ', url.length, props.subFace);
      } else {
        console.log('url size: ', url.length, props.subFace);
      }
      setImageUrl(url);
      setIsSubButtonDisabled(false);
    } else {
      console.log('useEffect: props.subFace is null');
    }
  }, [props.subFace]);

  const handleSubButtonClick = () => {
    onSubButtonClick();
    // copy self image to selected face
  };

  return (
    <div className="bench-player">
      {imageUrl && (
        <img src={imageUrl} alt="image" className="bench-player-img" />
      )}
      {!imageUrl && <div className="bench-player-box"></div>}
      <button
        className="sub-button"
        disabled={isSubButtonDisabled}
        onClick={handleSubButtonClick}
      >
        替補
      </button>
    </div>
  );
}
BenchPlayer.propTypes = {
  image: PropTypes.string,
  subFace: PropTypes.object,
  onSubButtonClick: PropTypes.func.isRequired,
};

export default BenchPlayer;
