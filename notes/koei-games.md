# Notes of Koei Games

雜七雜八的都記在這邊

## 項劉記

大地圖 (see [https://cafe.naver.com/koeimod/256])

- GRP3.KR1
- 分上下部份
- 變種 NPK/RLE
- 一個檔案中有多個不同格式

## 源平合戰

원평합전
원평합전 이미지 편집기 (源平合戰 影像 編輯器)

似乎有韓文編輯器 (source: https://k66google.tistory.com/766)

0x8000A000 在 kaodata.gp 出現位置
- 0
- 4403 0x1133 後面接 0x7FFF, 與前差 4403
- 5068 0x13cc 後面接 0x7000, 與前差 665
- 10068 0x2754, 0x7FFF, 5000
- 10760 0x2A08, 0x7000, 692
- 14932 0x3A54, 0x7FFF, 4172
- 15490 0x3C82, 0x7000, 558

mask 應該有 2560 bytes

## 英傑傳

有兩個版本的頭像檔案

### DOS

- 人物似乎只有八色
- 檔案 342 KB
- 前面有 1440 bytes 為 offsets 資料, 6 bytes 一組, 240 組
- offset info 為 start(4 bytes) 與 size(2 bytes)
- 每個 block 開頭有 7 bytes 相同 `0254 0850 0033 03`
- 第 8 byte 都是 D2, C6, E1, C6, C9 這類的數值
- 第 9 byte 都是 `20`
- 第 10 byte 都是 `04` `05` `06` `07` `08`
- 後面的就比較沒規律

### WINDOS

- 檔案 461 KB
- 有 LS11 檔頭
- 每個 block 似乎都有 'NPK016' 字樣 (獨立戰爭也有)

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

### NPK 壓縮

bitflag: 0xff1e, cursor=1, dest_len=0             #
bitflag: 0x7f8f, cursor=3, dest_len=4             #
    over_line=False, run_offset=0, run_count=128  #
bitflag: 0x3fc7, cursor=4, dest_len=132
    over_line=False, run_offset=8, run_count=108  # 第一行結束
bitflag: 0x1fe3, cursor=5, dest_len=240
    over_line=True, run_offset=0, run_count=128   #
bitflag: 0xff1, cursor=6, dest_len=368
    over_line=False, run_offset=8, run_count=112  # 第二行結束
bitflag: 0x7f8, cursor=7, dest_len=480            # 4px, 黑黑黑　藍
bitflag: 0x3fc, cursor=9, dest_len=484            # 4px, 藍 淺藍 淺藍 黑
bitflag: 0x1fe, cursor=11, dest_len=488           # 4px, 藍 藍 藍 藍 (共有 224 個藍)
bitflag: 0xff83, cursor=14, dest_len=492          #
    over_line=False, run_offset=0, run_count=128  # 128 藍, (累計132, 剩餘92)
bitflag: 0x7fc1, cursor=15, dest_len=620          #
    over_line=False, run_offset=8, run_count=92   # 92 藍, (累計224, 剩餘0)
bitflag: 0x3fe0, cursor=16, dest_len=712          # 黑 淺 淺 藍
bitflag: 0x1ff0, cursor=18, dest_len=716          # 藍 黑 黑 黑, 第三行結束
bitflag: 0xff8, cursor=20, dest_len=720           # 4px
bitflag: 0x7fc, cursor=22, dest_len=724           # 4px
bitflag: 0x3fe, cursor=24, dest_len=728           # 4px
bitflag: 0x1ff, cursor=26, dest_len=732
    over_line=False, run_offset=0, run_count=128  # 128px
bitflag: 0xffc1, cursor=28, dest_len=860
    over_line=False, run_offset=8, run_count=92   # 92px
bitflag: 0x7fe0, cursor=29, dest_len=952          # 4px
bitflag: 0x3ff0, cursor=31, dest_len=956          # 4px, 第四行結束
bitflag: 0x1ff8, cursor=33, dest_len=960          # 4px
bitflag: 0xffc, cursor=35, dest_len=964           # 4px
bitflag: 0x7fe, cursor=37, dest_len=968           # 4px
bitflag: 0x3ff, cursor=39, dest_len=972           #
    over_line=False, run_offset=0, run_count=128  # 128px
bitflag: 0x1ff, cursor=40, dest_len=1100
    over_line=False, run_offset=8, run_count=92   # 92px
bitflag: 0xff30, cursor=42, dest_len=1192         # 4px
bitflag: 0x7f98, cursor=44, dest_len=1196         # 4px, 第五行結束
bitflag: 0x3fcc, cursor=46, dest_len=1200         # 4px
bitflag: 0x1fe6, cursor=48, dest_len=1204         # 4px ! 最後變藍色？
bitflag: 0xff3, cursor=50, dest_len=1208
    over_line=True, run_offset=480, run_count=128 # 128px
bitflag: 0x7f9, cursor=51, dest_len=1336
    over_line=False, run_offset=8, run_count=96   # 96px
bitflag: 0x3fc, cursor=52, dest_len=1432          # 4px
bitflag: 0x1fe, cursor=54, dest_len=1436          # 4px, 第六行結束
bitflag: 0xff18, cursor=57, dest_len=1440         # 4px
bitflag: 0x7f8c, cursor=59, dest_len=1444         # 4px
bitflag: 0x3fc6, cursor=61, dest_len=1448         # 4px
bitflag: 0x1fe3, cursor=63, dest_len=1452
    over_line=False, run_offset=0, run_count=128  # 128px
bitflag: 0xff1, cursor=64, dest_len=1580
    over_line=False, run_offset=8, run_count=92   # 92px
bitflag: 0x7f8, cursor=65, dest_len=1672          # 4px
bitflag: 0x3fc, cursor=67, dest_len=1676          # 4px, 第七行結束
bitflag: 0x1fe, cursor=69, dest_len=1680          # 4px
bitflag: 0xff66, cursor=72, dest_len=1684         # 4px
bitflag: 0x7fb3, cursor=74, dest_len=1688         # 4px
    over_line=True, run_offset=0, run_count=128   # 128px
bitflag: 0x3fd9, cursor=75, dest_len=1816
    over_line=False, run_offset=8, run_count=96   # 96px
bitflag: 0x1fec, cursor=76, dest_len=1912
bitflag: 0xff6, cursor=78, dest_len=1916
bitflag: 0x7fb, cursor=80, dest_len=1920
    over_line=True, run_offset=1440, run_count=4
bitflag: 0x3fd, cursor=81, dest_len=1924
    over_line=True, run_offset=0, run_count=4
bitflag: 0x1fe, cursor=82, dest_len=1928
bitflag: 0xffd2, cursor=85, dest_len=1932
bitflag: 0x7fe9, cursor=87, dest_len=1936
    over_line=False, run_offset=0, run_count=44
bitflag: 0x3ff4, cursor=88, dest_len=1980
bitflag: 0x1ffa, cursor=90, dest_len=1984
bitflag: 0xffd, cursor=92, dest_len=1988
    over_line=False, run_offset=0, run_count=4
bitflag: 0x7fe, cursor=93, dest_len=1992
bitflag: 0x3ff, cursor=95, dest_len=1996
    over_line=False, run_offset=24, run_count=12
bitflag: 0x1ff, cursor=96, dest_len=2008
    over_line=False, run_offset=8, run_count=4
bitflag: 0xff66, cursor=98, dest_len=2012

## 魔眼邪神

- 日: ケルトの聖戦 (日文 wiki 好像找不到條目?)
- 英: Celtic Tales: Balor of the Evil Eye
- [魔眼邪神存檔分析 \- KPHEROS\# \- lechi的創作 \- 巴哈姆特](https://home.gamer.com.tw/artwork.php?sn=5227637)
