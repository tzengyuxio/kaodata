import {
  kohryukiFaceNames,
  san2FaceNames,
  san3FaceNames,
  suikodenFaceNames,
} from './faceNames';
import palettes from './palettes';

const gameInfos = {
  san2: {
    id: 'san2',
    name: '三國志II',
    filename: 'kaodata.dat',
    width: 64,
    height: 80,
    palette: palettes.default.codes,
    count: -1,
    halfHeight: true,
    faceNames: san2FaceNames,
  },
  san3: {
    id: 'san3',
    name: '三國志III',
    filename: 'kaodata.dat',
    width: 64,
    height: 80,
    palette: palettes.san3.codes,
    count: -1,
    halfHeight: false,
    faceNames: san3FaceNames,
  },
  san4: {
    id: 'san4',
    name: '三國志IV',
    filename: 'kaodatap.s4',
    width: 64,
    height: 80,
    palette: palettes.san4.codes,
    count: -1, // 701 or 818
    halfHeight: false,
    faceNames: [],
  },
  san5: {
    id: 'san5',
    name: '三國志V',
    filename: 'kaodata.s5',
    width: 64,
    height: 80,
    palette: palettes.san5.codes,
    count: -1,
    halfHeight: false,
    faceNames: [],
  },
  kohryuki: {
    id: 'kohryuki',
    name: '項劉記',
    filename: 'kao.kr1',
    width: 64,
    height: 80,
    palette: palettes.kohryuki.codes,
    count: -1,
    halfHeight: false,
    faceNames: kohryukiFaceNames,
  },
  suikoden: {
    id: 'suikoden',
    name: '水滸傳・天命之誓',
    filename: 'kaoibm.dat',
    width: 64,
    height: 80,
    palette: palettes.default.codes,
    count: -1,
    halfHeight: true,
    faceNames: suikodenFaceNames,
  },
};

export default function getGameInfos() {
  return gameInfos;
}
