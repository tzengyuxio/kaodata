import React, {useEffect, useState} from 'react';

export default function Changelog() {
  const [logs, setLogs] = useState([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    fetch('/changelog.json')
        .then((response) => response.json())
        .then((data) => setLogs(data));
  }, []);

  const toggleOpen = () => setOpen(!open);

  const listBoxStyle = {
    position: 'fixed',
    top: '50px',
    right: '20px',
    height: '200px',
    width: '300px',
    overflow: 'auto',
    display: open ? 'block' : 'none',
    opacity: .84,
    backgroundColor: '#fffff0',
    border: '1px solid #00000f',
  };

  return (
    <div style={{position: 'relative'}}>
      <button onClick={toggleOpen}>更新日誌</button>
      <div style={listBoxStyle}>
        <ul>
          {logs.map((log) => (
            <li key={log.id}>{log.content}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
