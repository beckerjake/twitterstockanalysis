<?php 
/*$con=mysql_connect('ec2-52-27-111-35.us-west-2.compute.amazonaws.com',"","");  
if (!$con)
{
    die('Could not connect: ' . mysql_error());
} */  



$servername = "localhost";
$username = "root";
$password = "";
$dbname = "ticktalk";


// Create connection
$con = new mysqli($servername, $username, $password, $dbname);

// Check connection
if (!$con) {
    die("Connection failed: " . mysqli_connect_error());
}


$sql = "SELECT * ticktalk.stocks";
$result = mysqli_query($con, $sql);

if (mysqli_num_rows($result) > 0) {
    // output data of each row
			echo "<table border='1' >
<tr>
<td align=center> <b>Company No</b></td>
<td align=center><b>Ticker</b></td>
<td align=center><b>Price</b></td>";
    while($row = mysqli_fetch_assoc($result)) {
		  
    echo "<tr>";
    echo "<td align=center>".$row["issuer_name"]."</td>";
    echo "<td align=center>".$row["symbol"]."</td>";
    echo "<td align=center>".$row["price"]."</td>";
    //echo "<td align=center>$data[3]</td>";
    //echo "<td align=center>$data[4]</td>";
    echo "</tr>";
}
echo "</table>";
		
       // echo "Company: " . $row["issuer_name"]. " - Ticker: " . $row["symbol"]. " - Price: " . $row["price"]. "<br>";
    }
} else {
    echo "0 results";
}






?>