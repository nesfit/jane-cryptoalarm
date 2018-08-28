{{ $list->links() }}
<table class="table table-striped">
    <thead>
        <tr>
            <th>#</th>
            <th>Name</th>
            <th>Coin</th>
            <th>Transaction</th>
            <th>Date</th>
        </tr>
    </thead>
    <tbody>
        @foreach($list as $item)
            <tr>
                <td>{{ $loop->iteration + $skipped }}</td>
                <td><a href="{{ action('WatchlistController@show', $item->watchlist->id) }}">{{ $item->watchlist->name }}</a></td>
                <td>{{ $item->watchlist->address->coin->name }}</td>
                <td><a href="{{ $item->watchlist->address->coin->explorer_url . $item->tx_hash }}">{{ $item->tx_hash }}</a></td>
                <td>{{ $item->created_at }}</td>
            </tr>
        @endforeach
    </tbody>
</table>
{{ $list->links() }}