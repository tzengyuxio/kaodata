import PropTypes from 'prop-types';
import React, {useState} from 'react';

import {SubstitudeImage, cropImgToImageData} from '../utils';

function UploadImage(props) {
  const [imageFile, setImageFile] = useState(null);
  const [image, setImage] = useState(null); // drag-and-drop 的圖片

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
        // reader.result is DataURL, 'data:image/png;base64,...'
        setImage(reader.result);
        generateKao(reader.result, 64, 80);
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

  function generateKao(dataURL, width, height) {
    const img = new Image();

    // 加載圖像
    img.onload = function() {
      // Determine new dimensions within max size
      const ratio = Math.min(img.width / width, img.height / height);
      const sw = width * ratio; // 原圖要裁下的寬度
      const sh = height * ratio; // 原圖要裁下的高度
      const sx = (img.width - sw) / 2;
      const sy = (img.height - sh) / 2;

      const imageData = cropImgToImageData(
          img,
          sx,
          sy,
          sw,
          sh,
          0,
          0,
          width,
          height,
      );
      const imageDataHH = cropImgToImageData(
          img,
          sx,
          sy,
          sw,
          sh,
          0,
          0,
          width,
          height/2,
      );

      const simg = new SubstitudeImage(imageData, imageDataHH);
      props.setSubImage(simg);
    };

    // 設置圖像源
    img.src = dataURL;
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
  setSubImage: PropTypes.func.isRequired,
};

export default UploadImage;
