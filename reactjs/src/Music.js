import React, { Component } from 'react';
import mixpanel from 'mixpanel-browser';
import Modal from './RedirectModal';
import apple_logo from './images/apple_logo.png';
import gpm_logo from './images/gpm_logo.png';
import soundcloud_logo from './images/soundcloud_logo.png';
import spotify_logo from './images/spotify_logo.png';

class Music extends Component {
  constructor(props) {
    super(props);

    this.appleMusicText = "Apple Music";
    this.gpmText = "Google Play Music";
    this.soundcloudText = "Soundcloud";
    this.spotifyText = "Spotify";

    this.closeModal = this.closeModal.bind(this);
    this.handleModalNever = this.handleModalNever.bind(this);
    this.handleModalNo = this.handleModalNo.bind(this);
    this.handleModalYes = this.handleModalYes.bind(this);

    this.openLink = this.openLink.bind(this);

    this.state = {
      modalOpen: false
    };
  }

  closeModal() {
    this.setState({
      modalOpen: false
    });
  }

  handleModalNever() {
    mixpanel.track("Set Redirect", { 'value': "none" });
    this.closeModal();
    localStorage.setItem("autoRedirect", "none");
    window.open(this.state.href, "_blank");
  }

  handleModalNo() {
    this.closeModal();
    window.open(this.state.href, "_blank");
  }

  handleModalYes() {
    mixpanel.track("Set Redirect", { 'value': this.state.modalType });
    this.closeModal();
    localStorage.setItem("autoRedirect", this.state.modalType);
    window.open(this.state.href, "_blank");
  }

  openLink(href, type) {
    const autoRedirect = localStorage.getItem("autoRedirect");

    mixpanel.track("Open Link", { 'href': href });

    if (autoRedirect !== 'none' && autoRedirect !== type) {
      this.setState({
        modalOpen: true,
        modalType: type,
        modalCurrentType: autoRedirect,
        href: href
      });
    } else {
      window.open(href, "_blank");
    }
  }

  render() {
    const music = this.props.music;
    const album = music.album && <h3 className="music-info">{ music.album }</h3>
    const apple_url = music.apple_url &&
      <li>
        <button type="button"
                className="music-button"
                onClick={ this.openLink.bind(this, music.apple_url, 'apple_url') }
        >
          <div className="flex-row">
            <div className="service-logo-container">
              <img alt="" className="service-logo" src={ apple_logo } />
            </div>
            <div className="service-description">
              Apple Music
            </div>
          </div>
        </button>
      </li>;
    const gpm_url = music.gpm_url &&
      <li>
        <button type="button"
                className="music-button"
                onClick={ this.openLink.bind(this, music.gpm_url, 'gpm_url') }
        >
          <div className="flex-row">
            <div className="service-logo-container">
              <img alt="" className="service-logo" src={ gpm_logo } />
            </div>
            <div className="service-description">
              Google Play Music
            </div>
          </div>
        </button>
      </li>;
    const soundcloud_url = music.soundcloud_url &&
      <li>
        <button type="button"
                className="music-button"
                onClick={ this.openLink.bind(this, music.soundcloud_url, 'soundcloud_url') }
        >
          <div className="flex-row">
            <div className="service-logo-container">
              <img alt="" className="service-logo" src={ soundcloud_logo } />
            </div>
            <div className="service-description">
              Soundcloud
            </div>
          </div>
        </button>
      </li>;
    const spotify_url = music.spotify_url &&
      <li>
        <button type="button"
                className="music-button"
                onClick={ this.openLink.bind(this, music.spotify_url, 'spotify_url') }
        >
          <div className="flex-row">
            <div className="service-logo-container">
              <img alt="" className="service-logo" src={ spotify_logo } />
            </div>
            <div className="service-description">
              Spotify
            </div>
          </div>
        </button>
      </li>;

    return (
      <div className="flex-row music-container">
        <Modal show={ this.state.modalOpen }
          type={ this.state.modalType }
          currentType={ this.state.modalCurrentType }
          onNever={this.handleModalNever}
          onNo={this.handleModalNo}
          onYes={this.handleModalYes} />
        <div className="flex-row col-100">
          <div className="flex-col">
            <h2 className="music-info">{ music.name }</h2>
            <h3 className="music-info">{ music.artist }</h3>
            { album }
          </div>
        </div>
        <div className="flex-row col-100">
          <div className="flex-row col-50">
            <img className="artwork" src={ music.artwork } alt="Album cover" />
          </div>
          <div className="flex-row col-50">
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
