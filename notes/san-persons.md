# 三國志 人物資料 研究筆記

## SAN4

下面檔案包含伊籍 (0x9444ADA5)

- SNDATA.S4
  - 名字 offset: 30892, 50637, 70672, 90527, 144632, 163447, 195512
  - 能力 offset: 26455, 46200, 65965, 86360, 140675, 159240, 184465
- TAIKI.S4
- 張飛, 關羽 SNDATA.S4, offsets
  - 10770, 9210
  - 28935, 27035
- 從統帥起找能力的 offset -> **間隔 20 bytes**
  - 關羽(0x64625241) 9209 (kao: 1)
  - 華雄 9189
  - 夏侯惇(0x5E603E) 9169 (kao: 6)
- 從名字找起的 offset -> **間隔 30 bytes**, 第 21 bytes 為顏編號
  - 華雄 13067
  - 關羽 13097
- 顏ID (名字, byte20, 21, 22)
  - 關羽 ________ 00 01 00
  - 華雄 ________ 00 07 00
  - 呂凱 95649FB2 00 E7 00
  - 劉巴 A6AB9351 00 03 F8
  - 呂義 9564A399 00 47 F0

## 參考來源

- 這邊有 1~11 代的能力一覽表：[楊奉とは (ヨウホウとは) \[単語記事\] - ニコニコ大百科](https://dic.nicovideo.jp/a/%E6%A5%8A%E5%A5%89)
- 三國志11 攻略 WIKI: [楊奉 - 三國志11攻略wiki - atwiki（アットウィキ）](https://w.atwiki.jp/sangokushi11/pages/795.html)
- 三國志13 攻略 WIKI: [楊奉 - 三国志13 攻略 WIKI](http://sangokushi13wiki.wiki.fc2.com/wiki/%E6%A5%8A%E5%A5%89)
- [火間虫入道-信長の野望 蒐集者の庭-](http://hima.que.ne.jp/)
  - 信長之野望系列
  - 太閤立志傳系列
  - 三國志 1~7, 12
  - 拿破崙
- 有天翔記~創造武將一覽 EXCEL [天翔記.jp](https://xn--rssu31gj1g.jp/)
- 有三國志10的改造資訊 [三国志Ⅹ改造スレ３](https://game13.5ch.net/test/read.cgi/gamehis/1098017701/)

## 其他註記

- 光榮美術館目前 39 作 (2023/3/1), koei-wiki 已整理 27 作，但尚未完整發布

## 人物解析步驟

```py
    # 定義 'stack unpack fmt' for PersonRaw
    # 定義 PersonRaw 資料結構
    # 定義 Person 資料結構
    # func of PersonRaw -> Person
    #
    # 定義 headers
    # new table and add columns with header
    #
    # 宣告 persons
    # with open file:
    #     read data (maybe need to join with parts)
    #     pr = PersonRaw._make(unpack(fmt, data))
    #     p = convert(pr)
    #     persons.append(p)
    #
    # for p in persons:
    #     add row to table, or
    #     output as csv
    # print summary of persons
```
