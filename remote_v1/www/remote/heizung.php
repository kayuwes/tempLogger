<?php
$datum=exec('python /var/www/remote/datum.py');
$temp1=exec('python /var/www/remote/temp1.py');
$temp2=exec('python /var/www/remote/temp2.py');
$temp3=exec('python /var/www/remote/temp3.py');
if ( $_GET['stat'] <> "" )
{
    // Datei wird zum Schreiben geöffnet
    $handle = fopen ( "schalter", "w" );

    // schreiben des Inhaltes
    fwrite ( $handle, $_GET['stat'] );

    // Datei schließen
    fclose ( $handle );

//Zurück
	echo '<a href="heizung.php">Zurück</a>';
    // Datei wird nicht weiter ausgeführt
    exit;
}
$myfile = fopen ( "zeiger", "r" );
$switch = fgetc ($myfile);
fclose ( $myfile );
if ($switch == "1")
	$display  =  KALT;
if ($switch == "0")
        $display  =  HEISS;

?>
<html>
<head>
<meta charset="UTF-8">
<meta name="HEIZUNG" content="width=device-width" />
<title>H E I Z U N G</title>
<link href="/var/www/favicon.ico" rel="icon" type="image/x-icon" />
</head>
<body>
<p>Letzte Messung: <?php echo $datum ?><br/></p>
<p>Temperatur1: <?php echo $temp1 ?><br/></p>
<p>Temperatur2: <?php echo $temp2 ?><br/></p>
<p>Temperatur3: <?php echo $temp3 ?><br/></p>
<form action="heizung.php" method="get">

<p>STATUS AN oder AUS<br />
<input type="Text" name="stat" ></p>
<input type="Submit" stat="" value="speichern">
</form>
<p>GPIO18: <?php echo $switch ?></p>
<p>Die Heizung ist: <?php echo $display ?></p>
<p><br/></p>
<p>ANLEITUNG:<br/>
AN oder AUS eingeben und speichern<br/>
auf Gross- Kleinschreibung achten!!<br/>
Nach spätestens 1 Minute<br/>
wird geschaltet und der aktuelle Zustand<br/>
 --- 1/0 und KALT/HEISS wird aktualisiert<br/>
Relais ist aktiv low 0<br/>
daher 1--> Kalt/aus  ;  0 --> Heiss an<br/>
</p>

</body>
</html>
