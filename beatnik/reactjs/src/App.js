import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import Converter from './Converter.js';
import Header from './Header.js';
import Home from './Home.js';
import './App.css';

class App extends Component {
  render() {
    return (
      <div>
        <Header />
        <Route path="/index" component={ Home } />
        <Route path="/convert" component={ Converter } />
      </div>
    );
  }
}

export default App;
