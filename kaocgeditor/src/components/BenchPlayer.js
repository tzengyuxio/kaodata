import React, {useState, useEffect} from 'react';
import PropTypes from 'prop-types';

/**
 * 可替補上場的頭像，一個包含圖片和「替換」按鈕的 React 組件。
 * 相對於出廠預設的先發頭像，角色類似於「替補」或「板凳球員」。
 * @param {Object} props - 組件的屬性。
 * @param {ImageData} props.imageData - 用於繪製圖片的數據。
 * @param {function} props.onSubButtonClick - img 元素重繪完成後需要執行的回調函數。
 * @return {JSX.Element} ImageWithButton 組件。
 */
function BenchPlayer({imageData, onSubButtonClick}) {
  const [imageUrl, setImageUrl] = useState(null);
  const [isSubButtonDisabled, setIsSubButtonDisabled] = useState(true);

  useEffect(() => {
    if (imageData) {
      setImageUrl(URL.createObjectURL(imageData));
      setIsSubButtonDisabled(false);
    }
  }, [imageData]);

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
  imageData: PropTypes.object.isRequired,
  onSubButtonClick: PropTypes.func.isRequired,
};

export default BenchPlayer;
