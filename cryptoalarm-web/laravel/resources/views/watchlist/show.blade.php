@extends('layouts.app')

@section('content')
<div class="container">
    @include('messages.all')
    <h1>Watchlist detail: {{ $item->name }} </h1>

    <div style="float:right; width:130px;">
        <a href="{{ action('WatchlistController@edit', $item->id) }}" class="btn btn-primary" style="float:left;">Edit</a>
        {{ Form::open(['method' => 'DELETE', 'action' => ['WatchlistController@destroy', $item->id]]) }}
            <button class="btn btn-danger" type="submit">Delete</button>
        {{ Form::close() }}
    </div>
        
    <br>
    Coin: {{ $item->address->coin->name }}<br>
    Address: <a href="{{ $item->address->coin->explorer_url . $item->address->hash }}">{{ $item->address->hash }}</a><br>
    Type: {{ Cryptoalarm\Watchlist::getKeyedEnum('types', $item->type) }}<br>
    Notify: {{ Cryptoalarm\Watchlist::getKeyedEnum('notifyTypes', $item->notify) }}<br>
    Email template: <br>
    <pre>{{ $item->email_template ? $item->email_template : $email_template }}</pre>
    @if($identities->isNotEmpty())
        <h2>Identities</h2>
        <table class="table table-striped">
            <tr>
                <th>Source</th>
                <th>Label</th>
            </tr>
            @foreach($identities as $item)
                <tr>
                    <td>{{ $item->source }}</td>
                    <td><a href="{{ $item->url }}">{{ $item->label }}</a></td>
                </tr>
            @endforeach
        </table>
    @endif

    <h2>Notifications</h2>
    @include('notification.list')
</div>
@endsection
