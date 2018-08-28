@extends('layouts.app')

@section('content')
<div class="container">
    @include('messages.all')

    <div class="row">
        {{ Form::open(['method' => 'PATCH', 'action' => ['WatchlistController@update', $item->id]]) }}
            @include('watchlist.form', ['title' => 'Update watchlist: ' . $item->name])
        {{ Form::close() }}
    </div>
</div>
@endsection