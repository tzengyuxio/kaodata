import React, { useState, useEffect } from "react";
import getGameInfos from "../data/gameData.js";
import { fileToImageDataArray } from "../utils.js";
import "../styles/Editor.css";

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
      let id = 1; // ID 起始值為 1
      for (const imageData of imageDataArray) {
        // 建立一個新的 <figure> 標籤元素
        const figure = document.createElement("figure");
        figure.setAttribute("id", `image-${id}`);

        // 建立一個新的 <img> 標籤，並將圖片資料設為其 src 屬性
        // const img = document.createElement("img");
        // img.src = URL.createObjectURL(
        //   new Blob([imageData], { type: "image/png" })
        // );
        const canvas = document.createElement("canvas");
        canvas.width = imageData.width;
        canvas.height = imageData.height;
        const ctx = canvas.getContext("2d");
        ctx.putImageData(imageData, 0, 0);
        canvas.toBlob((blob) => {
          const url = URL.createObjectURL(blob);
          const img = new Image();
          img.src = url;
          figure.appendChild(img);
        });

        // 建立一個新的 <figcaption> 標籤，並將圖說設為其內容
        const caption = document.createElement("figcaption");
        caption.textContent = `Image ${id}`;

        // 在 <figure> 標籤元素中添加 <img> 和 <figcaption> 子元素
        // figure.appendChild(img);
        figure.appendChild(caption);

        // 將 <figure> 標籤元素添加到 image-list 元素中
        imageList.appendChild(figure);

        id++;
      }
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
