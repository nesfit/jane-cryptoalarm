<?php

use Illuminate\Database\Seeder;

class WatchlistsTableSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $rows = [
            [1, 1, 1, 'inout', 'rest', 'w1'],
            [2, 2, 2, 'in', 'email', 'w2'],
            [3, 3, 3, 'out', 'email', 'w3'],
            [4, 4, 4, 'inout', 'email', 'w4'],
            [5, 5, 1, 'out', 'rest', 'w5'],
            [6, 6, 1, 'in', 'rest', 'w6'],
        ];

        foreach($rows as $row) {
            DB::table('watchlists')->insert([
                'id' => $row[0],
                'name' => $row[5],
                'type' => $row[3],
                'notify' => $row[4],
                'address_id' => $row[1],
                'user_id' => $row[2],
                'email_template' => NULL,
            ]);
        }
        DB::select("select setval('watchlists_id_seq', (SELECT MAX(id) FROM watchlists) + 1);");
    }
}
