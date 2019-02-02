

<?php
phpinfo();
$modeon17 = trim(@shell_exec("/usr/local/bin/gpio -g mode 18 out"));
//if(isset($_GET['Lichtein'])){
//$val = trim(@shell_exec("/usr/local/bin/gpio -g write 18 1"));
//echo "Licht18 ist an";
//}
//else if(isset($_GET['Lichtaus'])){
$val = trim(@shell_exec("/usr/local/bin/gpio -g write 18 0"));
//echo "Licht18 ist aus";
//}
?>
