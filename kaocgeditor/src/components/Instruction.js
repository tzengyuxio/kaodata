import Mark from 'mark.js';
import React, {useEffect, useRef} from 'react';
import {useTranslation} from 'react-i18next';

export default function Instruction() {
  const steps = [
    'instruction.step1',
    'instruction.step2',
    'instruction.step3',
    'instruction.step4',
    'instruction.step5',
    'instruction.step6',
    'instruction.step7',
    'instruction.step8',
  ];
  const nodeRef = useRef(null);
  const {t} = useTranslation();

  useEffect(() => {
    const instance = new Mark(nodeRef.current);
    instance.markRegExp(/「(.*?)」/g, {
      element: 'span',
      className: 'red',
    });
  });

  return (
    <>
      <div>{t('instruction.title')}</div>
      <ol ref={nodeRef}>
        {React.Children.map(
            steps.map((step) => t(step)),
            (child, i) => (
              <li key={i}>{child}</li>
            ),
        )}
      </ol>
    </>
  );
}
