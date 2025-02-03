import logo from './logo.png';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import TweetTrends  from './TweetTrends';
import Button from 'react-bootstrap/Button';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';

function App() {
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
          <InputGroup style={{flexGrow:1}}>
            <Form.Control type="text" id="topic" className="input" placeholder = "Twitter, e.g."></Form.Control>
            <Button variant="primary">Search</Button>
          </InputGroup>
        </div>

        <br />
        <br />
        <TweetTrends/>
      </div>

    </div>
  );
}

export default App;
