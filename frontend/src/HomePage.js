import logo from './logo.png';
import TweetTrends  from './TweetTrends';
import Button from 'react-bootstrap/Button';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import { useState } from 'react';

function HomePage() {

  const search = async () => {
    alert(`You searched for ${searchString}`)
  }

  const searchIfEnter = (e) => {
    if (e.key === 'Enter') search();
  }

  const [searchString, setSearchString] = useState("");

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <span>EchoX</span>
      </header>
      <div className="Body">
        <div style={{display:'flex'}}>
          <span className = "question" style={{width:600}}>
            What topic would you like to explore?
          </span>
          <InputGroup style={{flexGrow:1}} onKeyDown={searchIfEnter}>
            <Form.Control type="text" id="topic" className="input" placeholder = "Twitter, e.g." 
              value={searchString} onChange={(e) => setSearchString(e.target.value)}></Form.Control>
            <Button variant="primary" onClick={search}>Search</Button>
          </InputGroup>
        </div>

        <br />
        <br />
        <TweetTrends/>
      </div>

    </div>
  );
}

export default HomePage;
