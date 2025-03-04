import logo from './logo.png';
import TweetTrends  from './TweetTrends';
import Button from 'react-bootstrap/Button';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import { useEffect, useState } from 'react';
import TweetList from './TweetList';
import Card from 'react-bootstrap/Card';

function HomePage() {

  const search = async () => {
    if (searchDisabled || searchString === chartTitle) return;
    setSearchDisabled(true);
    const curSearchString = searchString || "Artificial Intelligence";
    
    // Get the search results
    // Temporary
    const a = () => Math.floor(Math.random() * 1000);
    const b = Math.random
    const data = [
      ["Date", "Mentions", "Sentiment"],
      ...Array.from(Array(12)).map((_, i) => 
        [new Date(2024, i, 1), a(), b()]
      )
    ];

    // Sleep for half a second
    await new Promise(r => setTimeout(r, 500));

    setSearchDisabled(false);
    setChartData(data); 
    setChartTitle(curSearchString)
  }

  const searchIfEnter = (e) => {
    if (e.key === 'Enter') search();
  }

  const [searchString, setSearchString] = useState("");

  const [searchDisabled, setSearchDisabled] = useState(false);

  const [chartTitle, setChartTitle] = useState("Twitter");

  const [chartData, setChartData] = useState(null);

  const [tweets, setTweets] = useState([]); // State for storing generated tweets

  // Search on load
  useEffect(() => {
    search()
  }, []);

  // Scroll to the tweet list whenever tweets changes
  useEffect(() => {
    // Check if tweets is empty
    if (tweets.length === 0) return;
    const y = document.getElementById("tweets-container").getBoundingClientRect().top + window.scrollY - 40;
    window.scrollTo({top: y, behavior: 'smooth'});
  }, [tweets]);

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
            <Button variant="primary" onClick={search} disabled={searchDisabled}>Search</Button>
          </InputGroup>
        </div>

        <br />
        <br />
        <TweetTrends chartData={chartData} chartTitle={chartTitle} setTweets={setTweets} />
        <br />
        <TweetList tweets={tweets} />
      </div>

    </div>
  );
}

export default HomePage;
