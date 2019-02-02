#!/usr/bin/php


<?php
    $val = trim(@shell_exec("/usr/local/bin/gpio -g read 18"));
//    $handle = fopen ( "zeiger", "w" );//link geht nicht
    $handle = fopen ( "/var/www/remote/zeiger", "w" );
    fwrite ( $handle, $val );
    fclose ( $handle );
    exit;
?>

