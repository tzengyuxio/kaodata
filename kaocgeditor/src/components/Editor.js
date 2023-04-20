import React, { useState, useEffect } from "react";
import getGameInfos from "../data/gameData.js";
import { fileToImageDataArray } from "../utils.js";
import "../styles/Editor.css";
import UploadImage from "./UploadImage.js";

function GameSelect(props) {
  const handleChange = (e) => {
    const gameId = e.target.value;
    props.setImageDataArray(null);
    props.setSelectedGame(gameId);
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

function ImageFigure(props) {
  const [imgUrl, setImgUrl] = useState(null);

  useEffect(() => {
    const canvas = document.createElement("canvas");
    canvas.width = props.imageData.width;
    canvas.height = props.imageData.height;
    const ctx = canvas.getContext("2d");
    ctx.putImageData(props.imageData, 0, 0);
    canvas.toBlob((blob) => {
      const url = URL.createObjectURL(blob);
      setImgUrl(url);
    });
  }, [props.imageData]);

  let faceIndex = props.imageKey + 1;

  let names = getGameInfos()[props.selectedGame].names;
  let name = names[props.imageKey] === "" ? "(未命名)" : names[props.imageKey];

  console.log("Rendering ImageFigure");
  return (
    <figure
      id={`face-${props.imageKey + 1}`}
      className={`image-figure ${props.selected ? "selected" : ""} ${
        props.modified ? "modified" : ""
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

function FaceList(props) {
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [modified, setModified] = useState([]);

  function handleFigureClick(e, index) {
    e.stopPropagation();
    if (selectedIndex === index) {
      setSelectedIndex(null);
    } else {
      setSelectedIndex(index);
      setModified(modified => [...modified.slice(0, index), false, ...modified.slice(index + 1)]);
    }
  }

  const handleApplyClick = () => {
    setModified(modified => [...modified.slice(0, selectedIndex), true, ...modified.slice(selectedIndex + 1)]);
  };

  const handleSaveClick = () => {
    setModified(modified => modified.map(() => false));
    setSelectedIndex(null);
  };

  if (!props.imageDataArray) {
    return (
      <div className="image-list" id="image-list">
        請先選擇遊戲，並上傳檔案
      </div>
    );
  }
  return (
    <div className="image-list">
      <Apply disabled={selectedIndex === null} onClick={handleApplyClick} />
      <Save disabled={!modified.some(val => val)} onClick={handleSaveClick} />
      <br />
      {props.imageDataArray.map((imageData, index) => (
        <ImageFigure
          key={index}
          imageKey={index}
          imageData={imageData}
          selectedGame={props.selectedGame}
          selected={selectedIndex == index}
          modified={modified[index]}
          onClick={e => handleFigureClick(e, index)}
        ></ImageFigure>
      ))}
    </div>
  );
}

function Apply({ disabled, onClick }) {
  return (
    <button className="apply-btn" disabled={disabled} onClick={onClick}>
      Apply
    </button>
  );
}

function Save({ disabled, onClick }) {
  return (
    <button className="save-btn" disabled={disabled} onClick={onClick}>
      Save
    </button>
  );
}

function Editor() {
  const [gameList, setGameList] = useState([]);
  const [selectedGame, setSelectedGame] = useState(null);
  const [UploadBtnDisabled, setUploadBtnDisabled] = useState(true);
  const [imageDataArray, setImageDataArray] = useState(() => null);
  const [selectedFace, setSelectedFace] = useState(() => null);

  useEffect(() => {
    // 從 gameData.js 文件中取得遊戲數據
    const game_infos = getGameInfos();
    // 根據數據建立選項
    const list = Object.values(game_infos).map((game) => ({
      id: game.id,
      name: game.name,
    }));
    setGameList(list);
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    // 在這裡編寫提交表單的邏輯
  };

  function ImagePreview({ imageDataArray }) {
    console.log("ImagePreview called");
    if (!Array.isArray(imageDataArray)) {
      return null;
    }
    return (
      <div>
        {imageDataArray.map((imageData) => (
          <ImageFigure key={imageData.id} imageData={imageData} />
        ))}
      </div>
    );
  }

  const handleFileSelected = (event) => {
    const gameSelect = document.querySelector("#game-select");
    const theGame = getGameInfos()[gameSelect.value];
    setImageDataArray(null);

    const file = event.target.files[0];
    const reader = new FileReader();
    reader.readAsArrayBuffer(file);
    reader.onload = (event) => {
      const uint8Buffer = new Uint8Array(event.target.result);
      const imageDataArray = fileToImageDataArray(
        uint8Buffer,
        theGame.width,
        theGame.height,
        theGame.palette,
        theGame.halfHeight,
        theGame.count
      );

      setImageDataArray(imageDataArray);
    };
  };

  return (
    <div className="container">
      <div className="settings">
        <GameSelect
          gameList={gameList}
          setImageDataArray={setImageDataArray}
          setSelectedGame={setSelectedGame}
          setUploadBtnDisabled={setUploadBtnDisabled}
        ></GameSelect>
        <input
          type="file"
          disabled={UploadBtnDisabled}
          onChange={handleFileSelected}
          //   accept="image/*"
        />
      </div>
      <div className="preview">
        <UploadImage></UploadImage> →<div className="result"></div>
        <button className="apply">Apply</button>
      </div>
      <hr />
      <FaceList
        imageDataArray={imageDataArray}
        selectedGame={selectedGame}
      ></FaceList>
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
