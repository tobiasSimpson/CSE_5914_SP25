import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

import React from 'react';
import FrontPage from './FrontPage';
import HomePage from './HomePage';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom'

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<FrontPage />} />
        <Route path="/home" element={<HomePage />} />
      </Routes>
    </Router>
    
  );
}

export default App;
