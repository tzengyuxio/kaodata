# 三國志 頭像 研究筆記

- [三國志 頭像 研究筆記](#三國志-頭像-研究筆記)
  - [系列共通](#系列共通)
    - [各代用語](#各代用語)
    - [尺寸代號](#尺寸代號)
    - [工具或參考頁面](#工具或參考頁面)
    - [頭像檔命名規範](#頭像檔命名規範)
      - [代號](#代號)
  - [SAN1, SAN2](#san1-san2)
    - [檔案](#檔案)
  - [SAN4, SAN5](#san4-san5)
  - [SAN11](#san11)
    - [檔案格式](#檔案格式)
  - [SAN12](#san12)
    - [數據](#數據)
    - [相關檔案](#相關檔案)
  - [SAN13](#san13)
  - [SAN14](#san14)

## 系列共通

- 楊奉從七代開始就作為顏排名第一位，其次是張飛與關羽。一直到 12 代（13 之後未確認）
- 八代開始分大小圖
- 八代至 11 代的大圖多半還是頭像或胸像，12 代則是半身像（或及腰像）
- 13代開始有一個人多畫像（年輕壯年、文官武將、低位高位）

### 各代用語

- 臉譜: 4, 5
- 相貌: 7, 8
- 容貌: 9, 10, 11, 12, 13
- 臉孔: 14 (又稱, 臉部畫像)
- (缺6代)

### 尺寸代號

- XS: Extra Small
- S: Small
- M: Medium
- L: Large
- XL: Extra Large

### 工具或參考頁面

- [Van’s House](http://pigspy.ysepan.com/)
- 日本製編輯器 [Vector： トップ / ダウンロード / WindowsMe/98/95用ソフト / ゲーム / ユーティリティ / 市販ゲーム等の設定変更 / 光栄用](https://www.vector.co.jp/vpack/filearea/win95/game/tool/edit/koei/)
- ニコニコ動画 歴史戦略ゲー プレイ動画まとめwiki
  - LOS Face Editor [顔画像エディタ - 覚醒支援システム【カギヤマキナ】 総合まとめwiki - atwiki（アットウィキ）](https://w.atwiki.jp/losystem/pages/34.html), 支援 天下創世、革新、天道、三國志12
  - LOS MSG Editor [列伝エディタ - 覚醒支援システム【カギヤマキナ】 総合まとめwiki - atwiki（アットウィキ）](https://w.atwiki.jp/losystem/pages/29.html)
  - [顔グラ変更について - ニコニコ動画 歴史戦略ゲー プレイ動画まとめwiki - atwiki（アットウィキ）](https://w.atwiki.jp/nicosangokushi/pages/134.html)
  - [顔グラ変更について（三国志８以前） - ニコニコ動画 歴史戦略ゲー プレイ動画まとめwiki - atwiki（アットウィキ）](https://w.atwiki.jp/nicosangokushi/pages/794.html)
  - [顔グラ変更について（信長の野望） - ニコニコ動画 歴史戦略ゲー プレイ動画まとめwiki - atwiki（アットウィキ）](https://w.atwiki.jp/nicosangokushi/pages/777.html)
- LS11 格式
  - numdisp 的發問帖 [请问光荣系列的 LS11 格式 - 设计与修改 - 轩辕春秋文化论坛](http://www.xycq.online/forum/viewthread.php?tid=206168&page=1&showoldetails=yes)
  - 後來 numdisp 寫了篇 PDF 介紹 LS11, 我的主要實現均是參考自該篇 PDF

### 頭像檔命名規範

```sh
{作品代號}_{平台}_F{尺寸}{編號}_{附加資訊}.png

編號由 1 開始, 四碼 (0001~9999)

範例：
    SAN1_PC98_F0001.png
    SAN1_DOS_F0001.png
    SAN2_DOS_F0001_TW.png
```

#### 代號

- `F`: 顏 Face (不用 Kao, 遊戲後期命名都改 Face)
- `I`: Item 道具
- `E`: Event 事件
- `M`: Map 地圖
- `U`: Unit 單位

## SAN1, SAN2

- Steam 版 SAN1, SAN2 用的是 PC9801 的版本
- SAN1 DOS 版(Eng.) 與 Steam/PC98 版，除了顏色的差別外(4色 vs 8色), 顏良(No.41)頭盔也是一個差別
- 上面兩個版本在大眾臉武將處的空白也有差異
- SAN2 DOS 版 與 Steam/PC98 版，人物大致相同但有差異，前者感覺大小比較一致
- SAN2 DOS 版 與 Steam/PC98 版，關羽的帽子色不同，張飛的帽子則有明顯顏色不同（前藍後紅）

### 檔案

- SAN1: `PICDATA.DAT`, 檔案後面有其他圖
- SAN2: `KAODATA.DAT`

## SAN4, SAN5

## SAN11

- [香港三國志 - \[教學\]三國志11頭像、暴擊圖導入/導出(連圖解)](http://hksan.net/main/article.php?/196)

### 檔案格式

解析資料到一半時，發現檔案內常出現 `WFTX0010`，
Google 了一下 `"wftx0010"`, 只找到 [การถอดรหัสไฟล์ (เช่น. Map, Data) - Programming Talk - ParadizeX Forum][progtalk] 這一個結果。
翻譯之後內容跟想像的差不多，雖沒有突破性的收穫，但自己的推測有人驗證也是感覺蠻不錯的。

[progtalk]: https://skjune.com/forum/topic/621-%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%96%E0%B8%AD%E0%B8%94%E0%B8%A3%E0%B8%AB%E0%B8%B1%E0%B8%AA%E0%B9%84%E0%B8%9F%E0%B8%A5%E0%B9%8C-%E0%B9%80%E0%B8%8A%E0%B9%88%E0%B8%99-map-data/

## SAN12

### 數據

- 遊戲中統計
  - 編輯武將容貌時有下拉式選單可選，每項最多10頁，從中可計算總頭像數
  - 新武將 139 張，包括古武將與日本戰國
  - 基本人物 611，包含傳令、童子等 NPC，以及異民族的首領、武將
  - 特別版 42，有關羽諸葛呂布等角色的特殊造型、武則天，以及無雙人物
  - **Total 792**

- 檔案中統計 (基於 steam 版)
  - `resfile` 674
  - `spkao` 35
  - `addkao00`, `addkao00pk` 4
  - `addkao20`, `addkao20pk` 180
  - **Total 893**

- [信長のWiki](https://www.nobuwiki.org/san/cg/12)
  - **收錄了 三國志12 人物頭像 933 張**，
  - 其中包含 40 張比較二次元風格（龍狼傳等）的頭像
    - 第二頁 21 張，第三頁 19 張
  - 從檔名推測圖檔可能源自 RPGViewer 的匯出
  - 與檔案中統計相差 40 張，剛好就是二次元風格的部分

- 其他補充
  - 遊戲中的武將名鑑列表有 588 位
  - 三國志武將大名鑑 書中刊載 12 代有武將 708 人
- 二次元風格 タイアップ (tie up)
  - 編號 1106-1126 為 三國志魂 (荒川弘) 連動
  - 關於 `addkao21` 19張的合作情報: [三國志12 タイアップ情報](http://www.gamecity.ne.jp/sangokushi/12wpk/netplay/tieup1.html)
    - 龍狼傳 13-16 四張
    - みんなの呉 18,19 兩張, 孫權 魯肅
    - 漢晉春秋司馬仲達伝三国志　しばちゅうさん 1-3 三張。看畫風後面也可能是
    - 還有10張...

### 相關檔案

Steam 版存檔位置：`Users\系統使用者名稱\Documents\KOEI\35th\San12WPK_TC\`
（跟網路上查到的資料不同，找好久）

- RPGViewer 可讀取下列檔案（與頭像有關）
  - `resfiles_01.bin`: 基本頭像。表定 2000 張，實際有 674 張。頭像不連續。檔案也包含物品圖。
  - `resfiles_addkao00.bin`: 4張頭像。
  - `resfiles_addkao00_pk.bin`: 同上。
  - `resfiles_addkao20.bin`: 180 張頭像。
  - `resfiles_addkao20_pk.bin`: 同上。
  - `resfiles_addkao21_pk.bin`: 無頭像。有 19 個空位，應該是信長のWiki第二頁的 19 張二次元頭像。
  - `resfiles_spkao0_pk.bin`: 35 張頭像。以無雙角色和主要角色壯年版為主。
  - 以上均包含所有尺寸在一個檔案中。

- 以下檔案是 RPGViewer 不讀取但也跟頭像有關的檔案
  - 下列檔案含 695 張個尺寸頭像，對應檔案 `resfiles_01.bin` 的 674 張與 21 張二次元頭像
    - `Data\KAO_F_M.S12` 推測是 48x60 頭像檔 (Medium)
    - `Data\KAO_F_S.S12` 推測是 32x32 頭像檔 (Small)
    - `Data\KAO_W_L.S12` 推測是 360x512 半身像 (Large)
    - `Data\KAO_W_S.S12` 推測是 90x128 半身像 (Small)
    - `Data\KAODATA.S12`: 作用不清，只有 266 bytes
  - 下列檔案含 4 張各尺寸頭像，對應檔案 `resfiles_addkao00`
    - `AddKao00\ADD00_KAO_F_M.S12`
    - `AddKao00\ADD00_KAO_F_S.S12`
    - `AddKao00\ADD00_KAO_W_L.S12`
    - `AddKao00\ADD00_KAO_W_S.S12`
    - `AddKao00\ADD00.dat` 頭像資料 與 頭像ID 的對應
  - 下列檔案含 180 張各尺寸頭像，對應檔案 `resfiles_addkao20`
    - `PK\AddKao20\ADD20_KAO_F_M.S12`
    - `PK\AddKao20\ADD20_KAO_F_S.S12`
    - `PK\AddKao20\ADD20_KAO_W_L.S12`
    - `PK\AddKao20\ADD20_KAO_W_S.S12`
    - `PK\AddKao20\ADD20.dat` 頭像資料 與 頭像ID 的對應
  - 下列檔案含 19 張各尺寸頭像，對應檔案 `resfiles_addkao21`，有龍狼傳等二次元三國角色
    - `PK\AddKao21\ADD21_KAO_F_M.S12`
    - `PK\AddKao21\ADD21_KAO_F_S.S12`
    - `PK\AddKao21\ADD21_KAO_W_L.S12`
    - `PK\AddKao21\ADD21_KAO_W_S.S12`
    - `PK\AddKao21\ADD21.dat` 頭像資料 與 頭像ID 的對應
  - 下列檔案含 35 張各尺寸頭像，對應檔案 `resfiles_spkao0`
    - `PK\AddKao21\SP0_KAO_F_M.S12`
    - `PK\AddKao21\SP0_KAO_F_S.S12`
    - `PK\AddKao21\SP0_KAO_W_L.S12`
    - `PK\AddKao21\SP0_KAO_W_S.S12`
    - `PK\AddKao21\SP0.dat` 頭像資料 與 頭像ID 的對應

## SAN13

推測數量：1467

以下取自「『三國志13』武將ＣＧ追加工具」的 README file (英文取自英文版 README)

> 3.『三國志13』中所使用的武將ＣＧ，每個武將皆備有5張大小不同（特大、大、中、小、極小）的圖像。
> ‧特大(Extra-large) 　…　1024x1024像素：使用於戰法演出、絆成立等特定事件。
> ‧大(Large) 　　　　　…　 633x 900像素：使用於情報畫面、武將對話等。
> ‧中(Medium)　　　　　…　 186x  90像素：使用於出征畫面、都市情報畫面等。
> ‧小(Small) 　　　　　…　　96x　96像素：使用於武將畫面、內政對話方塊畫面等。
> ‧極小(Extra-small) 　…　　72x　72像素：使用於相關圖、標頭情報等。

## SAN14

推測數量：1446, 全14代總計推測 10450

以下取自「『三國志14』武將ＣＧ追加工具」的 README file (英文取自英文版 README)

> ‧大(Large) 　　…　1024x1024像素：使用於發動戰法時。
> ‧中(Medium)　　…　 633x 900像素：使用於事件、武將詳情畫面等。
> ‧小(Small) 　　…　 512x 512像素：使用於各種圖示以及獨特戰法演出等。

以下取自「武將 CG 追加工具」的使用說明書

```txt
A＝事件與武將詳細畫面等（636×900px）
B＝出陣時等表示的武將圖示（512×512px）
C＝戰法發動時的武將照片（1024×1024px）
```
