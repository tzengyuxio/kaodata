import React, {useState, useEffect} from 'react';
// import {useDispatch} from 'react-redux';
// import {updateSubFace} from '../reducers.js';
import PropTypes from 'prop-types';
import {hexToRgb, imageUrlToKaoImage} from '../utils';
import {useSelector} from 'react-redux';

function UploadImage(props) {
  const [imageFile, setImageFile] = useState(null);
  // const dispatch = useDispatch();
  const gameInfos = useSelector((state) => state.editor.gameInfos);
  const currentGame = useSelector((state) => state.editor.currentGame);
  let palette = [
    '#000000',
    '#55FF55',
    '#FF5555',
    '#FFFF55',
    '#5555FF',
    '#55FFFF',
    '#FF55FF',
    '#FFFFFF',
  ];
  if (gameInfos[currentGame]) {
    palette = gameInfos[currentGame].palette;
  }

  useEffect(() => {
    if (!props.image) {
      return;
    }
    const newImageData = imageUrlToKaoImage(
        props.image,
        64,
        80,
        palette.map(hexToRgb),
    );
    props.setSubFace(newImageData);
  }, [props.image]);

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
        props.setImage(reader.result);
        // dispatch(updateSubFace(reader.result));
        // reader.result is ArrayBuffer
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
        {props.image && (
          <img
            src={URL.createObjectURL(imageFile)}
            alt="uploaded"
            width="100%"
            height="100%"
          />
        )}
        {!props.image && (
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
  image: PropTypes.string,
  setImage: PropTypes.func.isRequired,
  setSubFace: PropTypes.func.isRequired,
};

export default UploadImage;
