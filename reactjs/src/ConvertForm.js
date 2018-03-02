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

    mixpanel.track("Search", {
      'query': this.state.value
    });

    const url = `http://localhost:8000/api/music?q=${this.state.value}`
    axios.get(url)
      .then((response) => { 
        this.history.push({
          pathname: '/convert',
          search: `?q=${this.state.value}`
        });
        this.props.onSubmit(response.data);
      })
      .catch((err) => { console.log(err); });
    if (event) {
      event.preventDefault();
    }
    return false;
  }

  render() {
    return (
      <form id="search-form" className="search-form flex-row" onSubmit={ this.handleSubmit }>
        <div className="col-100">
          <input 
            className="search-box"
            type="text" 
            placeholder="Enter a link to convert" 
            value={ this.state.value }
            onChange={ this.handleChange }
          />
        </div>
      </form>
    )
  }
}

export default ConvertForm;
