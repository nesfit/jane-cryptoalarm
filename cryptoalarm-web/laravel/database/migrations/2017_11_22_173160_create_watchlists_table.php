<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;

class CreateWatchlistsTable extends Migration {

	/**
	 * Run the migrations.
	 *
	 * @return void
	 */
	public function up()
	{
		Schema::create('watchlists', function(Blueprint $table)
		{
			$table->increments('id');
			$table->string('name');
			$table->enum('type', ['in', 'out', 'inout']);
			$table->enum('notify', ['email', 'rest']);
			$table->integer('address_id');
			$table->integer('user_id');

			$table->foreign('address_id')->references('id')->on('addresses');
			$table->foreign('user_id')->references('id')->on('users');
		});
	}


	/**
	 * Reverse the migrations.
	 *
	 * @return void
	 */
	public function down()
	{
		Schema::dropIfExists('watchlists');
	}

}
