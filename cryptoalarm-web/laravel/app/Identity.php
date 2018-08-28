<?php

namespace Cryptoalarm;

use Exception;
use Illuminate\Database\Eloquent\Model;
use lluminate\Database\QueryException;
use Cryptoalarm\Address;
use Cryptoalarm\Coin;

class Identity extends Model
{
    protected $fillable = ['label', 'url', 'source', 'address_id'];
    public $timestamps = false;

    public function saveItem($data)
    {
        $coin_id = Coin::getByName($data['coin'])->id;
        $this->label = $data['label'];
        $this->url = $data['url'];
        $this->address_id = Address::getOrCreate($coin_id, $data['address']);
        $this->source = $data['source'];
        try {
            $this->save();
        } catch (Exception $e) {
            if($e->getCode() != 23505) { // 23505 == duplicated
                throw $e;
            }
        }
    }
}
