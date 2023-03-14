# 字庫研究

## 通用

- 0xnn3A - 0xnn40
- 0xnn5B - 0xnn60
- 0xnn7B - 0xnn7F

輸出表格中，XX30-xx7F 這段的圖形分佈，與 EUC JP 的 A3B0-A3FF 圖形相似。

https://uic.io/en/charset/show/euc-jp/

推測未使用部分可能用來作為某些控制碼定義。

big5
    - per page: 157
    - start pos: A440
koei-font
    - per page: 188(?), 187(?)
    - start pos: 92A0 (未證實，須參考 '一' 的 code)

## 水滸傳
- 3F4A58 (忠義 仁愛 勇氣 64, 74, 88) 魯智深
    - 體力能耐技能智慧 隨機
- 魯智深 第二, 宋江 第四, 高俅 第一

## 三國志III

| 字  | DOS編碼 | WIN 編碼 | Big5 |        Memo        |
| --- | ------- | -------- | ---- | ------------------ |
| 袁  | 9CAF    |          | B04B |                    |
| 紹  | 9ED4    |          | B2D0 |                    |
| 曹  | 9E39    |          | B1E4 |                    |
| 操  | A8E6    |          | BEDE |                    |
| 陳  | 9F94    |          | B3AF |                    |
| 琳  | A0DE    |          | B559 | 與 拿破崙 in-game 編碼相同 |

## 拿破崙

| word | in name | big 5 | in msg.16 |     |  diff  |
| ---- | ------- | ----- | --------- | --- | ------ |
| 三   | 92b4    | a454  |           | x   | 0x11a0 |
| 卡   | 93a5    | a564  |           | x   | 0x11bf |
| 世   | 9381    | a540  |           | x   | 0x11bf |
| 四   | 93bd    | a57c  |           | x   | 0x11bf |
| 治   | 97d8    | aa76  |           | x   | 0x129e |
| 洛   | 99a7    | aca5  |           | x   | 0x12fe |
| 娜   | 9af3    | ae52  |           | x   | 0x135f |
| 拿   | 9b71    | aeb3  |           | x   | 0x1342 |
| 破   | 9c31    | af7d  |           | x   | 0x134c |
| 崙   | 9da0    | b15b  |           | x   | 0x13bb |
| 喬   | 9fd1    | b3ec  |           | x   | 0x141b |
| 琳   | a0de    | b559  |           | x   | 0x147b |