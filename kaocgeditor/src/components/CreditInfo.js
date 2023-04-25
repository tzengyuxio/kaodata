import React from 'react';
import Changelog from './Changelog.js';

export default function CreditInfo() {
  return (
    <div id="credit-info" className="outline-block child">
      <Changelog />
      <div id="credits">
                設計製作
        <br />
        <a href="https://tzengyuxio.me">Tzeng Yuxio</a>
        <br />
        <br />
                測試協力
        <br />
        <a href="https://github.com/reganlu007/">ReganLu</a>
        <br />
        <br />
                更多光榮遊戲資料
        <br />
        <a
          href="https://koei-wiki.tzengyuxio.me/"
          style={{marginTop: '1rem'}}
        >
                    光栄遊戲百科事典
        </a>
      </div>
      <a
        href="https://www.buymeacoffee.com/tzengyuxio"
        target="_blank"
        rel="noreferrer"
      >
        <img
          src="https://cdn.buymeacoffee.com/buttons/v2/default-red.png"
          alt="Buy Me A Coffee"
          style={{
            height: '48px',
            width: '168px',
            marginTop: '1rem',
          }}
        />
      </a>
    </div>
  );
}
