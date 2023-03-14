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

### 實驗

#### 將袁紹名字改一個不存在於 MSG.16P 的字，看顯示結果

將「紹」改為「叻」，這字的 BIG5 順序在「四」(93BD)之前，推導為 '93BC', MSG.16P 沒有。進去遊戲後亂碼。

#### 新君主名字取「一乙丁」看存檔內容

"一乙丁": D901 D902 D903
改成 D901 D904 D905 後進遊戲看不到後面兩個字
字型存在存檔檔案中, 605,520 開始為 D901 第一個字，每 28 bytes 一個字

#### 結論

- 綜合上面實驗可知，遊戲中有對應方式可以將 koei-tw 編碼對應到 MSG.16P 裡面的字，但目前不知在哪。
- 對應方式以外的字，會無法顯示成為亂碼（目前不知亂碼產生規則）
- 若要新增對應方式以外的字，必須將新字存於 sav file 中以作為顯示
- NBDATA.DAT 中也有對應字型(glyph)紀錄
- 上兩點的字形編碼從 D901 開始，形狀由 NAME.16P copy


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


## adjusted codes

9A30 <- [ ] (nobu4) 宇佐美 949694F59A30
9A32
9A35
9A43 <- [x] 胡
（中略）
9C66 <- [x] 新納 忠元 A2BA9C66
9C74 <- [ ] 耽
9C75 <- [ ] 耿

A66D <- [x] 銀
A66E <- [x] 銅
A696 <- [x] 髦
（中略）
A841 <- [x] 賞
A86D <- [x] 鄭
A86E <- [x] 鄧
A889 <- [ ] 震

## uncommon codes

AAAA <- [ ] 濬
AAAB
AAB3
AABC
AABE
AACB
AACF
AAD2
AAD3
AAD4
AADA
AADC
AAE3
AAE9
AAEC
AAF5
AAFD <- 膺
AB41
AB47 <- [ ] 薛
AB65
AB69 <- [x] 謝
AB70
AB82 <- [x] 輿
AB86
AB8C
AB93
AB95
ABA6
ABAF
ABF0 <- [x] 禮
ABFB
ABFD
AC38
AC39
AC45
AC46
AC47
AC55
AC58 <- [ ] 豐
AC64
AC6B
AC74
AC85
AC8E
AC97
AC9C <- 魏
ACA6
ACB0
ACB1
ACB4
ACB9
ACCD
ACCF
ACD0
ACE4
ACED
ACF9
ACFD
AD35
AD47
AD4B
AD59
AD68
AD78
AD81
AD85 <- [ ] 嚴
AD8B
ADA5
ADAA
ADB6
ADBB
ADBC
ADCB
ADD5
ADDC
ADE0
ADFA
ADFC <- 續
AE31
AE39
AE4D
AE53
AE57
AE65
AE76
AE81
AE83
AE92
AE9D
AEB2
AEBB <- [ ] 瓚
AECE
AEDA
AEE7
AEE8
AEF0
AEFB
AF37 <- 觀
AF4A
B035
B06C
B0BB
B0DA <- 汜 (big5: C9FA)
B339
B3AC
B3D9
B3FD
B567
B5A9
B6FC
B868
B9B5
BA8F
BBBA <- 翊
BCB5
BD84
BDBD
BDD3
BE9F
BEA0
BEB0
BF46
BFEC
C04F
C177 <- 楙
C18A
C19C
C36A
C3AE
C4BC
C5C3
C5F0
C66A
CAA5
CAC5
CC66 -> 縤（張繡）
CC8E
CDE5
CEC5
CEC9
CF6A
D1B8
D1F8
D289
D396
D4D2
D4F0 -> 騭
D746
EB9F
EBA0
EBA1
EBA3
EBA4
EBA5
EBA8
EBB3
EBB4
