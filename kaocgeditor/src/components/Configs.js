import React from 'react';

import ColorPalette from './ColorPalette';
import TabLabel from './TabLabel';

export default function Configs() {
  return (
    <div className="configuration outline-block child">
      <TabLabel labelKey="tabs.color" />
      {/* <DithKernSelect /> */}
      <ColorPalette />
    </div>
  );
}
