import React from 'react';
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

/**
 * 選擇遊戲用的下拉式選單。改變當前選取遊戲。
 *
 * @return {JSX.Element} GameSelect 組件。
 */
function GameSelect() {
  const dispatch = useDispatch();
  const gameInfos = useSelector((state) => state.editor.gameInfos);
  const {t} = useTranslation();
  const handleChange = (e) => {
    const gameId = e.target.value;
    dispatch(selectGame(gameId));
  };

  return (
    <select id="game-select" onChange={handleChange}>
      <option value="">--{t('select-game')}--</option>
      {Object.values(gameInfos).map((info) => (
        <option key={info.id} value={info.id}>
          {info.name}
        </option>
      ))}
    </select>
  );
}

/**
 * 下載更新後的頭像檔案。
 *
 * @return {JSX.Element} SaveFaceFile 組件。
 */
function SaveFaceFile() {
  const kaoData = useSelector((state) => state.editor.kaoData);
  const filename = useSelector((state) => {
    const info = state.editor.gameInfos[state.editor.currentGame];
    return info ? info.filename : 'KAODATA.DAT';
  });
  const modified = useSelector((state) => {
    return state.editor.modifiedFace.some((value) => value);
  });
  const halfHeight = useSelector((state) => {
    const info = state.editor.gameInfos[state.editor.currentGame];
    return info ? info.halfHeight : false;
  });
  const {t} = useTranslation();

  const handleClick = () => {
    const faceDataSize = 1920;
    const bytes = new Uint8Array(kaoData.length * faceDataSize);

    kaoData.map((data, index) => {
      const u8Array = base64DecToArr(data);
      bytes.set(u8Array, index * faceDataSize);
    });

    // KAODATA.DAT -> KAODATA_YYYYMMTDDHHmmss0Z.DAT (ex. 20230425T025410170Z)
    const now = new Date();
    const dateString = now
        .toISOString()
        .replace(/[:-]/g, '')
        .replace('.', '');
    const newFilename = filename.replace(/(\.[^.]+)$/, `_${dateString}$1`);

    // create a link and click it to download the file
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
    <button
      className="save-btn save-face-file"
      disabled={!modified || halfHeight}
      onClick={handleClick}
    >
      {t('button.save')}
    </button>
  );
}

export default function Settings() {
  const dispatch = useDispatch();
  const gameInfo = useSelector(
      (state) => state.editor.gameInfos[state.editor.currentGame],
  );

  const handleFileSelected = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    if (file instanceof Blob) {
      reader.onload = (event) => {
        const u8Buffer = new Uint8Array(event.target.result);

        const w = gameInfo.width;
        const h = gameInfo.height;
        const hh = gameInfo.halfHeight;
        const count = gameInfo.count;
        const colors = gameInfo.palette.map(hexToRgb);

        // prepare KaoDataArray
        const faceDataSize = hh ? (w * h * 3) / 8 / 2 : (w * h * 3) / 8;
        const faceCount =
                    count === -1 ?
                        Math.floor(u8Buffer.byteLength / faceDataSize) :
                        count;

        [...Array(faceCount)].map((_, i) => {
          const faceData = u8Buffer.slice(
              i * faceDataSize,
              (i + 1) * faceDataSize,
          );
          // faceData to imageData
          const imageData = dataToImage(faceData, w, h, colors, hh);
          // imgUrl
          const canvas = document.createElement('canvas');
          canvas.width = w;
          canvas.height = h;
          const ctx = canvas.getContext('2d');
          ctx.putImageData(imageData, 0, 0);
          canvas.toBlob((blob) => {
            const url = URL.createObjectURL(blob);
            const b64FaceData = base64EncArr(faceData);
            dispatch(
                updateKao({index: i, kao: b64FaceData, url: url}),
            );
          });
        });
        dispatch(loadFileDone());
      };
      reader.onerror = (error) => {
        console.error('Load file error:', error);
      };
      reader.readAsArrayBuffer(file);
    } else {
      console.error('The selected file isn\'t a Blob object.');
    }
  };

  const uploadButtonDisabled = useSelector((state) => {
    return state.editor.currentGame === '' ? true : false;
  });

  return (
    <div id="settings" className="settings outline-block">
      <TabLabel labelKey="tabs.game" />
      <GameSelect />
      <input
        type="file"
        className="load-face-file"
        disabled={uploadButtonDisabled}
        onChange={handleFileSelected}
        //   accept="image/*"
      />
      <SaveFaceFile />
    </div>
  );
}
