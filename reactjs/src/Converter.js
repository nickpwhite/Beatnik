import React, { Component } from 'react';
import mixpanel from 'mixpanel-browser';
import ConvertForm from './ConvertForm.js';
import MusicList from './MusicList.js';

class Converter extends Component {
  constructor(props) {
    super(props);

    mixpanel.track("View Converter");

    this.state = {
      music: []
    };

    this.updateMusic = this.updateMusic.bind(this);
  }

  updateMusic(music) {
    mixpanel.track("Load Music", music[0].fields);
    this.setState({ music });
  }

  render() {
    const params = new URLSearchParams(this.props.query);

    if (params.get('q') !== '') {
      const autoRedirect = localStorage.getItem("autoRedirect");
      if (autoRedirect && this.state.music.length > 0 && this.state.music[0].fields[autoRedirect]) {
        window.open(this.state.music[0].fields[autoRedirect], "_self");
        return false;
      }
    }

    return (
      <div className="content">
        <div className="flex-row">
          <ConvertForm onSubmit={ this.updateMusic } query={ this.props.location.search } />
        </div>
        <MusicList music={ this.state.music } />
      </div>
    )
  }
}

export default Converter;
