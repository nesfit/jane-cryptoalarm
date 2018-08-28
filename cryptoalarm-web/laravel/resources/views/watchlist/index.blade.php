@extends('layouts.app')

@section('content')
<div class="container">
    @include('messages.all')
    <h1>Watchlists</h1>
    <a href="{{ action('WatchlistController@create') }}" class="btn btn-success">Create new</a>
    <br><br>
    {{ $list->links() }}
    <table class="table table-striped">
        <thead>
            <tr>
                <th>#</th>
                <th>Name</th>
                <th>Coin</th>
                <th>Address</th>
                <th>Type</th>
                <th>Notifications</th>
                <th colspan="3">Action</th>
            </tr>
        </thead>
        <tbody>
            @foreach($list as $item)
                <tr>
                    <td>{{ $loop->iteration + $skipped }}</td>
                    <td>{{ $item->name }}</td>
                    <td>{{ $item->address->coin->name }}</td>
                    <td><a href="{{ $item->address->coin->explorer_url . $item->address->hash }}">{{ $item->address->hash }}</a></td>
                    <td>{{ $item->type }}</td>
                    <td>{{ $item->notify }}</td>
                    <td><a href="{{ action('WatchlistController@show', $item->id) }}" class="btn btn-primary">Detail</a></td>
                    <td><a href="{{ action('WatchlistController@edit', $item->id) }}" class="btn btn-primary">Edit</a></td>
                    <td>
                        {{ Form::open(['method' => 'DELETE', 'action' => ['WatchlistController@destroy', $item->id]]) }}
                            <button class="btn btn-danger" type="submit">Delete</button>
                        {{ Form::close() }}
                    </td>
                </tr>
            @endforeach
        </tbody>
    </table>
    {{ $list->links() }}
<div>
@endsection