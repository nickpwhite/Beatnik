import React, { Component } from 'react';
import ConvertForm from './ConvertForm.js';
import MusicList from './MusicList.js';

class Converter extends Component {
  constructor(props) {
    super(props);

    this.updateMusic = this.updateMusic.bind(this);

    this.state = {
      music: []
    };
  }

  updateMusic(music) {
    this.setState({ music });
    console.log(this.state);
  }

  render() {
    return (
      <div className="content">
        <div className="flex-row">
          <ConvertForm onSubmit={ this.updateMusic } />
        </div>
        <div className="flex-row">
          <MusicList music={ this.state.music } />
        </div>
      </div>
    )
  }
}

export default Converter;
