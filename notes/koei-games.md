# Notes of Koei Games

雜七雜八的都記在這邊

## 水滸傳

0 太尉,寵臣
1 太守,高官
2 官吏,官吏
3 好漢
4 頭目
5 強盜,無頼漢
6 義兄
7 義弟
8 死亡
9 罪犯
10 僧侶,僧侶
11 漁夫,漁師
12 苦力,人夫
13 醫者,医者
14 生意人,商人
15 客棧掌櫃,居酒屋
16 技工,職人
17 學究,学者
18 富人,長者
19 少爺,若旦那
20 少女,小娘
21 藝妓,芸妓
22 獵人,猟師
23 大力士,力士
24 壯士,武芸者
25 客商,旅商人
26 江湖藝人
27 道士,道士
28 失業武人,浪人
29 無業遊民,無法者
30 虎
31 狼
32 熊
33 豹

## 獨立戰爭

- 前三個 byte 是 MagicWord, 固定 'IDX'
- 第四個 byte 各有差異
- FACE.IDX 每個 block 的前 8 個 bytes 應該是 width 與 height
- FACE.IDX 有 299 筆 offset 資料 (299 - 0x12B)
  - block size: min(1538), max(2023), avg1798.12
- COMMAND.IDX, EVENT.IDX 中有 'NPK016' 字樣，覺得眼熟
  - 另外檔案中也有個 'OPENNPK.NPK', 推測可能是片頭 OP
- 98版 129 頭像，SF版 174 頭像 (光榮美術館數據)
- GRAPHICS.IDX 中，每個 block 的頭四個 bytes 是 width 與 height,
  - 接下來的兩個 bytes (`first_byte`) 可能與色彩數或 block 長度有關
  - block size = width x height x (`first_byte` / 8)

| file         | pos(3)     | pos(4-7)     | first NBK016 | bytes before first | memo                   |
| ------------ | ---------- | ------------ | ------------ | ------------------ | ---------------------- |
| COMMAND.IDX  | 18 (0x12)  | 76 (0x4C)    | 76           | 72                 |                        |
| EVENT.IDX    | 22 (0x16)  | 92 (0x5C)    | 92           | 88                 |                        |
| FACE.IDX     | 43 (0x2B)  | 1200 (0x4B0) | --           | 1196               | 1200 處是 0x40005000LE |
| GRAPHICS.IDX | 142 (0x8E) | 572 (0x23C)  | --           | 568                | 572 處是 0x04001800LE  |

## 魔眼邪神

- 日: ケルトの聖戦 (日文 wiki 好像找不到條目?)
- 英: Celtic Tales: Balor of the Evil Eye
- [魔眼邪神存檔分析 \- KPHEROS\# \- lechi的創作 \- 巴哈姆特](https://home.gamer.com.tw/artwork.php?sn=5227637)
