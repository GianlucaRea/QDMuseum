<!doctype html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- CSRF Token -->
    <meta name="csrf-token" content="{{ csrf_token() }}">

    <title>{{ config('app.name', 'Laravel') }}</title>

    <!-- Scripts -->
    <script src="{{ asset('js/app.js') }}"></script>

    <!-- Fonts -->
    <link rel="dns-prefetch" href="//fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css?family=Nunito" rel="stylesheet">


    <!-- Styles -->
    <link href="{{ asset('css/app.css') }}" rel="stylesheet">
</head>
<body>
    <div id="app">
        <main class="py-4" style="margin-bottom: 1%; margin-top: 1%">
            @yield('content')
        </main>
        <nav class="navbar navbar-expand-md navbar-light bg-white shadow-sm">
            <div class="container">
{{--                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="{{ __('Toggle navigation') }}">--}}
{{--                    <span class="navbar-toggler-icon"></span>--}}
{{--                </button>--}}

                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <!-- Left Side Of Navbar -->
                    <ul class="navbar-nav me-auto">

                    </ul>

                    <!-- Right Side Of Navbar -->
                    <ul class="navbar-nav ms-auto">
                        <!-- Authentication Links -->
                        @guest
                            @if (Route::has('login'))
                                <li class="nav-item">
                                    <a class="nav-link" href="{{ route('login') }}">{{ __('Login') }}</a>
                                </li>
                            @endif

                            @if (Route::has('register'))
                                <li class="nav-item">
                                    <a class="nav-link" href="{{ route('register') }}">{{ __('Register') }}</a>
                                </li>
                            @endif
                        @else
                            @if(Auth::user()->role == 2 || Auth::user()->role == 3)
                                <li><b>Museum Management and statistics</b>
                                    <ul>
                                        <li>
                                            <a id="navbarDropdown" class="nav-link dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" v-pre href="{{ url('/chooseMuseumForArtworkAndManagement') }}" > Manage Artworks</a>
                                        </li>
                                        <li>
                                            <a id="navbarDropdown" class="nav-link dropdown-toggle" href="{{ url('/timeslot/chooseMuseumToShow') }}" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" v-pre>
                                                Manage Time Slots
                                            </a>
                                        </li>
                                        <li>
                                            <a id="navbarDropdown" class="nav-link dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" v-pre href="{{ url('/chooseMuseumForTracking') }}" > Visitors Tracker</a>
                                        </li>
                                    </ul>
                                </li>
                            @endif
                            @if(Auth::user()->role == 1)
                                <li><b>Visit services</b>
                                    <ul>
                                        <li>
                                            <a id="navbarDropdown" class="nav-link dropdown-toggle" href="{{ url('bookingTicket') }}" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" v-pre>
                                                Booking tickets
                                            </a>
                                        </li>
                                        <li>
                                            <a id="navbarDropdown" class="nav-link dropdown-toggle" href="{{ url('tickets') }}" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" v-pre>
                                                Avaiable Tickets
                                            </a>
                                        </li>
                                        <li>
                                            <a id="navbarDropdown" class="nav-link dropdown-toggle" href="{{ url('user/visit') }}" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" v-pre>
                                                localization services
                                            </a>
                                        </li>
                                    </ul>
                                </li>
                                <li><b>Social</b>
                                    <ul>
                                        @isset($ticket_used)
                                            @if($ticket_used == True)
                                                <li>
                                                    <a id="navbarDropdown" class="nav-link dropdown-toggle" href="{{ url('feedbackMuseumsAndArtworks') }}" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" v-pre>
                                                        Give a feedback to museums and artworks!
                                                    </a>
                                                </li>
                                            @endif
                                        @endisset
                                        <li>
                                            <a id="navbarDropdown" class="nav-link dropdown-toggle" href="{{ url('socialArea') }}" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" v-pre>
                                                Go to social area
                                            </a>
                                        </li>
                                    </ul>
                                </li>
                            @endif
                            @if(Auth::user()->role == 2)
                                <li><b>tickets and tag operations</b>
                                    <ul>
                                        <li>
                                            <a id="navbarDropdown" class="nav-link dropdown-toggle" href="{{ url('ticketValidator/chooseMuseum') }}" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" v-pre>
                                                Tickets validation
                                            </a>
                                        </li>
                                        <li>
                                            <a id="navbarDropdown" class="nav-link dropdown-toggle" href="{{ url('tagDecoupling') }}" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" v-pre>
                                                Tag Decoupling
                                            </a>
                                        </li>
                                    </ul>
                                </li>
                            @endif
                                <li><b>User</b>
                                    <ul>
                                        <li class="nav-item dropdown">
                                            <a id="navbarDropdown" class="nav-link dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" v-pre href="{{ url('/user/profile') }}" >
                                                {{ Auth::user()->name }}
                                            </a>
                                        </li>
                                        <li>
                                            <a class="navbar-brand" href="{{ url('/') }}">
                                                {{ config('app.name', 'Laravel') }}
                                            </a>
                                        </li>
                                        <li>
                                            <a class="dropdown-item" href="{{ route('logout') }}"
                                               onclick="event.preventDefault();
                                                             document.getElementById('logout-form').submit();">
                                                {{ __('Logout') }}
                                            </a>
                                        </li>
                                    </ul>
                                </li>

                                <form id="logout-form" action="{{ route('logout') }}" method="POST" class="d-none">
                                    @csrf
                                </form>
                        @endguest
                    </ul>
                </div>
            </div>
        </nav>
    </div>
</body>
</html>
