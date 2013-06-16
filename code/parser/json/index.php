<?php
ini_set('display_errors', 1);
require_once('twitterAPIExchange.php');

// Set access tokens here - see: https://dev.twitter.com/apps/
$settings = array(
    'oauth_access_token' => "243821206-s85S2fXJuzcs44q0XxtTtHCBtm50YnMuUt9DhRuP",
    'oauth_access_token_secret' => "wGUwEzH4qcHbAP3FuSwVX86iutI54HkMeJIv9cmBaFw",
    'consumer_key' => "2joJbPhjrkcU6GGqKCwF9Q",
    'consumer_secret' => "uGzKT64ICmZ6e8gX4sXYQDMD0M0tO0sX1gmMknNxXs"
);

/*
// URL for REST request, see: https://dev.twitter.com/docs/api/1.1/
$url = 'https://api.twitter.com/1.1/blocks/create.json';
$requestMethod = 'POST';


// POST fields required by the URL above. See relevant docs as above
$postfields = array(
    'screen_name' => 'usernameToBlock', 
    'skip_status' => '1'
);

// Perform a POST request and echo the response
$twitter = new TwitterAPIExchange($settings);
echo $twitter->buildOauth($url, $requestMethod)
             ->setPostfields($postfields)
             ->performRequest();
*/

// Perform a GET request and echo the response
// Note: Set the GET field BEFORE calling buildOauth();
//$url = 'https://api.twitter.com/1.1/statuses/user_timeline.json';
//$getfield = '?screen_name=sbahnberlin&count=1';
$url = $argv[1];
$getfield = $argv[2];
$requestMethod = 'GET';
$twitter = new TwitterAPIExchange($settings);
echo $twitter->setGetfield($getfield)
             ->buildOauth($url, $requestMethod)
             ->performRequest();
?>