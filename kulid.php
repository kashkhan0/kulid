<?php

function ulid($ts = 0){

  $abc = '0123456789abcdefghjkmnpqrstvwxyz';
  $abclen = 32;
  $lastGenTime = 0;
  $lastRandChars = [];
  if ($ts <1)$ts = microtime(true) * 1000;
    $now = intval($ts);
   
    $timeChars = '';
    $randChars = '';

    for ($i = 9; $i >= 0; $i--) {
        $mod = $now % $abclen;
        $timeChars = $abc[$mod].$timeChars;
        $now = ($now - $mod) / $abclen;
    }


        for ($i = 0; $i < 16; $i++) {
             $lastRandChars[$i] = random_int(0, 31);
        }
    

    for ($i = 0; $i < 16; $i++) {
        $randChars .= $abc[ $lastRandChars[$i]];
    }

    return  $timeChars.$randChars;
}


// echo ulid();
// echo '<br>',ulid(1469918220538);

?>

