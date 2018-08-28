<?php

namespace Cryptoalarm;

use Illuminate\Database\Eloquent\Model;

class Coin extends Model
{
    public $timestamps = false;

    public static function getPairs() 
    {
        return self::get()->mapWithKeys(function ($item) {
            return [$item['id'] => $item['name']];
        });
    }

    public static function getByName($name) 
    {
        return self::where('name', strtoupper($name))->first();
    }
}
