@extends('layouts.app')

@section('content')
<div class="container">
    @include('messages.all')
    <h1>Dashboard</h1>
    @include('notification.list')
</div>
@endsection
