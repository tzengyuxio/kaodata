import React, {useState, useEffect} from 'react';
import getGameInfos from '../data/gameData.js';
import {dataToImage, hexToRgb} from '../utils.js';
import '../styles/Editor.css';
import UploadImage from './UploadImage.js';
import {useDispatch, useSelector} from 'react-redux';
import {
  selectGame,
  clearModified,
  selectFace,
  setKaoData,
} from '../reducers.js';
import PropTypes from 'prop-types';
import BenchPlayer from './BenchPlayer.js';
import {base64DecToArr, base64EncArr} from '../base64.js';

function GameSelect(props) {
  const dispatch = useDispatch();
  const handleChange = (e) => {
    const gameId = e.target.value;
    dispatch(selectGame(gameId));
    props.setUploadBtnDisabled(false);
  };
  return (
    <select id="game-select" onChange={handleChange}>
      <option value="">--選擇遊戲--</option>
      {props.gameList.map((game) => (
        <option key={game.id} value={game.id}>
          {game.name}
        </option>
      ))}
    </select>
  );
}
GameSelect.propTypes = {
  gameList: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.string.isRequired,
        name: PropTypes.string.isRequired,
      }),
  ).isRequired,
  setUploadBtnDisabled: PropTypes.func.isRequired,
};

function DithKernSelect({options, onChange}) {
  return (
    <select onChange={onChange}>
      {options.map((value) => (
        <option key={value} value={value}>
          {value}
        </option>
      ))}
    </select>
  );
}
DithKernSelect.propTypes = {
  options: PropTypes.arrayOf(PropTypes.string).isRequired,
  onChange: PropTypes.func.isRequired,
};

function ImageFigure(props) {
  const [imgUrl, setImgUrl] = useState(null);

  useEffect(() => {
    const canvas = document.createElement('canvas');
    canvas.width = props.imageData.width;
    canvas.height = props.imageData.height;
    const ctx = canvas.getContext('2d');
    ctx.putImageData(props.imageData, 0, 0);
    canvas.toBlob((blob) => {
      const url = URL.createObjectURL(blob);
      setImgUrl(url);
    });
  }, [props.imageData]);

  const faceIndex = props.imageKey + 1;

  const currentGame = useSelector((state) => state.editor.currentGame);
  const names = getGameInfos()[currentGame].names;
  const name =
    names[props.imageKey] === '' ? '(未命名)' : names[props.imageKey];

  console.log('Rendering ImageFigure');
  return (
    <figure
      id={`face-${props.imageKey + 1}`}
      className={`image-figure ${props.selected ? 'selected' : ''} ${
        props.modified ? 'modified' : ''
      }`}
      onClick={props.onClick}
    >
      {imgUrl && <img src={imgUrl} alt={`Image ${faceIndex}`} />}
      <figcaption>
        {faceIndex}
        <br />
        {name}
      </figcaption>
    </figure>
  );
}
ImageFigure.propTypes = {
  imageKey: PropTypes.number.isRequired,
  imageData: PropTypes.object.isRequired,
  selected: PropTypes.bool.isRequired,
  modified: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired,
};

function FaceList() {
  const dispatch = useDispatch();

  const handleFigureClick = (e, index) => {
    e.stopPropagation();
    dispatch(selectFace(index));
  };

  const selectedIndex = useSelector((state) => state.editor.selectedFace);
  const modified = useSelector((state) => state.editor.modifiedFace);
  const kaoData = useSelector((state) => state.editor.kaoData);

  const currentGame = useSelector((state) => state.editor.currentGame);
  let theGame = null;
  let colors = [];
  let width = -1;
  let height = -1;
  let halfHeight = false;
  if (currentGame !== '') {
    theGame = getGameInfos()[currentGame];
    colors = theGame.palette.map(hexToRgb);
    width = theGame.width;
    height = theGame.height;
    halfHeight = theGame.halfHeight;
  }

  if (kaoData.length === 0) {
    return (
      <div className="image-list" id="image-list">
        請先選擇遊戲，並上傳檔案
      </div>
    );
  }
  const imgDataArray = kaoData.map((kao) => {
    const buffer = base64DecToArr(kao);
    return dataToImage(buffer, width, height, colors, halfHeight);
  });
  return (
    <div className="image-list">
      <br />
      {imgDataArray.map((imageData, index) => (
        <ImageFigure
          key={index}
          imageKey={index}
          imageData={imageData}
          selected={selectedIndex === index}
          modified={modified[index]}
          onClick={(e) => handleFigureClick(e, index)}
        ></ImageFigure>
      ))}
    </div>
  );
}

