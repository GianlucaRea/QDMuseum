<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Artwork_Review extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'artwork_id',
        'user_id',
        'review_title',
        'review_text',
        'stars',
    ];

    /**
     * The attributes that should be hidden for serialization.
     *
     * @var array<int, string>
     */
    protected $hidden = [

    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'review_date' => 'datetime',
    ];

    public function artwork(){
        return $this->belongsTo(Artwork::class);
    }

    public function user(){
        return $this->belongsTo(User::class);
    }
}
