import { detect } from 'detect-browser';
import React, { Component } from 'react';

class Header extends Component {
  constructor(props) {
    super(props)

    this.state = {
      ext_url: this.get_ext_url()
    };
  }

  get_ext_url() {
    const browser = detect();

    switch (browser && browser.name) {
      case 'chrome':
        return 'https://chrome.google.com/webstore/detail/beatnik/imhhnehiopfkoogocbgihgepdkedbcfi?hl=en-US';
      case 'firefox':
        return 'https://addons.mozilla.org/en-US/firefox/addon/beatnik-app/';
      default:
        return null;
    }
  }

  render() {
    return (
      <header className="header">
        <div className="flex-row">
          <div className="col-50">
            <a href={process.env.REACT_APP_HOME} className="title"><h1>Beatnik</h1></a>
          </div>
          { this.state.ext_url && 
            <div className="col-50 subtitle">
              <a href={ this.state.ext_url } target="_blank" className="title"><h2>Get the extension</h2></a>
            </div>
          }
        </div>
      </header>
    )
  }
}

export default Header;
