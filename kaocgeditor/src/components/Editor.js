import React, { useState, useEffect } from "react";
import getGameInfos from "../data/gameData.js";
import { fileToImageDataArray } from "../utils.js";
import "../styles/Editor.css";

function ImageFigure({ imageData }) {
  const [imgUrl, setImgUrl] = useState(null);

  useEffect(() => {
    const canvas = document.createElement("canvas");
    canvas.width = imageData.width;
    canvas.height = imageData.height;
    const ctx = canvas.getContext("2d");
    ctx.putImageData(imageData, 0, 0);
    canvas.toBlob((blob) => {
      const url = URL.createObjectURL(blob);
      setImgUrl(url);
    });
  }, [imageData]);

  return (
    <figure>
      {imgUrl && <img src={imgUrl} alt={`Image ${imageData.id}`} />}
      <figcaption>{`Image ${imageData.id}`}</figcaption>
    </figure>
  );
}

function Editor() {
  const [gameList, setGameList] = useState([]);
  const [selectedGame, setSelectedGame] = useState(null);
  const [UploadBtnDisabled, setUploadBtnDisabled] = useState(true);

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

  function handleGameSelect(event) {
    const gameId = parseInt(event.target.value, 10);
    clearImageList();
    setSelectedGame(gameId);
    setUploadBtnDisabled(false);
  }

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
    clearImageList();

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

      // 在這裡編寫選擇文件後的處理邏輯
      const imageList = document.querySelector("#image-list");
      // let id = 1; // ID 起始值為 1
      imageList.appendChild(<ImagePreview imageDataArray={imageDataArray} />);
    };
  };

  function clearImageList() {
    const imageList = document.querySelector("#image-list");
    while (imageList.firstChild) {
      imageList.removeChild(imageList.firstChild);
    }
  }

  return (
    <div className="container">
      <div className="settings">
        <select id="game-select" onChange={handleGameSelect}>
          <option value="">--選擇遊戲--</option>
          {gameList.map((option) => (
            <option key={option.id} value={option.id}>
              {option.name}
            </option>
          ))}
        </select>
        <input
          type="file"
          disabled={UploadBtnDisabled}
          onChange={handleFileSelected}
          //   accept="image/*"
        />
      </div>
      <div className="preview">
        <div className="drag-drop">
          <p>拖放圖像到此區域或</p>
          <button>選擇圖像</button>
        </div>
        <div className="result"></div>
        <button className="apply">Apply</button>
      </div>
      <hr />
      <div className="image-list" id="image-list"></div>
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
