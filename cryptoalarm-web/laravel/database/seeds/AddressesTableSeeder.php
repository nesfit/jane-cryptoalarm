<?php

use Illuminate\Database\Seeder;
use Flynsarmy\CsvSeeder\CsvSeeder;

class AddressesTableSeeder extends CsvSeeder
{
    public function __construct()
    {
        $this->table = 'addresses';
        $this->csv_delimiter = ';';
        $this->filename = base_path().'/database/seeds/csvs/addresses.csv';
    }

    public function run()
    {
        DB::disableQueryLog();
        parent::run();
        DB::select("select setval('addresses_id_seq', (SELECT MAX(id) FROM addresses) + 1);");        
    }
}
