import React, { Component } from 'react';

class Music extends Component {
  render() {
    const music = this.props.music;
    const album = music.album && <h3 className="music-info-item">{ music.album }</h3>
    const apple_url = music.apple_url && <li><a href={ music.apple_url } target="_blank">{ music.apple_url }</a></li>;
    const gpm_url = music.gpm_url && <li><a href={ music.gpm_url } target="_blank">{ music.gpm_url }</a></li>;
    const soundcloud_url = music.soundcloud_url && <li><a href={ music.soundcloud_url } target="_blank">{ music.soundcloud_url }</a></li>;
    const spotify_url = music.spotify_url && <li><a href={ music.spotify_url } target="_blank">{ music.spotify_url }</a></li>;
    return (
      <div className="flex-row music-container">
        <div className="flex-row col-100">
          <div>
            <img src={ music.artwork } alt="Album cover" />
          </div>
          <div className="flex-col">
            <div className="row-50 music-info">
              <h2 className="music-info-item">{ music.name }</h2>
              <h3 className="music-info-item">{ music.artist }</h3>
              { album }
            </div>
            <div className="row-50">
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
