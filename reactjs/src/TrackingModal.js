import React, { Component } from 'react';

class Modal extends Component {
  render() {
    if (!this.props.show) {
      return null;
    }

    return (
      <div className="backdrop">
        <div className="modal">
          <div className="flex-col modal-content">
            <div className="row-90">
              <p className="modal-text">
                At Beatnik we collect anonymous data about actions our users perform on the site. This is to understand how people use the service and how we can make it better.
              </p>
              <p className="modal-text">
                We only collect this data if you explicitly let us, and you can opt out at any time. To grant us permission to collect data about your usage, click allow, or click block and we won't bother you again.
              </p>
            </div>
            <div className="row-10">
              <div className="flex-row-reverse">
                <div className="col-50">
                  <button className="modal-button" onClick={ this.props.onYes }>
                    Allow
                  </button>
                </div>
                <div className="col-50">
                  <button className="modal-button" onClick={ this.props.onNo }>
                    Block
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
