import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Header extends Component {
  render() {
    return (
      <header className="header">
        <div className="flex-row">
          <div className="col-25">
            <Link to="/index" className="title"><h1>Beatnik</h1></Link>
          </div>
          <div className="col-25 subtitle">
            <Link to="/convert" className="title"><h2>Link Converter</h2></Link>
          </div>
          <div className="col-25 subtitle">
            <a href="/" className="title"><h2>Get the extension</h2></a>
          </div>
        </div>
      </header>
    )
  }
}

export default Header;
