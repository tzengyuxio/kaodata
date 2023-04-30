import PropTypes from 'prop-types';
import React from 'react';
import {useTranslation} from 'react-i18next';

export default function TabLabel(props) {
  const {t} = useTranslation();

  return <div className="tab-label">{t(props.labelKey)}</div>;
}
TabLabel.propTypes = {
  labelKey: PropTypes.string.isRequired,
};
