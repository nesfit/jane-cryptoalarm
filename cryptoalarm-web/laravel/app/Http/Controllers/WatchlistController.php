<?php

namespace Cryptoalarm\Http\Controllers;

use Illuminate\Http\Request;
use Cryptoalarm\Notification;
use Cryptoalarm\Watchlist;
use Cryptoalarm\Coin;
use Cryptoalarm\Setting;
use Cryptoalarm\Identity;
use Cryptoalarm\AddressMatcher;

class WatchlistController extends Controller
{
    public function rules()
    {
        return [
            'name' => 'required',
            'address' => 'required',
            'type' => 'required',
            'coin' => 'required',
            'notify' => 'required',
            'email_template' => 'nullable',
        ];
    }

    public function show($id)
    {
        $email_template = Setting::findOrFail('email_template')->value;
        $item = Watchlist::where('user_id', auth()->user()->id)->findOrFail($id);
        $identities = Identity::where('address_id', $item->address_id)->get();
        $list = Notification::where('watchlist_id', $item->id)->orderBy('created_at', 'desc')->paginate(50);
        $skipped = ($list->currentPage() * $list->perPage()) - $list->perPage();
        
        return view('watchlist.show', compact('list', 'item', 'skipped', 'email_template', 'identities'));
    }

    public function index()
    {
        $list = Watchlist::where('user_id', auth()->user()->id)->paginate(50);
        $skipped = ($list->currentPage() * $list->perPage()) - $list->perPage();
        
        return view('watchlist.index',compact('list', 'skipped'));
    }

    public function create()
    {
        $email_template = Setting::findOrFail('email_template')->value;
        $coins = Coin::getPairs();
        
        return view('watchlist.create', compact('coins', 'email_template'));
    }

    public function store(Request $request)
    {
        $item = new Watchlist();
        $data = $this->validate($request, $this->rules());
        $item->saveItem($data);
        $this->restCheck($request, $data);

        return redirect('/watchlist')->with('success', 'Item created!');
    }

    public function edit($id)
    {
        $email_template = Setting::findOrFail('email_template')->value;
        $item = Watchlist::where('user_id', auth()->user()->id)->findOrFail($id);
        $coins = Coin::getPairs();

        return view('watchlist.edit', compact('item', 'id', 'coins', 'email_template'));
    }

    public function update(Request $request, $id)
    {
        $item = new Watchlist();
        $data = $this->validate($request, $this->rules());
        $data['id'] = $id;
        $item->updateItem($data);
        $this->restCheck($request, $data);

        return redirect('/watchlist')->with('success', 'Item has been updated!');
    }

    public function destroy($id)
    {
        $item = Watchlist::findOrFail($id);
        $item->delete();

        return redirect('/watchlist')->with('success', 'Item has been deleted!');
    }

    public function identify(Request $request)
    {
        $address = $request->input('address');
        $am = new AddressMatcher();
        $possible_coins = $am->identify_address($address);

        return response()->json([
            'status' => !empty($possible_coins),
            'coins' => $possible_coins,
        ]);
    }

    public function restCheck(Request $request, $data)
    {
        error_log($data['notify']);
        error_log($request->user()->rest_url);
        error_log(in_array($data['notify'], ['both', 'rest']));
        error_log(empty($request->user()->rest_url));
        if(in_array($data['notify'], ['both', 'rest']) && empty($request->user()->rest_url)) {
            $request->session()->flash('warning', 'Notifications include REST but REST URL is not set. Fill it in your profile.');
            error_log("podminka");
        }
    }
}
