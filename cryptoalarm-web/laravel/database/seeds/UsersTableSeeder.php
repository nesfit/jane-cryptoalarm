<?php

use Illuminate\Database\Seeder;

class UsersTableSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $rows = [
            [1, 'alice'],
            [2, 'bob'],
            [3, 'carol'],
            [4, 'dave'],
        ];

        foreach($rows as $row) {
            DB::table('users')->insert([
                'id' => $row[0],
                'name' => $row[1],
                'email' => $row[1] . "@cryptoalarm.tld",
                'password' => bcrypt($row[1]),
            ]);
        }
        DB::select("select setval('users_id_seq', (SELECT MAX(id) FROM users) + 1);");
    }
}
