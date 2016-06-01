<?php 
/*$con=mysql_connect('ec2-52-27-111-35.us-west-2.compute.amazonaws.com',"","");  
if (!$con)
{
    die('Could not connect: ' . mysql_error());
} */  

$numStocks = 10;

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "ticktalk";


// Create connection
$con = new mysqli($servername, $username, $password, $dbname);

// Check connection
if (!$con) 
{
    die("Connection failed: " . mysqli_connect_error());
}

$url = "https://publish.twitter.com/oembed?url=https%3A%2F%2Ftwitter.com%2FInterior%2Fstatus%2F507185938620219395";
$json = file_get_contents($url);
$json_data = json_decode($json, true);
$tweet = $json_data["html"];


//$sql = "SELECT TOP " .$numStocks. " * FROM  ticktalk.stocks";
//$sql = "SELECT * FROM (SELECT * FROM ticktalk.daySummaries order by id desc limit ".$numStocks.") unsorted order by id asc";
//$sql = "SELECT * FROM (SELECT * FROM ticktalk.daySummaries order by id desc limit ".$numStocks.") unsorted order by stockName asc";
$sql = "SELECT * FROM (SELECT * FROM ticktalk.daySummaries order by id desc limit ".$numStocks.") unsorted order by trim(leading 'the ' from lower(stockName)) asc";
$result = mysqli_query($con, $sql);

