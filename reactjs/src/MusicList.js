import React, { Component } from 'react';
import Music from './Music.js';

class MusicList extends Component {
  render() {
    let items = [];

    for (let i = 0; i < this.props.music.length; i++) {
      const item = this.props.music[i];

      items.push(
        <Music key={ i } music={ item.fields } />
      );
    }
    return items;
  }
}

export default MusicList;
