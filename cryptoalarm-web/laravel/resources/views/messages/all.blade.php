@if ($errors->any())
    <div class="row">
        <div class="alert alert-danger">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div><br />
    </div>
@endif

@if (session('status'))
    <div class="row">
        <div class="alert alert-success">
            {{ session('status') }}
        </div>
    </div>
@endif


@if(session('success'))
    <div class="row">
        <div class="alert alert-success">
            {{ session('success') }}
        </div>
    </div>
@endif

@if(session('warning'))
    <div class="row">
        <div class="alert alert-warning">
            {{ session('warning') }}
        </div>
    </div>
@endif