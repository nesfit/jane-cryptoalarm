<?php

namespace Cryptoalarm;

use Illuminate\Database\Eloquent\Model;
use Cryptoalarm\Traits\Enums;
use Cryptoalarm\Address;

class Watchlist extends Model
{
    use Enums;

    protected $fillable = ['name', 'address_id', 'user_id', 'type', 'email_template', 'notify'];
    public $timestamps = false;
    public $type_text = null;

    protected $enumTypes = [
        'in' => 'Input',
        'out' => 'Output',
        'inout' => 'Input & output',
    ];

    protected $enumNotifyTypes = [
        'none' => 'None',
        'rest' => 'Rest',
        'email' => 'Email',
        'both' => 'Both',
    ];

    public function address()
    {
        return $this->belongsTo('Cryptoalarm\Address', 'address_id');
    }

    public function saveItem($data)
    {
        $this->user_id = auth()->user()->id;
        $this->name = $data['name'];
        $this->address_id = Address::getOrCreate($data['coin'], $data['address']);
        $this->type = $data['type'];
        $this->notify = $data['notify'];
        $this->email_template = $data['email_template'];
        $this->save();
    }

    public function updateItem($data)
    {
        $item = $this->findOrFail($data['id']);
        $item->user_id = auth()->user()->id;
        $item->name = $data['name'];
        $item->address_id = Address::getOrCreate($data['coin'], $data['address']);
        $item->type = $data['type'];
        $item->notify = $data['notify'];
        $item->email_template = $data['email_template'];
        $item->save();
    }
}
