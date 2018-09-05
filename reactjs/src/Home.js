import React, { Component } from 'react';
import mixpanel from 'mixpanel-browser';
import ConvertForm from './ConvertForm.js';
import MusicList from './MusicList.js';
import Spinner from './Spinner.js';
import Utils from './Utils.js';

class Home extends Component {
  constructor(props) {
    super(props);

    mixpanel.track("View Home");

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

  renderConverter() {
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
          <ConvertForm onBeforeSubmit={ this.setLoading }
            onSubmit={ this.updateMusic }
            query={ Utils.getQueryParams(window.location.href) } />
        </div>
        <Spinner loading={ this.state.loading } />
        <MusicList music={ this.state.music } />
      </div>
    )
  }

  renderIntro() {
    return (
      <div className="content">
        <p className="intro">
          Beatnik makes it easy to share music that you love with the people you know will love it too.
        </p>
        <p className="intro">
          To get started just download the browser extension into your favourite browser, and any links that would normally take you to one of our supported streaming service will now take you to a page on this site that has a link to the same song or album on all of our suppored streaming services.
        </p>
        <p className="intro">
          Alternatively, you can use our converter to get a link that you can easily share with your friends, no matter how they listen.
        </p>
      </div>
    )
  }

  render() {
    const converter = this.renderConverter();
    const intro = this.renderIntro();

    return (
      <div>
        {converter}
        {intro}
      </div>
    )
  }
}

export default Home;
