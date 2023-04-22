import React, {useState} from 'react';
import PropTypes from 'prop-types';
import {hexToRgb} from '../utils';
import {useSelector} from 'react-redux';
import RgbQuant from 'rgbquant';

function resizeImage(fileResult, newWidth, newHeight, palette, setSubFace) {
  const img = new Image();

  img.onload = function() {
    // Determine new dimensions within max size
    const ratio = Math.min(img.width / newWidth, img.height / newHeight);
    const width = ratio === 1 ? img.width : newWidth * ratio;
    const height = ratio === 1 ? img.height : newHeight * ratio;
    const sx = (img.width - width) / 2;
    const sy = (img.height - height) / 2;

    // Draw image on canvas
    const canvas = document.createElement('canvas');
    canvas.width = newWidth;
    canvas.height = newHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, sx, sy, width, height, 0, 0, newWidth, newHeight);

    // Get new image data
    const imageData = ctx.getImageData(0, 0, newWidth, newHeight);

    const opts = {
      colors: 8,
      method: 1,
      dithKern: 'FloydSteinberg', // 'Atkinson',
      palette: palette,
    };

    const q = new RgbQuant(opts);
    const out = q.reduce(imageData);
    const carr = new Uint8ClampedArray(out.buffer);
    const newImageData = new ImageData(carr, newWidth, newHeight);

    setSubFace(newImageData);
  };

  img.src = fileResult;
}

function UploadImage(props) {
  const [imageFile, setImageFile] = useState(null);
  const [image, setImage] = useState(null); // drag-and-drop 的圖片
  const gameInfos = useSelector((state) => state.editor.gameInfos);
  const currentGame = useSelector((state) => state.editor.currentGame);

  const palette = gameInfos[currentGame] ?
    gameInfos[currentGame].palette.map(hexToRgb) :
    [
      '#000000',
      '#55FF55',
      '#FF5555',
      '#FFFF55',
      '#5555FF',
      '#55FFFF',
      '#FF55FF',
      '#FFFFFF',
    ].map(hexToRgb);

  function handleDrop(e) {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    setImageFile(file);
    handleFile(file);
  }

  function handleFile(file) {
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onloadend = () => {
        setImage(reader.result);
        resizeImage(reader.result, 64, 80, palette, props.setSubFace);
      };
    }
  }

  function handleButtonClick() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = (e) => {
      const file = e.target.files[0];
      setImageFile(file);
      handleFile(file);
    };
    input.click();
  }

  /**
   * Handle the drag over event.
   * @param {React.DragEvent<HTMLDivElement>} e The drag over event.
   * @return {void}
   */
  function handleDragOver(e) {
    e.preventDefault();
  }

  return (
    <div
      className="upload-container"
      id="drop-area"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
    >
      <div className="upload-image">
        {image && (
          <img
            src={URL.createObjectURL(imageFile)}
            alt="uploaded"
            width="100%"
            height="100%"
          />
        )}
        {!image && (
          <div className="upload-text">
            <p>拖放圖像到此區域或</p>
            <button onClick={handleButtonClick}>選擇圖像</button>
          </div>
        )}
      </div>
    </div>
  );
}
UploadImage.propTypes = {
  setSubFace: PropTypes.func.isRequired,
};

export default UploadImage;
