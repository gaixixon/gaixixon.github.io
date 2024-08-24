<?php
if ($_GET == null){echo "it works!"; die;}
/* get json data from local file
$jsonFilePath = 'iptv.json';
$jsonData = file_get_contents($jsonFilePath);
$dataArray = json_decode($jsonData, true);
*/

/* get json raw data from with curl
function getJsonData($url) {
    $curl = curl_init($url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false); // Optional: Disable SSL verification (use with caution)
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false); // Optional: Disable SSL verification (use with caution)

    $jsonData = curl_exec($curl);
    curl_close($curl);

    if ($jsonData === false) {
        return null; // Return null on error
    }

    return json_decode($jsonData, true);
} */

$jsonData = file_get_contents('https://gaixixon.github.io/iptv.json');
$dataArray = json_decode($jsonData, true);
$channel = isset($_GET['channel']) ? $_GET['channel'] : '';
if ($channel == ''){echo 'Null'; die;}

function getLinkByChannel($dataArray, $channel) {
    foreach ($dataArray as $item) {
        if ($item['channel'] == $channel) {
            return $item['link'];
        }
    }
    echo 'Null'; die;
    //return 'None is found'; // Return null if channel not found
}
header("Location: " . getLinkByChannel($dataArray, $channel));
die();
?>
