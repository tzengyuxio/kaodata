import PropTypes from 'prop-types';
import React, {useEffect, useState} from 'react';
import {useSelector} from 'react-redux';
import RgbQuant from 'rgbquant';

import palettes from '../data/palettes';
import {hexToRgb, usedColorsOfImageData} from '../utils';

function UploadImage(props) {
  const [imageFile, setImageFile] = useState(null);
  const [image, setImage] = useState(null); // drag-and-drop 的圖片
  const [resizedImage, setResizedImage] = useState(null); // 調整大小後的圖片
  const currentGame = useSelector((state) => state.editor.currentGame);
  const dithKern = useSelector((state) => state.editor.dithKern);
  const gameInfos = useSelector((state) => state.editor.gameInfos);

  const palette = gameInfos[currentGame] ?
        gameInfos[currentGame].palette.codes.map(hexToRgb) :
        palettes.default.codes.map(hexToRgb);

  useEffect(() => {
    console.log('useEffect: currentGame changed to [' + currentGame + ']');
    resizeImage(resizedImage, 64, 80, palette, false);
  }, [currentGame]);

  useEffect(() => {
    console.log('useEffect: dithKern changed', dithKern);
    resizeImage(resizedImage, 64, 80, palette, false);
  }, [dithKern]);

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
        resizeImage(reader.result, 64, 80, palette, true);
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

  function resizeImage(fileResult, newWidth, newHeight, palette, needSave) {
    const img = new Image();

    img.onload = function() {
      // Determine new dimensions within max size
      const ratio = Math.min(
          img.width / newWidth,
          img.height / newHeight,
      );
      const width = ratio === 1 ? img.width : newWidth * ratio;
      const height = ratio === 1 ? img.height : newHeight * ratio;
      const sx = (img.width - width) / 2;
      const sy = (img.height - height) / 2;

      // Draw image on canvas
      const canvas = document.createElement('canvas');
      canvas.width = newWidth;
      canvas.height = newHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(
          img,
          sx,
          sy,
          width,
          height,
          0,
          0,
          newWidth,
          newHeight,
      );

      // Get resized image data
      const imageData = ctx.getImageData(0, 0, newWidth, newHeight);
      if (needSave) {
        // NOTE: resizedImage 是否可改用 imageData? 是的話最後 img.src 要怎麼改?
        setResizedImage(canvas.toDataURL('image/png'));
      }

      // used colors of imageData
      const usedColors = usedColorsOfImageData(imageData);
      console.log('usedColors', usedColors);

      // Rgb Quant
      const opts = {
        colors: 8,
        method: 2, // histogram method
        boxSize: [4, 4], // if method = 2
        boxPxls: 0.1, // if method = 2
        initColors: 32, // if method = 1
        dithKern: dithKern === 'None' ? null : dithKern,
        dithDelta: 0.1,
        palette: palette,
        // palette: palettes.default.codes.map(hexToRgb),
      };

      const q = new RgbQuant(opts);
      // q.sample(imageData);
      const out = q.reduce(imageData);
      const carr = new Uint8ClampedArray(out.buffer);
      const newImageData = new ImageData(carr, newWidth, newHeight);

      props.setSubFace(newImageData);
    };

    img.src = fileResult;
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