function Save({disabled, onClick}) {
  return (
    <button className="save-btn" disabled={disabled} onClick={onClick}>
      Save
    </button>
  );
}
Save.propTypes = {
  disabled: PropTypes.bool,
  onClick: PropTypes.func,
};

function Editor() {
  const [gameList, setGameList] = useState([]);
  const [UploadBtnDisabled, setUploadBtnDisabled] = useState(true);
  const [subFace, setSubFace] = useState(null); // rgbQuant 的結果
  const [dithKern, setDithKern] = useState('FloydSteinberg');
  const dispatch = useDispatch();

  useEffect(() => {
    // 從 gameData.js 文件中取得遊戲數據
    const gameInfos = getGameInfos();
    // 根據數據建立選項
    const list = Object.values(gameInfos).map((game) => ({
      id: game.id,
      name: game.name,
    }));
    setGameList(list);
  }, []);

  const currentGame = useSelector((state) => state.editor.currentGame);
  const theGame = getGameInfos()[currentGame];

  const handleFileSelected = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.readAsArrayBuffer(file);
    reader.onload = (event) => {
      const uint8Buffer = new Uint8Array(event.target.result);

      // prepare KaoDataArray
      const faceDataSize = theGame.halfHeight ?
        (theGame.width * theGame.height * 3) / 8 / 2 :
        (theGame.width * theGame.height * 3) / 8;

      const faceCount =
        theGame.count === -1 ?
          Math.floor(uint8Buffer.byteLength / faceDataSize) :
          theGame.count;

      const kaoDataArray = new Array(faceCount);
      for (let i = 0; i < faceCount; i++) {
        const faceData = uint8Buffer.slice(
            i * faceDataSize,
            (i + 1) * faceDataSize,
        );
        kaoDataArray[i] = base64EncArr(faceData);
      }
      dispatch(setKaoData(kaoDataArray));
    };
  };

  const handleSaveClick = () => {
    dispatch(clearModified());
    dispatch(selectFace(null));
  };

  const handleDithKernSelectChange = (event) => {
    setDithKern(event.target.value);
  };

  const modified = useSelector((state) => state.editor.modifiedFace);
  const dithKernList = [
    'FloydSteinberg',
    'FalseFloydSteinberg',
    'Stucki',
    'Atkinson',
    'Jarvis',
    'Burkes',
    'Sierra',
    'TwoSierra',
    'SierraLite',
  ];

  return (
    <div className="container">
      <div className="settings">
        <GameSelect
          gameList={gameList}
          setUploadBtnDisabled={setUploadBtnDisabled}
        ></GameSelect>
        <input
          type="file"
          disabled={UploadBtnDisabled}
          onChange={handleFileSelected}
          //   accept="image/*"
        />
        <DithKernSelect
          options={dithKernList}
          onChange={handleDithKernSelectChange}
        />
      </div>
      <div className="preview">
        <UploadImage dithKern={dithKern} setSubFace={setSubFace} />
        →
        <BenchPlayer subFace={subFace} />
        <Save
          disabled={!modified.some((val) => val)}
          onClick={handleSaveClick}
        />
      </div>
      <hr />
      <FaceList></FaceList>
      <div className="clipboard">
        <h2>Clipboard</h2>
        <div className="image-grid"></div>
        <button className="copy">Copy</button>
        <button className="cut">Cut</button>
      </div>
    </div>
  );
}

export default Editor;
