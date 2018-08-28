@extends('layouts.app')

@section('content')
<div class="container">
    @include('messages.all')

    <div class="row">
        {{ Form::open(['method' => 'POST', 'action' => 'WatchlistController@store'])}}
            @include('watchlist.form', ['title' => 'Create watchlist'])
        {{ Form::close() }}
    </div>
</div>
@endsection
