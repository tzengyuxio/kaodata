
## 獨立戰爭

- 前三個 byte 是 MagicWord, 固定 'IDX'
- 第四個 byte 各有差異
- FACE.IDX 每個 block 的前 8 個 bytes 應該是 width 與 height
- FACE.IDX 有 299 筆 offset 資料 (299 - 0x12B)
  - block size: min(1538), max(2023), avg1798.12
- COMMAND.IDX, EVENT.IDX 中有 'NPK016' 字樣，覺得眼熟
  - 另外檔案中也有個 'OPENNPK.NPK', 推測可能是片頭 OP

| file         | pos(3)     | pos(4-7)     | first NBK016 | bytes before first | memo                   |
| ------------ | ---------- | ------------ | ------------ | ------------------ | ---------------------- |
| COMMAND.IDX  | 18 (0x12)  | 76 (0x4C)    | 76           | 72                 |                        |
| EVENT.IDX    | 22 (0x16)  | 92 (0x5C)    | 92           | 88                 |                        |
| FACE.IDX     | 43 (0x2B)  | 1200 (0x4B0) | --           | 1196               | 1200 處是 0x40005000LE |
| GRAPHICS.IDX | 142 (0x8E) | 572 (0x23C)  | --           | 568                | 572 處是 0x04001800LE  |
