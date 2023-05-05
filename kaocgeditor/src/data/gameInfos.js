import {
  kohryukiFaceNames,
  lempeFaceNames,
  san2FaceNames,
  san3FaceNames,
  san4FaceNames,
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
    palette: palettes.default,
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
    palette: palettes.san3,
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
    palette: palettes.san4,
    count: -1, // 701 or 818
    halfHeight: false,
    faceNames: san4FaceNames,
  },
  san5: {
    id: 'san5',
    name: '三國志V',
    filename: 'kaodata.s5',
    width: 64,
    height: 80,
    palette: palettes.san5,
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
    palette: palettes.kohryuki,
    count: -1,
    halfHeight: false,
    faceNames: kohryukiFaceNames,
  },
  lempe: {
    id: 'lempe',
    name: '拿破崙',
    filename: 'kaodata.dat',
    width: 64,
    height: 80,
    palette: palettes.default,
    count: -1,
    halfHeight: true,
    faceNames: lempeFaceNames,

  },
  suikoden: {
    id: 'suikoden',
    name: '水滸傳・天命之誓',
    filename: 'kaoibm.dat',
    width: 64,
    height: 80,
    palette: palettes.default,
    count: -1,
    halfHeight: true,
    faceNames: suikodenFaceNames,
  },
};

export default function getGameInfos() {
  return gameInfos;
}
