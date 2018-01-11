import React, { Component } from 'react';
import apple_logo from './images/apple_logo.png';
import gpm_logo from './images/gpm_logo.png';
import soundcloud_logo from './images/soundcloud_logo.png';
import spotify_logo from './images/spotify_logo.png';

class Music extends Component {
  constructor(props) {
    super(props);

    this.openLink = this.openLink.bind(this);
  }

  openLink(href) {
    window.open(href, "_blank");
  }

  render() {
    const music = this.props.music;
    const album = music.album && <h3 className="music-info">{ music.album }</h3>
    const apple_url = music.apple_url && 
      <li>
        <button type="button" 
                className="apple" 
                onClick={ this.openLink.bind(this, music.apple_url) }
        >
          <div className="flex-row">
            <div className="col-25">
              <img alt="" className="service-logo" src={ apple_logo } />
            </div>
            <div className="col-75 service-description">
              Apple Music
            </div>
          </div>
        </button>
      </li>;
    const gpm_url = music.gpm_url && 
      <li>
        <button type="button" 
                className="google"
                onClick={ this.openLink.bind(this, music.gpm_url) }
        >
          <div className="flex-row">
            <div className="col-25">
              <img alt="" className="service-logo" src={ gpm_logo } />
            </div>
            <div className="col-75 service-description">
              Google Play Music
            </div>
          </div>
        </button>
      </li>;
    const soundcloud_url = music.soundcloud_url && 
      <li>
        <button type="button" 
                className="soundcloud"
                onClick={ this.openLink.bind(this, music.soundcloud_url) }
        >
          <div className="flex-row">
            <div className="col-25">
              <img className="service-logo" src={ soundcloud_logo } />
            </div>
            <div className="col-75 service-description">
              Soundcloud
            </div>
          </div>
        </button>
      </li>;
    const spotify_url = music.spotify_url && 
      <li>
        <button type="button" 
                className="spotify"
                onClick={ this.openLink.bind(this, music.spotify_logo) }
        >
          <div className="flex-row">
            <div className="col-25">
              <img className="service-logo" src={ spotify_logo } />
            </div>
            <div className="col-75 service-description">
              Spotify
            </div>
          </div>
        </button>
      </li>;
    return (
      <div className="flex-row music-container">
        <div className="flex-row col-100">
          <div className="flex-col">
            <h2 className="music-info">{ music.name }</h2>
            <h3 className="music-info">{ music.artist }</h3>
            { album }
          </div>
        </div>
        <div className="flex-row col-100">
          <div className="flex-row col-33">
            <img className="artwork" src={ music.artwork } alt="Album cover" />
          </div>
          <div className="flex-row col-66">
            <div className="flex-col">
              <ul>
                { apple_url }
                { gpm_url }
                { soundcloud_url }
                { spotify_url }
              </ul>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Music;
