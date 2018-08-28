@extends('layouts.app')

@section('content')
<div class="container">
    @include('messages.all')
    <h1>Edit profile</h1>

    {{ Form::open(['UserController@edit', $item->id]) }}
        <div class="form-group">
            {{ Form::label('rest_url', 'REST URL:') }}
            {{ Form::text('rest_url', isset($item) ? $item->rest_url : '', ['class' => "form-control"]) }}
        </div>
        If specified, notifications will be send to given URL as POST requests with following JSON payload:<br>
        <code>
            {
                'address': hash,
                'coin': ticker,
                'watchlist': name,
                'transactions': [hash1, hash2, ..., hashN]
            }
        </code>
        <br><br>
        <div class="form-group">
            {{ Form::submit('Save profile', ['class' => 'form-control btn btn-primary']) }}
        </div>
    {{ Form::close() }}
<div>
@endsection