import React from 'react';
import {useSelector} from 'react-redux';

import {FaceFigure} from './FaceFigure';

export default function FaceFigureContainer() {
  const currentGame = useSelector((state) => state.editor.currentGame);
  const faceCount = useSelector((state) => {
    const info = state.editor.gameInfos[state.editor.currentGame];
    return info ? info.faceNames.length : -1;
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

  const instruction = (
    <React.Fragment>
      <div>使用說明：</div>
      <ol>
        <li>先在左上角選單選擇遊戲</li>
        <li>
                    按下<span style={{color: '#f44'}}>「選擇檔案」</span>
                    按鈕上傳遊戲頭像檔
        </li>
        <li>讀取完成之後會出現頭像列表。</li>
        <li>
                    將想要放進遊戲裡的頭像拖拉至替換區域。可使用照片或是其他圖片，寬高比例
                    4:5 為佳，超過的話會自動裁切。
        </li>
        <li>
                    在下方頭像列表中選取要替換的頭像，按下
          <span style={{color: '#f44'}}>「替補」</span>按鈕
        </li>
        <li>
                    重複 步驟 4. 5.,
                    可替換多個頭像。被替換的頭像會以背景色特別標註。
        </li>
        <li>
                    完成替換後，按下
          <span style={{color: '#f44'}}>「下載更新」</span>
                    按鈕，即可下載檔案。
        </li>
        <li>
                    將下載的檔案放到遊戲資料夾中，替換檔名，進去遊戲後便可看到替換的頭像。
        </li>
      </ol>
    </React.Fragment>
  );

  return (
    <div className="face-figure-container">
      {currentGame &&
                fileLoaded &&
                [...Array(faceCount)].map((_, index) => (
                  <FaceFigure key={index} id={index}></FaceFigure>
                ))}
      {currentGame && !fileLoaded && (
        <div className="no-game-selected">
                    請選擇遊戲檔案 <code style={{color: 'blue'}}>{kaoFile}</code> 上傳。
          <br />
          {`${
                        currentGame && halfHeight ?
                            '此遊戲目前只支援瀏覽頭像，尚不支援「下載更新」功能。' :
                            ''
          } `}
        </div>
      )}
      {!currentGame && (
        <React.Fragment>
          <div className="no-game-selected">
                        請先選擇遊戲，並上傳檔案。
          </div>
          <br />
          {instruction}
        </React.Fragment>
      )}
    </div>
  );
}
