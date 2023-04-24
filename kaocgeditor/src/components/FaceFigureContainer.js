import React from 'react';
import {useSelector} from 'react-redux';

import {FaceFigure} from './FaceFigure';

export default function FaceFigureContainer() {
  const currentGame = useSelector((state) => state.editor.currentGame);
  const faceCount = useSelector((state) => {
    const info = state.editor.gameInfos[state.editor.currentGame];
    return info ? info.names.length : -1;
  });
  const kaoFile = useSelector((state) => {
    const info = state.editor.gameInfos[state.editor.currentGame];
    return info ? info.filename : '';
  });
  const fileLoaded = useSelector((state) => state.editor.fileLoaded);
  const halfHeight = useSelector((state) => {
    const info = state.editor.gameInfos[state.editor.currentGame];
    return info ? info.halfHeight : false;
  });

  return (
    <div className="face-figure-container">
      {currentGame &&
                fileLoaded &&
                [...Array(faceCount)].map((_, index) => (
                  <FaceFigure key={index} id={index}></FaceFigure>
                ))}
      {currentGame && !fileLoaded && (
        <div className="no-game-selected">
                    請選擇遊戲檔案 {kaoFile} 上傳。
          <br />
          {`${
                        currentGame && halfHeight ?
                            '此遊戲目前只支援瀏覽頭像，尚不支援「替換」與「下載更新」頭像。' :
                            ''
          } `}
        </div>
      )}
      {!currentGame && (
        <div className="no-game-selected">
                    請先選擇遊戲，並上傳檔案。
        </div>
      )}
    </div>
  );
}
