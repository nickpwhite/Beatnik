import React, { Component } from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';
import Converter from './Converter.js';
import Header from './Header.js';
import Home from './Home.js';
import './App.css';

class App extends Component {
  render() {
    console.log(this.props.location);
    return (
      <div>
        <Header />
        <Switch>
          <Route path="/index" component={ Home } />
          <Route path="/convert" component={ Converter } />
          <Redirect exact={true} from="/" to="/index" />
        </Switch>
      </div>
    );
  }
}

export default App;
