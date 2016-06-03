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
					<th align=center><b>Company</b></th>
					<th align=center><b>Symbol</b></th>
					<th align=center><b>Sentiment</b></th>
					<th align=center><b>Closing Price</b></th>
					<th align=center><b>More Data</b></th>
				</tr>
			</thead>";
			
	$counter = 0;
    while($row = mysqli_fetch_assoc($result)) {
		  
		$counter = $counter + 1;
		  
		$symbol = $row["symbol"];
		$stockName = $row["stockName"];
		$time_period = "7d";
		  
		//Table Data
		
		echo "<tr>";
			echo "<td>".$stockName."</td>";
			echo "<td>".$symbol."</td>";
			echo "<td>Neutral</td>";
			echo "<td>".$row["end_price"]."</td>";
			echo "<td><a href=\"#\" id=\"show_".$counter."\">Show Data</a></td>";
		echo "</tr>";
          
		//More Data
		echo "<tr>";
			echo " <td colspan=\"5\">";
				echo "<div id=\"extra_".$counter."\" style=\"display: none;\">";
          
				//More Data (Calculated)
				/* //echo  "<div class=\"table-responsive\" align=\"center\">";
					echo  "<div class=\"table-responsive\">"; //left aligned
					echo "  <table class=\"table\">";
					echo "<caption> Calculated </caption>";
					//for the tweet
					echo "  <tr>";
					echo "  <td colspan=\"5\">";
					//echo "<td>";
					echo $tweet;
					echo "  </td>";
					echo "  </tr>";
		  
					echo "  </table>";
					echo "  </div>"; */
		
		
		$svg_side_length = 200;
		$spacer_side_length = 100;
		$default_rad = $svg_side_length/2;
		$per_daily_avg = 100;
		$per_neg_tweets = 25;
		$per_pos_tweets = 75;
		
		$daily_avg_radius = $per_daily_avg/100 * $default_rad;
		$neg_tweets_radius = $per_neg_tweets * $daily_avg_radius;
		$pos_tweets_radius = $per_pos_tweets * $daily_avg_radius;
		
		//https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/text-anchor
		echo"<div style=\"text-align:center;\">
				<svg height=".$svg_side_length." width=".$svg_side_length.">
					<circle cx=\"100\" cy=\"100\" r=".$default_rad." stroke=\"black\" stroke-width=\"0\" fill=\"lightcoral\" />
					<text text-anchor=\"middle\" x=\"100\" y=\"100\" fill=\"white\">".$per_neg_tweets."</text>
					<style><![CDATA[text{font: bold 36px Helvetica, sans-serif;}]]></style>
				</svg>
				<svg height=".$spacer_side_length." width=".$spacer_side_length.">
				<svg height=".$svg_side_length." width=".$svg_side_length.">
					<circle cx=\"100\" cy=\"100\" r=".$default_rad." stroke=\"black\" stroke-width=\"0\" fill=\"grey\" />
					<text text-anchor=\"middle\" x=\"100\" y=\"100\" fill=\"white\">".$per_daily_avg."</text>
					<style><![CDATA[text{font: bold 36px Helvetica, sans-serif;}]]></style>
				</svg>
				<svg height=".$spacer_side_length." width=".$spacer_side_length.">
				<svg height=".$svg_side_length." width=".$svg_side_length.">
					<circle cx=\"100\" cy=\"100\" r=".$default_rad." stroke=\"black\" stroke-width=\"0\" fill=\"lightgreen\" />
					<text text-anchor=\"middle\" x=\"100\" y=\"100\" fill=\"white\">".$per_pos_tweets."</text>
					<style><![CDATA[text{font: bold 36px Helvetica, sans-serif;}]]></style>
				</svg>
			</div>";
		
		
	echo "	
		<div id=\"myCarousel\" class=\"carousel slide\" data-ride=\"carousel\">
  <!-- Indicators -->
  <ol class=\"carousel-indicators\">
    <li data-target=\"#myCarousel\" data-slide-to=\"0\" class=\"active\"></li>
    <li data-target=\"#myCarousel\" data-slide-to=\"1\"></li>
    <li data-target=\"#myCarousel\" data-slide-to=\"2\"></li>
    <li data-target=\"#myCarousel\" data-slide-to=\"3\"></li>
  </ol>

  <!-- Wrapper for slides -->
  <div class=\"carousel-inner div-responsive center-block\" role=\"listbox\">
    <div class=\"item active\">
      ".$tweet."
    </div>

    <div class=\"item div-responsive center-block\">
      ".$tweet."
    </div>

    <div class=\"item div-responsive center-block\">
      ".$tweet."
    </div>

    <div class=\"item div-responsive center-block\">
      ".$tweet."
    </div>
  </div>

  <!-- Left and right controls -->
  <a class=\"left carousel-control\" href=\"#myCarousel\" role=\"button\" data-slide=\"prev\">
    <span class=\"glyphicon glyphicon-chevron-left\" aria-hidden=\"true\"></span>
    <span class=\"sr-only\">Previous</span>
  </a>
  <a class=\"right carousel-control\" href=\"#myCarousel\" role=\"button\" data-slide=\"next\">
    <span class=\"glyphicon glyphicon-chevron-right\" aria-hidden=\"true\"></span>
    <span class=\"sr-only\">Next</span>
  </a>
</div>
		";
		
		
		echo "<ul class=\"bxslider\">";
			/* echo "<li>".$tweet."</li>";
			echo "<li>".$tweet."</li>";
			echo "<li>".$tweet."</li>"; */
			
			echo "<li>tweet</li>";
			echo "<li>tweet</li>";
			echo "<li>tweet</li>";
			
		echo "</ul>";
		
		//echo $tweet;
		
		
		
		
		 //More Data (Yahoo-populated)
		 echo  "<div class=\"table-responsive\" align=\"center\">";

			echo " <table class=\"table\">";
				echo "<caption> Yahoo Data </caption>";
		 //stock charts
		 
					echo "<thead>";
						echo " <tr>";
			//print header
							echo "<th colspan=\"2\">";
								echo "<p><font size=\"4\">Day and Week Charts for ".$stockName."</font></p>";
							echo "</th>";
						echo "</tr>";
					echo "</thead>";
		 
					echo "  <tr>";
						//1 day
						echo " <td align=\"center\">";
							echo "<br>";
							echo "<img align=\"center\" src=\"http://chart.finance.yahoo.com/z?s=".$symbol."&t=1d&q=l&l=on&z=s\"/>";
						echo "  </td>";
						//7 days
						echo " <td align=\"center\">";
							echo "<br>";
							echo "<img align=\"center\" src=\"http://chart.finance.yahoo.com/z?s=".$symbol."&t=7d&q=l&l=on&z=s\"/>";
						echo "  </td>";
		 
					echo " </tr>";
			echo "</table>";
		echo "</div>";
		  
		  
		  //headlines
		  
		  //consyruct the url with the necessary ticker symbol
		  $path_prefix = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=";
			$ticker = $symbol;
			$path_suffix = "&lg=us&region=US&lang=en-US";

			$path = $path_prefix.$ticker.$path_suffix;

			//retrieve the file from the url
			$xml_file = file_get_contents($path);
			
			//extract the data from the file
			$xml = simplexml_load_string($xml_file);
			
			//get data in useable form
			$channel = $xml->channel;
			$channel_title = $channel->title;
			$channel_description = $channel->description;
			
			//headline table
			echo  "<div class=\"table-responsive\" align=\"center\">";
				echo "<table class=\"table table-no-border\">";
					echo "<thead>";
						echo " <tr>";
			//print header
							echo "<th colspan=\"2\">";
								//echo "<p><font size=\"5\">".$channel_title."</font></p>"; //unnecessary
								echo "<p><font size=\"4\">".$channel_description."</font></p>";
							echo "</th>";
						echo "</tr>";
					echo "</thead>";
			//print headlines
					foreach ($channel->item as $item)
					{
						$title = $item->title;
						$link = $item->link;
						$descr = $item->description;
						echo "<tr>";
							echo "<td colspan=\"2\">";
								echo "<font size=\"3\"><a href='".$link."'>".$title."</a></font>";
								//echo "<p><font size=\"3\"><a href='".$link."'>".$title."</a></font></p>";
								//echo "<p>".$descr."</p>";
							echo "</td>";
						echo " </tr>";
					}
		  	  
				echo "</table>";
			echo "</div>";
		  
          echo "          </div>";
          echo "        </td>";
          echo "      </tr>";
		  
	}

	echo "</table>";
		
}
 else 
{
    echo "0 results";
}






?>
