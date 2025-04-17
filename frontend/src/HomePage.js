import logo from './logo.png';
import TweetTrends  from './TweetTrends';
import Button from 'react-bootstrap/Button';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import { useEffect, useState } from 'react';
import TweetList from './TweetList';

function HomePage() {

  const search = async () => {
    if (searchDisabled || searchString === chartTitle) return;
    setSearchDisabled(true);
    const curSearchString = searchString || "Artificial Intelligence";
    
    // Get the tweets from localhost:5000/tweet_data/<topic>
    const response = await fetch(`http://localhost:5000/tweet_data/${curSearchString}`);

    if (!response.ok) {
      setTweets(["Error fetching tweets"]);
      setSearchDisabled(false);
      return;
    }
    const responseJSON = await response.json();
    // const responseJSON = {
    //   sentiment: {positive: Math.floor(Math.random() * 100 + 1), negative: Math.floor(Math.random() * 100 + 1)},
    //   tweets: {
    //     generated: "This is a generated tweet",
    //     text: ["This is a real tweet", "This is another real tweet"]
    //   }
    // }
    console.log(responseJSON.sentiment);
    // const tweets = [responseJSON.tweets.generated, ...responseJSON.tweets.text]
    setTweets(responseJSON.tweets);
    setChartData([["Sentiment", "Number of Tweets", { role: "style" }],["Negative",responseJSON.sentiment.negative, "red"], ["Positive", responseJSON.sentiment.positive, "green"]]);
    setChartTitle(curSearchString)
    setSearchDisabled(false);
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
  // useEffect(() => {
  //   // Check if tweets is empty
  //   if (tweets.length === 0) return;
  //   const y = document.getElementById("tweets-container").getBoundingClientRect().top + window.scrollY - 40;
  //   window.scrollTo({top: y, behavior: 'smooth'});
  // }, [tweets]);

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
