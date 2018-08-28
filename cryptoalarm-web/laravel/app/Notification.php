<?php

namespace Cryptoalarm;

use Illuminate\Database\Eloquent\Model;

class Notification extends Model
{
    public $fillable = ['watchlist_id', 'block_id', 'tx_hash'];

    public function watchlist() 
    {
        return $this->belongsTo('Cryptoalarm\Watchlist', 'watchlist_id');
    }
}
