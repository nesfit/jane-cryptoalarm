<?php

namespace Cryptoalarm;

use Illuminate\Database\Eloquent\Model;

class Setting extends Model
{
    protected $primaryKey = 'key';
    protected $fillable = ['value'];
    public $timestamps = false;
}
