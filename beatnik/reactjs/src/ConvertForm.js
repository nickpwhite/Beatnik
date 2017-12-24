import React, { Component } from 'react';
import axios from 'axios';

class ConvertForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: ''
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    const url = `http://127.0.0.1:8000/api/music?q=${this.state.value}`
    axios.get(url)
      .then((response) => { 
        this.props.onSubmit(response.data);
      })
      .catch((err) => { console.log(err); });
    event.preventDefault();
    return false;
  }

  render() {
    return (
      <form className="search-form flex-row" onSubmit={ this.handleSubmit }>
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
