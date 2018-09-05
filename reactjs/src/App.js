import React, { Component } from 'react';
import mixpanel from 'mixpanel-browser';
import Header from './Header.js';
import Home from './Home.js';
import Modal from './TrackingModal.js';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);

    const tracking = localStorage.getItem("tracking") === "true";
    mixpanel.init(process.env.REACT_APP_MIXPANEL_TOKEN, { opt_out_tracking_by_default: !tracking });

    this.closeModal = this.closeModal.bind(this);
    this.handleModalNo = this.handleModalNo.bind(this);
    this.handleModalYes = this.handleModalYes.bind(this);

    this.state = {
      modalOpen: localStorage.getItem("tracking") === null
    };
  }

  closeModal() {
    this.setState({
      modalOpen: false
    })
  }

  handleModalNo() {
    this.closeModal();
    localStorage.setItem("tracking", false);
  }

  handleModalYes() {
    this.closeModal();
    localStorage.setItem("tracking", true);
    mixpanel.opt_in_tracking();
  }

  render() {
    return (
      <div>
        <Header />
        <Home />
        <Modal show={ this.state.modalOpen }
          onNo={this.handleModalNo}
          onYes={this.handleModalYes} />
      </div>
    );
  }
}

export default App;
