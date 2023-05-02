import i18n from 'i18next';
import {initReactI18next} from 'react-i18next';

// the translations
// (tip move them in a JSON file and import them,
// or even better, manage them separated from your code: https://react.i18next.com/guides/multiple-translation-files)
const resources = {
  zh_tw: {
    translation: {
      'Welcome to React': 'Welcome to React and react-i18next',
      'title': '顏ＣＧ編輯器',
      'tabs': {
        game: '遊戲',
        color: '色彩',
        substitute: '替換',
      },
      'buttons': {
        reset: '重設',
        save: '下載更新',
        upload: '選擇檔案',
        substitute: '替換',
      },
      'select-game': '選擇遊戲',
      'label': {
        'dith-kern': '抖色演算法：',
      },
      'instruction': {
        title: '使用說明：',
        step1: '先在左上角選單選擇遊戲',
        step2: '按下「選擇檔案」按鈕上傳遊戲頭像檔',
        step3: '讀取完成之後會出現頭像列表。',
        step4: '將想要放進遊戲裡的頭像拖拉至替換區域。可使用照片或是其他圖片，寬高比例 4:5 為佳，超過的話會自動裁切。',
        step5: '在下方頭像列表中選取要替換的頭像，按下「替補」按鈕',
        step6: '重複 步驟 4. 5., 可替換多個頭像。被替換的頭像會以背景色特別標註。',
        step7: '完成替換後，按下「下載更新」按鈕，即可下載檔案。',
        step8: '將下載的檔案放到遊戲資料夾中，替換檔名，進去遊戲後便可看到替換的頭像。',
        upload_file: '請選擇遊戲檔案 `{{filename}}` 上傳。',
        no_download: '此遊戲目前只支援瀏覽頭像，尚不支援「下載更新」。',
        select_game: '請先選擇遊戲，並上傳檔案。',
      },
    },
  },
  zh_cn: {
    translation: {
      'Welcome to React': 'Bienvenue à React et react-i18next',
      'title': '颜ＣＧ编辑器',
      'tabs': {
        game: '游戏',
        color: '色彩',
        substitute: '替换',
      },
      'buttons': {
        reset: '重设',
        save: '下载更新',
        upload: '选择档案',
        substitute: '替补',
      },
      'select-game': '选择游戏',
      'label': {
        'dith-kern': '抖色算法：',
      },
      'instruction': {
        title: '使用说明：',
        step1: '先在左上角菜单选择游戏',
        step2: '按下「选择档案」按钮上传游戏头像文件',
        step3: '读取完成之后会出现头像列表。',
        step4: '将想要放进游戏里的头像拖拉至替换区域。可使用照片或是其他图片，宽高比例 4:5 为佳，超过的话会自动裁切。',
        step5: '在下方头像列表中选取要替换的头像，按下「替补」按钮',
        step6: '重复 步骤 4. 5., 可替换多个头像。被替换的头像会以背景色特别标注。',
        step7: '完成替换后，按下「下载更新」按钮，即可下载文件。',
        step8: '将下载的档案放到游戏资料夹中，替换档名，进去游戏后便可看到替换的头像。',
        upload_file: '请选择游戏档案 `{{filename}}` 上传。',
        no_download: '此游戏目前只支持浏览头像，尚不支持「下载更新」。',
        select_game: '请先选择游戏，并上传档案。',
      },
    },
  },
  ja: {
    translation: {
      'Welcome to React': 'Bienvenue à React et react-i18next',
      'title': '顔ＣＧエディター',
      'tabs': {
        game: 'ゲーム',
        color: '色',
        substitute: '置換',
      },
      'buttons': {
        reset: 'リセット',
        save: '更新をダウンロード',
        upload: 'ファイルを選択',
        substitute: '置換',
      },
      'select-game': 'ゲームを選択',
      'label': {
        'dith-kern': 'ディザリング：',
      },
      'instruction': {
        title: '使用説明：',
        step1: '左上のメニューでゲームを選択します',
        step2: '「ファイルを選択」ボタンを押してゲームのアバターをアップロードします',
        step3: '読み込みが完了すると、アバターリストが表示されます。',
        step4:
                    'ゲームに入れたいアバターを置換エリアにドラッグアンドドロップします。' +
                    '写真や他の画像を使用できます。アスペクト比4：5が最適です。それ以上の場合は、自動的にトリミングされます。',
        step5: '下のアバターリストから置換するアバターを選択し、「置換」ボタンを押します',
        step6: 'ステップ4. 5.を繰り返します。複数のアバターを置換できます。置換されたアバターは背景色で特別にマークされます。',
        step7: '置換が完了したら、「更新をダウンロード」ボタンを押して、ファイルをダウンロードします。',
        step8:
                    'ダウンロードしたファイルをゲームフォルダに入れて、ファイル名を置き換えると、' +
                    'ゲームに入って置き換えたアバターが表示されます。',
        upload_file:
                    'ゲームファイル `{{filename}}` を選択してください。',
        no_download:
                    'このゲームは現在、アバターの閲覧のみをサポートしており、「更新をダウンロード」はサポートしていません。',
        select_game:
                    'ゲームを選択して、ファイルをアップロードしてください。',
      },
    },
  },
};

i18n.use(initReactI18next) // passes i18n down to react-i18next
    .init({
      resources,
      lng: 'zh_tw', // language to use, more information here: https://www.i18next.com/overview/configuration-options#languages-namespaces-resources
      // you can use the i18n.changeLanguage function to change the language manually: https://www.i18next.com/overview/api#changelanguage
      // if you're using a language detector, do not define the lng option

      interpolation: {
        escapeValue: false, // react already safes from xss
      },
    });

export default i18n;
