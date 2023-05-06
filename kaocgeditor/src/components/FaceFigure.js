import PropTypes from 'prop-types';
import React, {useEffect, useState} from 'react';
import {useDispatch, useSelector} from 'react-redux';

import {store} from '../app/store.js';
import {selectFace} from '../reducers.js';

export function FaceFigure(props) {
  const [imgUrl, setImgUrl] = useState(null);
  const dispatch = useDispatch();

  const name = useSelector((state) => {
    const info = state.editor.gameInfos[state.editor.currentGame];
    const n = info.faceNames[props.id];
    return n === '' ? '——' : n;
  });

  const selected = useSelector(
      (state) => state.editor.selectedFace == props.id,
  );
  const modified = useSelector(
      (state) => state.editor.modifiedFace[props.id],
  );

  const handleFigureClick = (e, index) => {
    e.stopPropagation();
    dispatch(selectFace(index));
  };

  useEffect(() => {
    const unsubsribe = store.subscribe(() => {
      const updatedItem = store.getState().editor.kaoImgUrl[props.id];
      setImgUrl(updatedItem);
    });

    return () => {
      unsubsribe();
    };
  }, [props.id]);

  return (
    <figure
      id={`face-${props.id}`}
      className={`face-figure ${selected ? 'selected' : ''} ${
                modified ? 'modified' : ''
      }`}
      onClick={(e) => handleFigureClick(e, props.id)}
    >
      {imgUrl && <img src={imgUrl} alt={`${name} 顏ＣＧ`} />}
      <figcaption>
        {props.id}
        <br />
        {name.split('\n').map((str) => (
          <>
            {str}
            <br />
          </>
        ))}
      </figcaption>
    </figure>
  );
}
FaceFigure.propTypes = {
  id: PropTypes.number.isRequired,
};

export default FaceFigure;
