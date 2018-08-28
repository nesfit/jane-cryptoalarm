<?php

use Illuminate\Database\Seeder;

class CoinsTableSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $rows = [
            [1, 'BTC', 'https://blockchain.info/search?search='],
            [2, 'BCH', 'https://explorer.bitcoin.com/bch/search/'],
            [3, 'LTC', 'http://explorer.litecoin.net/search?q='],
            [4, 'DASH', 'https://explorer.dash.org/search?q='],
            [5, 'ZEC', 'https://explorer.zcha.in/search?q='],
            [6, 'ETH', 'https://etherscan.io/search?q='],
            [7, 'XMR', ''],
        ];

        foreach($rows as $row) {
            DB::table('coins')->insert([
                'id' => $row[0],
                'name' => $row[1],
                'explorer_url' => $row[2],
            ]);
        }
        DB::select("select setval('coins_id_seq', (SELECT MAX(id) FROM coins) + 1);");
    }
}
