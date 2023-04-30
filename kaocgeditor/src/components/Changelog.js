import React, {useEffect, useState} from 'react';

export default function Changelog() {
  const [logs, setLogs] = useState([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    fetch('/kaocgeditor/changelog.json')
        .then((response) => response.json())
        .then((data) => setLogs(data))
        .catch((err) => console.log(err));
  }, []);

  const toggleOpen = () => setOpen(!open);

  const listBoxStyle = {
    position: 'fixed',
    bottom: '100px',
    right: '20px',
    // height: '200px',
    // width: '300px',
    overflow: 'auto',
    display: open ? 'block' : 'none',
    opacity: 0.84,
    backgroundColor: '#fffff0',
    border: '1px solid #00000f',
  };

  return (
    <div style={{position: 'relative'}}>
      {/* <button onClick={toggleOpen}>更新日誌</button> */}
      <i
        className="fa-solid fa-clipboard-list changeLogIcon"
        onClick={toggleOpen}
      ></i>
      <div id="changelog" style={listBoxStyle}>
        {logs.map((day) => (
          <div key={day.date} className="changelog-day">
            <h3 className="changelog-date">{day.date}</h3>
            {day.items.map((item) => (
              <div key={item.title} className="changelog-item">
                <h4 className="changelog-title">
                  {item.title}
                </h4>
                <div className="changelog-description">
                  {item.description}
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
