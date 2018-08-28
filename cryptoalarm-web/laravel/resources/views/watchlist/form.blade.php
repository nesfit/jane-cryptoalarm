<h1>{{ $title }}</h1>
<div class="form-group">
    {{ Form::label('address', 'Address:') }}
    {{ Form::text('address', isset($item) ? $item->address->hash : '', ['class' => "form-control"]) }}
</div>
<div class="form-group">
    {{ Form::label('name', 'Name:') }}
    {{ Form::text('name', isset($item) ? $item->name : '', ['class' => "form-control"]) }}
</div>
<div class="form-group">
    {{ Form::label('type', 'Type:') }}
    {{ Form::select('type', Cryptoalarm\Watchlist::getEnum('type'), isset($item) ? $item->type : '', ['class' => "form-control"]) }}
</div>
<div class="form-group">
    {{ Form::label('coin', 'Coin:') }}
    {{ Form::select('coin', $coins, isset($item) ? $item->address->coin->id : '', ['class' => "form-control"]) }}
</div>
<div class="form-group">
    {{ Form::label('notify', 'Notification:') }}
    {{ Form::select('notify', Cryptoalarm\Watchlist::getEnum('notifyType'), isset($item) ? $item->notify : '', ['class' => "form-control"]) }}
</div>
<div class="form-group">
    You can use placeholders to positions information in your emails:
    <ul>
        <li><code>{name}</code> - watchlist name</li>
        <li><code>{coin}</code> - coin name</li>
        <li><code>{address}</code> - address hash</li>
        <li><code>{txs}</code> - list of transactions</li>
    </ul>
    Both address and transaction will contain link to blockchain explorer by default.
</div>
<div class="form-group">
    {{ Form::label('email_template', 'Email template') }}
    {{ Form::textarea('email_template', isset($item) ? $item->email_template : '', ['class' => 'form-control', 'placeholder' => $email_template ]) }}
</div>
{{ Form::submit($title, ['class' => "form-control btn btn-primary"]) }}