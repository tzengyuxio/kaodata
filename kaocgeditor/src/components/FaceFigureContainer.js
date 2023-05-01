import Mark from 'mark.js';
import React, {useEffect, useRef} from 'react';
import {useTranslation} from 'react-i18next';
import {useSelector} from 'react-redux';

import {FaceFigure} from './FaceFigure';
import Instruction from './Instruction';

export default function FaceFigureContainer() {
  const nodeRef = useRef(null);
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
  const {t, i18n} = useTranslation();

  useEffect(() => {
    const instance = new Mark(nodeRef.current);
    instance.markRegExp(/`(.*?)`/g, {
      element: 'code',
      className: 'blue',
    });
  }, [kaoFile, i18n.language]);

  const instruction = <Instruction />;

  return (
    <div className="face-figure-container">
      {currentGame &&
                fileLoaded &&
                [...Array(faceCount)].map((_, index) => (
                  <FaceFigure key={index} id={index}></FaceFigure>
                ))}
      {currentGame && !fileLoaded && (
        <div className="no-game-selected" ref={nodeRef}>
          <span ref={nodeRef}>
            {t('instruction.upload_file', {
              filename: kaoFile.toUpperCase(),
            })}
          </span>
          <br />
          {`${
                        currentGame && halfHeight ?
                            t('instruction.no_download') :
                            ''
          } `}
        </div>
      )}
      {!currentGame && (
        <React.Fragment>
          <div className="no-game-selected">
            {t('instruction.select_game')}
          </div>
          <br />
          {instruction}
        </React.Fragment>
      )}
    </div>
  );
}