if (mysqli_num_rows($result) > 0) 
{
    // output data of each row
	echo "<table class=\"table table-striped\" >
			<thead>
				<tr>
					<th align=center> <b>Company</b></th>
					<th align=center><b>Symbol</b></th>
					<th align=center><b>Sentiment</b></th>
					<th align=center><b>Closing Price</b></th>
					<th align=center><b>More Data</b></th>
				</tr>
			</thead>
			"
			;
			
			$counter = 0;
    while($row = mysqli_fetch_assoc($result)) {
		  
		  $counter = $counter + 1;
		  
		  $symbol = $row["symbol"];
		  $time_period = "7d";
		  
		  echo "<tr>";
          echo "        <td>".$row["stockName"]."</td>";
          echo "        <td>".$symbol."</td>";
          echo "        <td>Neutral</td>";
          echo "        <td>".$row["end_price"]."</td>";
          echo "        <td><a href=\"#\" id=\"show_".$counter."\">Show Data</a></td>";
          echo "      </tr>";
          echo "      <tr>";
          echo "        <td colspan=\"5\">";
          echo "          <div id=\"extra_".$counter."\" style=\"display: none;\">";
          
		  
		  
		  
		  //echo "            <img src=\"http://chart.finance.yahoo.com/z?s=".$symbol."&t=".$time_period."&q=l&l=on&z=m\"/>";
		  //three graph display
		  echo "            <img align=\"middle\" src=\"http://chart.finance.yahoo.com/z?s=".$symbol."&t=7d&q=l&l=on&z=m\"/>";
		  echo "            <img align=\"middle\" src=\"http://chart.finance.yahoo.com/z?s=".$symbol."&t=1m&q=l&l=on&z=m\"/>";
		  //echo "            <img src=\"http://chart.finance.yahoo.com/z?s=".$symbol."&t=1y&q=l&l=on&z=s\"/>";
		  //echo " <input type=\"text\" id=\"update\"/><button id=\"btn\">Get</button> <div id=\"embed\"></div>";
          
		  //for the tweet
		  
		  echo $tweet;
		  
		  //stuff for headlines
		  $path_prefix = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=";
			$ticker = $symbol;
			$path_suffix = "&lg=us&region=US&lang=en-US";

			$path = $path_prefix.$ticker.$path_suffix;
			//$path = "http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDeputados";
			
			echo "before readfile";
			readfile($path);
			echo "after readfile";

			
			$xml_file = file_get_contents($path);
			if($xml_file)
			{
				//file_put_contents ("error_log.txt","2",FILE_APPEND);
				echo "get_contents_success";
				echo $xml_file;
			}
			else
			{
				
				echo "get_contents_fail";
				
			}
			
/* 			function get_xml_from_url($url){
				//file_put_contents ("error_log.txt","3",FILE_APPEND);
				$ch = curl_init();
//file_put_contents ("error_log.txt","4",FILE_APPEND);
				curl_setopt($ch, CURLOPT_URL, $url);
				curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
				curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13');
//file_put_contents ("error_log.txt","5",FILE_APPEND);
				$xmlstr = curl_exec($ch);
				curl_close($ch);
//file_put_contents ("error_log.txt","6",FILE_APPEND);
				return $xmlstr;
			} */
			
			echo "before old curl";

			
			function get_url_contents($url){
        $crl = curl_init();
        $timeout = 5;
        curl_setopt ($crl, CURLOPT_URL,$url);
        curl_setopt ($crl, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt ($crl, CURLOPT_CONNECTTIMEOUT, $timeout);
        $ret = curl_exec($crl);
        curl_close($crl);
        return $ret;
}

echo "after old curl";


echo "before new curl";

	$host = $path;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $host);
    curl_setopt($ch, CURLOPT_VERBOSE, 1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_AUTOREFERER, false);
    curl_setopt($ch, CURLOPT_REFERER, "https://feeds.finance.yahoo.com/rss/2.0");
    curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    $result = curl_exec($ch);
    curl_close($ch);

    print_r($result); 

	echo "after new curl";

	
function getSslPage($url) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($ch, CURLOPT_HEADER, false);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_REFERER, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
    $result = curl_exec($ch);
    curl_close($ch);
    return $result;
}
	echo "before ssl";
	echo getSslPage($path);		
	echo "after ssl";	
	
	
	$arrContextOptions=array(
    "ssl"=>array(
        "verify_peer"=>false,
        "verify_peer_name"=>false,
    ),
);  

	echo "before bad";

$response = file_get_contents($path, false, stream_context_create($arrContextOptions));

echo $response;
		echo "after bad";

	
	
//file_put_contents ("error_log.txt","7",FILE_APPEND);			
			$xmlstr = get_url_contents($path);
//file_put_contents ("error_log.txt","8",FILE_APPEND);
			echo($xmlstr);
//file_put_contents ("error_log.txt","9",FILE_APPEND);	



		
			/*  if (($response_xml_data = file_get_contents($path)===false){
				echo "Error fetching XML";
			} else {
				libxml_use_internal_errors(true);
				$data = simplexml_load_string($response_xml_data);
				if (!$data) {
					echo "Error loading XML";
					foreach(libxml_get_errors() as $error) {
						echo $error->message;
					}
				} else {
					print_r($data);
				}
			}  */
			
//file_put_contents ("error_log.txt","10",FILE_APPEND);			
			$xml = simplexml_load_string($xml_file);
			//file_put_contents ("error_log.txt","11",FILE_APPEND);
			$channel = $xml->channel;
			$channel_title = $channel->title;
			$channel_description = $channel->description;
//file_put_contents ("error_log.txt","12",FILE_APPEND);
			echo "<h1>".$channel_title."</h1>";
			echo "<h2>".$channel_description."</h2>";

			foreach ($channel->item as $item)
			{
				$title = $item->title;
				$link = $item->link;
				$descr = $item->description;

				echo "<h3><a href='".$link."'>".$title."</a></h3>";
				echo "<p>".$descr."</p>";
			}
		  ////headlines
		  
		  
		  echo "            <br>hidden row";
          echo "            <br>hidden row";
          echo "          </div>";
          echo "        </td>";
          echo "      </tr>";
		  
		  /*
			echo "<tr>";
			echo "<td align=center>".$row["issuer_name"]."</td>";
			echo "<td align=center>".$row["symbol"]."</td>";
			echo "<td align=center>".$row["price"]."</td>";
			echo "</tr>";
	*/
	}

	echo "</table>";
		
       // echo "Company: " . $row["issuer_name"]. " - Ticker: " . $row["symbol"]. " - Price: " . $row["price"]. "<br>";
}
 else 
{
    echo "0 results";
}






?>
