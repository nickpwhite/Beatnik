import React, { Component } from 'react';

class Modal extends Component {
  constructor(props) {
    super(props);

    this.displayTypes = {
      'apple_url': "Apple Music",
      'gpm_url': "Google Play Music",
      'soundcloud_url': "Soundcloud",
      'spotify_url': "Spotify"
    };
  }
  render() {
    if (!this.props.show) {
      return null;
    }

    const type = this.displayTypes[this.props.type];
    const currentType = this.props.currentType && <p>Note that { this.displayTypes[this.props.currentType] } is currently your default</p>;

    return (
      <div className="backdrop">
        <div className="modal">
          <div className="flex-col modal-content">
            <div className="row-90">
              <p className="modal-text">Would you like to make { type } your default?</p>
              { currentType } 
              <p className="modal-text"><small>You can reset this value by clearing data for this site in your browser</small></p>
            </div>
            <div className="row-10">
              <div className="flex-row-reverse">
                <div className="col-33">
                  <button className="modal-button" onClick={ this.props.onYes }>
                    Set default 
                  </button>
                </div>
                <div className="col-33">
                  <button className="modal-button" onClick={ this.props.onNo }>
                    Not this time
                  </button>
                </div>
                <div className="col-33">
                  <button className="modal-button" onClick={ this.props.onNever }>
                    Don't ask again
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Modal;
