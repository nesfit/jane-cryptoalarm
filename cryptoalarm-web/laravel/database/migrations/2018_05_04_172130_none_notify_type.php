<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class NoneNotifyType extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        DB::beginTransaction();
        DB::statement("ALTER TABLE watchlists DROP CONSTRAINT watchlists_notify_check");
        DB::statement("ALTER TABLE watchlists ADD CONSTRAINT watchlists_notify_check CHECK (notify::text = ANY (ARRAY['email'::character varying, 'rest'::character varying, 'both'::character varying, 'none'::character varying]::text[]))");
        DB::commit();
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        DB::beginTransaction();
        DB::statement("ALTER TABLE watchlists DROP CONSTRAINT watchlists_notify_check");
        DB::statement("ALTER TABLE watchlists ADD CONSTRAINT watchlists_notify_check CHECK (notify::text = ANY (ARRAY['email'::character varying, 'rest'::character varying, 'both'::character varying]::text[]))");
        DB::commit();
    }
}
