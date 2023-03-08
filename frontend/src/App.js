import React from 'react';
import './App.css';

import Header from './components/Header/Header';
import ChecksList from './components/CheckList/ChecksList';


function App() {

    return (
      <div className="App">
        <Header/>
        <ChecksList/>
      </div>
    );
}

export default App;
