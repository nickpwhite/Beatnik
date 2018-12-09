import React, { Component } from 'react';
import axios from 'axios';
import mixpanel from 'mixpanel-browser';
import createHistory from 'history/createBrowserHistory';

class ConvertForm extends Component {
  constructor(props) {
    super(props);
    const params = new URLSearchParams(props.query);
    this.state = {
      value: params.get('q') || ''
    };

    this.history = createHistory();

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);

    this.handleSubmit();
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    if (this.state.value === '') {
      return false;
    }

    this.props.onBeforeSubmit();

    mixpanel.track("Search", {
      'query': this.state.value
    });

    const url = `${process.env.REACT_APP_API_ROOT}/api/music?q=${this.state.value}`
    axios.get(url)
      .then((response) => { 
        this.history.push({
          pathname: '/',
          search: `?q=${this.state.value}`
        });
        this.props.onSubmit(response.data);
      })
      .catch((err) => {
        this.props.onSubmit([]);
      });
    if (event) {
      event.preventDefault();
    }
    return false;
  }

  render() {
    return (
      <form id="search-form" className="search-form flex-row" onSubmit={ this.handleSubmit }>
        <div className="col-75">
          <input
            className="search-box"
            type="text"
            placeholder="Enter a link to convert"
            value={ this.state.value }
            onChange={ this.handleChange }
          />
        </div>
        <div className="col-25">
          <input className="search-button" type="submit" value="Convert" />
        </div>
      </form>
    )
  }
}

export default ConvertForm;
