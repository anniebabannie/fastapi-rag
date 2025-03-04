import React from 'react';
import './Loader.css'; // Ensure you have a separate CSS file for loader styles

const Loader = () => (
  <div className="bg-gray-100 flex px-5 py-3 rounded-lg">
    <div className="typing-loader">
      <span className="dot"></span>
      <span className="dot"></span>
      <span className="dot"></span>
    </div>
  </div>
);

export default Loader; 