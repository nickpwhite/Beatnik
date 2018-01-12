import React, { Component } from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';
import mixpanel from 'mixpanel-browser';
import Converter from './Converter.js';
import Header from './Header.js';
import Home from './Home.js';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);

    mixpanel.init(process.env.REACT_APP_MIXPANEL_TOKEN);
  }

  render() {
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
