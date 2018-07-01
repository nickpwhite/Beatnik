import React, { Component } from 'react';
import mixpanel from 'mixpanel-browser';
import ConvertForm from './ConvertForm.js';
import MusicList from './MusicList.js';
import Spinner from './Spinner.js';

class Converter extends Component {
  constructor(props) {
    super(props);

    mixpanel.track("View Converter");

    this.state = {
      loading: false,
      music: []
    };

    this.updateMusic = this.updateMusic.bind(this);
    this.setLoading = this.setLoading.bind(this);
  }

  setLoading() {
    this.setState({
      loading: true,
      music: []
    });
  }

  updateMusic(music) {
    if (music.length > 0) {
      mixpanel.track("Load Music", music[0].fields);
    }
    this.setState({ 
      loading: false,
      music: music 
    });
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
          <ConvertForm onBeforeSubmit={ this.setLoading } onSubmit={ this.updateMusic } query={ this.props.location.search } />
        </div>
        <Spinner loading={ this.state.loading } />
        <MusicList music={ this.state.music } />
      </div>
    )
  }
}

export default Converter;
