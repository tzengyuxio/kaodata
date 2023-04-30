import PropTypes from 'prop-types';
import React, {useEffect, useState} from 'react';
import {useTranslation} from 'react-i18next';
import {useDispatch, useSelector} from 'react-redux';

import {base64DecToArr, base64EncArr} from '../base64.js';
import {
  clearModified,
  loadFileDone,
  selectFace,
  selectGame,
  updateKao,
} from '../reducers';
import {dataToImage, hexToRgb} from '../utils.js';
import TabLabel from './TabLabel.js';

function GameSelect(props) {
  const dispatch = useDispatch();
  const handleChange = (e) => {
    const gameId = e.target.value;
    dispatch(selectGame(gameId));
    props.setUploadBtnDisabled(false);
  };
  const {t} = useTranslation();

  return (
    <select id="game-select" onChange={handleChange}>
      <option value="">--{t('select-game')}--</option>
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

function SaveFaceFile({disabled, onClick}) {
  const {t} = useTranslation();
  return (
    <button className="save-btn" disabled={disabled} onClick={onClick}>
      {t('button.save')}
    </button>
  );
}
SaveFaceFile.propTypes = {
  disabled: PropTypes.bool,
  onClick: PropTypes.func,
};

export default function Settings() {
  const [gameList, setGameList] = useState([]);
  const gameInfos = useSelector((state) => state.editor.gameInfos);
  const dispatch = useDispatch();
  const [UploadBtnDisabled, setUploadBtnDisabled] = useState(true);
  const modified = useSelector((state) => state.editor.modifiedFace);
  const halfHeight = useSelector((state) => {
    const info = state.editor.gameInfos[state.editor.currentGame];
    return info ? info.halfHeight : false;
  });
  const b64strings = useSelector((state) => state.editor.kaoData);
  const filename = useSelector((state) => {
    const info = state.editor.gameInfos[state.editor.currentGame];
    return info ? info.filename : 'KAODATA.DAT';
  });
  const gameInfo = useSelector(
      (state) => state.editor.gameInfos[state.editor.currentGame],
  );

  useEffect(() => {
    // 根據數據建立選項
    const list = Object.values(gameInfos).map((game) => ({
      id: game.id,
      name: game.name,
    }));
    setGameList(list);
  }, []);

  const handleFileSelected = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    if (file instanceof Blob) {
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
                updateKao({
                  index: i,
                  kao: base64EncArr(faceData),
                  url: url,
                }),
            );
          });
        });
        dispatch(loadFileDone());
      };
      reader.onerror = (error) => {
        console.error(error);
      };
      reader.readAsArrayBuffer(file);
    } else {
      console.error('The selected file isn\'t a Blob object.');
    }
  };

  const handleSaveClick = () => {
    const bytes = new Uint8Array(b64strings.length * 1920);

    for (
      let i = 0, offset = 0;
      i < b64strings.length;
      i++, offset += 1920
    ) {
      const data = base64DecToArr(b64strings[i]);
      bytes.set(data, offset);
    }

    const now = new Date();
    const dateString = now
        .toISOString()
        .replace(/[:-]/g, '')
        .replace('.', '');
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

  return (
    <div id="settings" className="settings outline-block">
      <TabLabel labelKey="tabs.game" />
      <GameSelect
        gameList={gameList}
        setUploadBtnDisabled={setUploadBtnDisabled}
      />
      <input
        type="file"
        className="load-face-file"
        disabled={UploadBtnDisabled}
        onChange={handleFileSelected}
        //   accept="image/*"
      />
      <SaveFaceFile
        className="save-face-file"
        disabled={!modified.some((val) => val) || halfHeight}
        onClick={handleSaveClick}
      />
    </div>
  );
}
