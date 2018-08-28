<?php

namespace Cryptoalarm;

class AddressMatcher {
    public $coins = [
        'btc' => ['([13][a-km-zA-HJ-NP-Z1-9]{25,33}|bc1([A-Za-z0-9]{39}|[A-Za-z0-9]{59}))'],
        'bch' => ['[13][a-km-zA-HJ-NP-Z1-9]{25,33}'],
        'ltc' => ['[LM3][a-km-zA-HJ-NP-Z1-9]{25,33}'],
        'dash' => ['X[1-9A-HJ-NP-Za-km-z]{25,33}'],
        'zec' => ['t[a-zA-Z0-9]{34}'],
        'eth' => ['0x[a-fA-F0-9]{40}'],
        'xmr' => ['4[0-9AB][[:alnum:]]{93}'],
    ];

    public function identify_address($address) {
        $result = [];

        foreach($this->coins as $coin => $regexes) {
            foreach($regexes as $regex) {
                if(preg_match('/^' . $regex . '$/', $address)) {
                    $result[] = $coin;
                    break;
                }
            }
        }

        return $result;
    }

    public function match_addresses($text) {
        $results = [];

        foreach($this->coins as $coin => $regexes) {
            foreach($regexes as $regex) {
                $matches = [];
                # spaces so it doesnt match only parts of text
                $res = preg_match_all('/ ' . $regex . ' /', $text, $matches);

                if($res) {
                    $matches[0] = array_unique($matches[0]);
                    foreach($matches[0] as $match) {
                        $results[trim($match)][] = $coin;
                    }
                }
            }
        }
        
        return $results;
    }

}

