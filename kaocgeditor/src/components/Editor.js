import React, {useState, useEffect} from 'react';
import getGameInfos from '../data/gameData.js';
import '../styles/Editor.css';
import UploadImage from './UploadImage.js';
import {useDispatch, useSelector} from 'react-redux';
import {
  selectGame,
  clearModified,
  selectFace,
  updateKao,
  loadFileDone,
} from '../reducers.js';
import PropTypes from 'prop-types';
import BenchPlayer from './BenchPlayer.js';
import {base64DecToArr, base64EncArr} from '../base64.js';
import FaceFigureContainer from './FaceFigureContainer.js';
import {dataToImage, hexToRgb} from '../utils.js';

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

function Save({disabled, onClick}) {
  return (
    <button className="save-btn" disabled={disabled} onClick={onClick}>
      下載更新
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
  const b64strings = useSelector((state) => state.editor.kaoData);
  const filename = useSelector((state) => {
    const info = state.editor.gameInfos[state.editor.currentGame];
    return info ? info.filename : 'KAODATA.DAT';
  });
  const halfHeight = useSelector((state) => {
    const info = state.editor.gameInfos[state.editor.currentGame];
    return info ? info.halfHeight : false;
  });

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

  const gameInfo = useSelector(
      (state) => state.editor.gameInfos[state.editor.currentGame],
  );

  const handleFileSelected = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.readAsArrayBuffer(file);
    reader.onload = (event) => {
      const uint8Buffer = new Uint8Array(event.target.result);

      // prepare KaoDataArray
      const faceDataSize = gameInfo.halfHeight ?
        (gameInfo.width * gameInfo.height * 3) / 8 / 2 :
        (gameInfo.width * gameInfo.height * 3) / 8;

      const faceCount =
        gameInfo.count === -1 ?
          Math.floor(uint8Buffer.byteLength / faceDataSize) :
          gameInfo.count;

      const color = gameInfo.palette.map(hexToRgb);

      [...Array(faceCount)].map((_, i) => {
        const faceData = uint8Buffer.slice(
            i * faceDataSize,
            (i + 1) * faceDataSize,
        );
        // faceData to imageData
        const imageData = dataToImage(
            faceData,
            gameInfo.width,
            gameInfo.height,
            color,
            gameInfo.halfHeight,
        );
        // imgUrl
        const canvas = document.createElement('canvas');
        canvas.width = gameInfo.width;
        canvas.height = gameInfo.height;
        const ctx = canvas.getContext('2d');
        ctx.putImageData(imageData, 0, 0);
        canvas.toBlob((blob) => {
          const url = URL.createObjectURL(blob);
          dispatch(
              updateKao({index: i, kao: base64EncArr(faceData), url: url}),
          );
        });
      });
      dispatch(loadFileDone());
    };
  };

  const handleSaveClick = () => {
    const bytes = new Uint8Array(b64strings.length * 1920);

    for (let i = 0, offset = 0; i < b64strings.length; i++, offset += 1920) {
      const data = base64DecToArr(b64strings[i]);
      bytes.set(data, offset);
    }

    const now = new Date();
    const dateString = now.toISOString().replace(/[:-]/g, '').replace('.', '');
    const newFilename = filename.replace(/(\.[^.]+)$/, `_${dateString}$1`);

    const blob = new Blob([bytes], {type: 'application/octet-stream'});
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = newFilename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // clear other states
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
          disabled={!modified.some((val) => val) || halfHeight}
          onClick={handleSaveClick}
        />
      </div>
      <hr />
      <FaceFigureContainer />
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
