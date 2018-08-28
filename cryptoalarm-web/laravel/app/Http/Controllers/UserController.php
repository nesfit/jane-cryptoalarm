<?php

namespace Cryptoalarm\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    public function edit()
    {
        $item = auth()->user();

        return view('user.profile', compact('item'));
    }

    public function update(Request $request)
    {
        $user = auth()->user();
        $data = $this->validate($request, ['rest_url' => 'nullable|url']);
        $user->rest_url = $data['rest_url'];
        $user->save();

        return redirect('/profile')->with('success', 'Item has been updated!');
    }
}
