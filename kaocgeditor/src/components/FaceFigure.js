import React, {useState, useEffect} from 'react';
import {useDispatch, useSelector} from 'react-redux';
import PropTypes from 'prop-types';
import {selectFace} from '../reducers.js';
import {store} from '../app/store.js';

export function FaceFigure(props) {
  const [imgUrl, setImgUrl] = useState(null);
  const dispatch = useDispatch();

  const name = useSelector((state) => {
    const n = state.editor.gameInfos[state.editor.currentGame].names[props.id];
    return n === '' ? '(未命名)' : n;
  });

  const selected = useSelector(
      (state) => state.editor.selectedFace == props.id,
  );
  const modified = useSelector((state) => state.editor.modifiedFace[props.id]);

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
        {props.id + 1}
        <br />
        {name}
      </figcaption>
    </figure>
  );
}
FaceFigure.propTypes = {
  id: PropTypes.number.isRequired,
};

export default FaceFigure;
