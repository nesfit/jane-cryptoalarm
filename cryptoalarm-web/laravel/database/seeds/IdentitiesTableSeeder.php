<?php

use Illuminate\Database\Seeder;
use Flynsarmy\CsvSeeder\CsvSeeder;

class IdentitiesTableSeeder extends CsvSeeder
{
    public function __construct()
    {
        $this->table = 'identities';
        $this->csv_delimiter = ';';
        $this->filename = base_path().'/database/seeds/csvs/identities.csv';
    }

    public function run()
    {
        DB::disableQueryLog();
        parent::run();
        DB::select("select setval('identities_id_seq', (SELECT MAX(id) FROM identities) + 1);");
    }
}
