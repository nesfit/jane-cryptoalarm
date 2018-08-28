<?php

namespace Cryptoalarm\Http\Controllers;

use Illuminate\Http\Request;
use Cryptoalarm\Watchlist;
use Cryptoalarm\Notification;

class DashboardController extends Controller
{
    public function index()
    {
        $item = Watchlist::select('id')->where('user_id', auth()->user()->id)->get();
        $list = Notification::whereIn('watchlist_id', $item)->orderBy('created_at', 'desc')->paginate(50);
        $skipped = ($list->currentPage() * $list->perPage()) - $list->perPage();
        
        return view('dashboard', compact('list', 'skipped'));
    }
}
