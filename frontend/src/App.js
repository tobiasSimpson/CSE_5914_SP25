import logo from './logo.png';
import './App.css';
import TweetTrends  from './TweetTrends';

function App() {
  return (
    <div className="App">
      <header className="App-header">

      
        <img src={logo} className="App-logo" alt="logo" />
        <span>EchoX</span>
      </header>
      <div className="Body">

        <span className = "question">
          What topic would you like to explore?
        </span>
        <span className = "input-group">
          <input id="topic" className="input" placeholder = "Twitter, e.g."></input>
          <button className = "btn">Search</button>
        </span>

        <br />
        <br />
        <TweetTrends/>
      </div>

    </div>
  );
}

export default App;
