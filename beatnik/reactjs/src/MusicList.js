import React, { Component } from 'react';

class MusicList extends Component {
  render() {
    console.log(this.props.music);
    let items = [];
    let links = [];

    for (let i = 0; i < this.props.music.length; i++) {
      const item = this.props.music[i];
      const data = item.fields;
      items.push(
        <div>
          <div className="flex-row">
            <img src={ data.artwork } />
            <h2>{ data.name }</h2>
            <h3>{ data.artist }</h3>
          </div>
          <ul>
            { data.apple_url && <li><a href={ data.apple_url }>{ data.apple_url }</a></li> }
            { data.gpm_url && <li><a href={ data.gpm_url }>{ data.gpm_url }</a></li> }
            { data.soundcloud_url && <li><a href={ data.soundcloud_url }>{ data.soundcloud_url }</a></li> }
            { data.spotify_url && <li><a href={ data.spotify_url }>{ data.spotify_url }</a></li> }
          </ul>
        </div>
      )
    }
    return items
  }
}

export default MusicList;
