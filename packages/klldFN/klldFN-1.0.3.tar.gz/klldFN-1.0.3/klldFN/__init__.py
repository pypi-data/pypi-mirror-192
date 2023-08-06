"""
“Commons Clause” License Condition v1.0
Copyright klld 2022
The Software is provided to you by the Licensor under the
License, as defined below, subject to the following condition.
Without limiting other conditions in the License, the grant
of rights under the License will not include, and the License
does not grant to you, the right to Sell the Software.
For purposes of the foregoing, “Sell” means practicing any or
all of the rights granted to you under the License to provide
to third parties, for a fee or other consideration (including
without limitation fees for hosting or consulting/ support
services related to the Software), a product or service whose
value derives, entirely or substantially, from the functionality
of the Software. Any license notice or attribution required by
the License must also include this Commons Clause License
Condition notice.
Software: klldv5
License: Apache 2.0
"""
try:
    # System imports.
    from typing import Tuple, Any, Union, Optional

    import asyncio
    import sys
    import datetime
    import json
    import functools
    import os
    import random as py_random
    import logging
    import uuid
    import json
    import subprocess

    # Third party imports.
    from fortnitepy.ext import commands
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
    from functools import partial

    from datetime import timedelta

    import crayons
    try:
        import PirxcyPinger
    except:
        pass
    import fortnitepy
    import BenBotAsync
    import FortniteAPIAsync
    import sanic
    import aiohttp
    import uvloop
    import requests

except ModuleNotFoundError as e:
    print(f'Error: {e}\nAttempting to install packages now.')

    for module in (
        'crayons',
        'PirxcyPinger',
        'fortnitepy==3.6.7',
        'BenBotAsync',
        'FortniteAPIAsync',
        'sanic==20.6.3',
        'aiohttp',
        'requests'
    ):
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

    os.system('clear')

    print('Installed packages, restarting script.')

    python = sys.executable
    os.execl(python, python, *sys.argv)


print(crayons.blue(f'klldv5 by klld'))
print(crayons.magenta(f'Discord server: https://klld.tk/discord.html - For support, questions, etc.'))


sanic_app = sanic.Sanic(__name__)
server = None

cid = ""
name = ""
friendlist = ""
password = "4635"
copied_player = ""
__version__ = "1.0.1"
adminsss = 'klld َََََ'
owner = 'e375edab04964813a886ee974b66bd70'
errordiff = 'errors.com.epicgames.common.throttled', 'errors.com.epicgames.friends.inviter_friendships_limit_exceeded'
shit_partys_errrors = 'errors.com.epicgames.social.party.invite_already_exists', 'errors.com.epicgames.social.party.party_not_found', 'errors.com.epicgames.social.party.stale_revision', 'errors.com.epicgames.social.party.party_change_forbidden', 'errors.com.epicgames.social.party.invite_forbidden'#HTTPexception (soon...)
vips = "klld َََََ"


with open('info.json') as f:
    try:
        info = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(Fore.RED + ' [ERROR] ' + Fore.RESET + "")
        print(Fore.LIGHTRED_EX + f'\n {e}')
        exit(1)


def is_vips():
    async def predicate2(ctx):
        return ctx.author.display_name in vips
    return commands.check(predicate2)

def is_admin():
    async def predicate(ctx):
        return ctx.author.display_name in info['FullAccess']
    return commands.check(predicate)


#only me ()
def is_owner():
    async def predicate1(ctx):
        return ctx.author.id in owner
    return commands.check(predicate1)


prefix = '!','?','/','',' ','+'



@sanic_app.middleware('response')
async def custom_banner(request: sanic.request.Request, response: sanic.response.HTTPResponse):
    response.headers["Access-Control-Allow-Origin"] = "*/*"


@sanic_app.route('/', methods=['GET'])
async def root(request: sanic.request.Request) -> None:
    if 'Accept' in request.headers and request.headers['Accept'] == 'application/json':
        return sanic.response.json(
            {
                "status": "online"
            }
        )

    return sanic.response.html(
        """
<style> 
input[type=text] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
}
</style>
</head>
<body>
<title>klldv5.4</title>
<link href="https://ezfn.dev/assets/libs/tiny-slider/tiny-slider.css" rel="stylesheet">
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v6.2.0/css/all.css">
<link href="https://ezfn.dev/assets/css/bootstrap-dark.min.css" class="theme-opt" rel="stylesheet" type="text/css">

<link href="https://ezfn.dev/assets/css/icons.min.css" rel="stylesheet" type="text/css">
<link href="https://ezfn.dev/assets/libs/@iconscout/unicons/css/line.css" type="text/css" rel="stylesheet">

<link href="https://ezfn.dev/assets/css/style-dark.min.css" class="theme-opt" rel="stylesheet" type="text/css">


<link rel="shortcut icon" href="">

<link href="https://ezfn.dev/assets/libs/tiny-slider/tiny-slider.css" rel="stylesheet">
<link href="https://ezfn.dev/assets/libs/tobii/css/tobii.min.css" rel="stylesheet">

<link href="https://ezfn.dev/assets/css/bootstrap-dark.min.css" class="theme-opt" rel="stylesheet" type="text/css">

<link href="https://ezfnv2-cloudflare-pages.pages.dev/assets/css/icons.min.css" rel="stylesheet" type="text/css">
<link href="https://ezfnv2-cloudflare-pages.pages.dev/assets/libs/@iconscout/unicons/css/line.css" type="text/css" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.2/css/all.min.css" rel="stylesheet" integrity="sha512-1sCRPdkRXhBV2PBLUdRb4tMg1w2YPf37qatUFeS7zlBy7jJI8Lf4VHwWfZZfpXtYSLy85pkm9GaYVYMfw5BC1A==" crossorigin="anonymous" referrerpolicy="no-referrer">

<link href="https://ezfn.dev/assets/css/style-dark.min.css" class="theme-opt" rel="stylesheet" type="text/css">





  
<script src="https://partner.googleadservices.com/gampad/cookie.js?domain=v2.ezfn.dev&amp;callback=_gfp_s_&amp;client=ca-pub-8899997837601633&amp;cookie=ID%3Dbc06fea3bc69b073-22cade575dd4005e%3AT%3D1658961486%3ART%3D1658961486%3AS%3DALNI_MZmtaI4YI05RHlccI_4qg3oCTVs6A"></script><script src="https://pagead2.googlesyndication.com/pagead/managed/js/adsense/m202207210101/show_ads_impl_with_ama_fy2019.js?client=ca-pub-8899997837601633&amp;plah=v2.ezfn.dev&amp;bust=31068585" id="google_shimpl"></script><script src="assets/js/cookiehelper.js"></script>

<script data-ad-client="ca-pub-8899997837601633" async="" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" data-checked-head="true"></script>
<meta http-equiv="origin-trial" content="AzoawhTRDevLR66Y6MROu167EDncFPBvcKOaQispTo9ouEt5LvcBjnRFqiAByRT+2cDHG1Yj4dXwpLeIhc98/gIAAACFeyJvcmlnaW4iOiJodHRwczovL2RvdWJsZWNsaWNrLm5ldDo0NDMiLCJmZWF0dXJlIjoiUHJpdmFjeVNhbmRib3hBZHNBUElzIiwiZXhwaXJ5IjoxNjYxMjk5MTk5LCJpc1N1YmRvbWFpbiI6dHJ1ZSwiaXNUaGlyZFBhcnR5Ijp0cnVlfQ=="><meta http-equiv="origin-trial" content="A6+nc62kbJgC46ypOwRsNW6RkDn2x7tgRh0wp7jb3DtFF7oEhu1hhm4rdZHZ6zXvnKZLlYcBlQUImC4d3kKihAcAAACLeyJvcmlnaW4iOiJodHRwczovL2dvb2dsZXN5bmRpY2F0aW9uLmNvbTo0NDMiLCJmZWF0dXJlIjoiUHJpdmFjeVNhbmRib3hBZHNBUElzIiwiZXhwaXJ5IjoxNjYxMjk5MTk5LCJpc1N1YmRvbWFpbiI6dHJ1ZSwiaXNUaGlyZFBhcnR5Ijp0cnVlfQ=="><meta http-equiv="origin-trial" content="A/9La288e7MDEU2ifusFnMg1C2Ij6uoa/Z/ylwJIXSsWfK37oESIPbxbt4IU86OGqDEPnNVruUiMjfKo65H/CQwAAACLeyJvcmlnaW4iOiJodHRwczovL2dvb2dsZXRhZ3NlcnZpY2VzLmNvbTo0NDMiLCJmZWF0dXJlIjoiUHJpdmFjeVNhbmRib3hBZHNBUElzIiwiZXhwaXJ5IjoxNjYxMjk5MTk5LCJpc1N1YmRvbWFpbiI6dHJ1ZSwiaXNUaGlyZFBhcnR5Ijp0cnVlfQ=="><script async="" src="https://fundingchoicesmessages.google.com/i/ca-pub-8899997837601633?ers=2"></script><link rel="preload" href="https://adservice.google.co.uk/adsid/integrator.js?domain=v2.ezfn.dev" as="script"><script type="text/javascript" src="https://adservice.google.co.uk/adsid/integrator.js?domain=v2.ezfn.dev"></script><link rel="preload" href="https://adservice.google.com/adsid/integrator.js?domain=v2.ezfn.dev" as="script"><script type="text/javascript" src="https://adservice.google.com/adsid/integrator.js?domain=v2.ezfn.dev"></script><script async="" src="https://fundingchoicesmessages.google.com/f/AGSKWxU1qVDBsyiWGQnuJPFQqO_Zw2_MDwF81gulZRB8mNGjYel_ZWa95XFCrtvIeb7Ek88ZgZXhGz5fgFqbC4tg9U8=?fccs=W1siQUtzUm9sLVpRMnBFRVN3cG1WUDFUOUg5MHpBN3E4UWdybEI4ckxkR20xR0dMTEJ5RHkweDIyVVpRc3FXa1FPMkYtUTl4Rk1HZEtjdEdaczhUeUlqbUtDREZvYjZLRkJkNkpaTGRuaTlVMU9QTUZ3TE1ldTJ5Zm5ubDFKWGNvTzczUi1UOTNIRGJubGlYWjJ6X29hdDZXX001dFVHeW5JLUdnPT0iXSxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsWzE2NTg5NjE1NzEsOTU2MDAwMDAwXSwiRjU0MDZEQTAtMUY4NS00RTI2LTg5OTEtNEU1MDIwNUU0MkNGIiwiQzQ3OTJCRjctMEI5Mi00NUY3LTk4N0MtMTAwRjUxOEFBMzg5IixudWxsLFtudWxsLFs3XSxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsdHJ1ZSx0cnVlXSwiaHR0cHM6Ly92Mi5lemZuLmRldi9sb2JieS11dGlscy5odG1sIixudWxsLFtdXQ"></script><script async="" src="https://fundingchoicesmessages.google.com/f/AGSKWxWMcJ8g_5uotAQoH4szEda_7DtEvcZHVgymlfkElepthNL-DZoUkVtqmNirMzWGZ6CCHDpiAJhW0P6QP3R2tgNz_kP300oiQm5IhymEj-ALH9AfCXq6lcIha1jPKql1VFKgbPxJEQ==?fccs=W1siQUtzUm9sLVpRMnBFRVN3cG1WUDFUOUg5MHpBN3E4UWdybEI4ckxkR20xR0dMTEJ5RHkweDIyVVpRc3FXa1FPMkYtUTl4Rk1HZEtjdEdaczhUeUlqbUtDREZvYjZLRkJkNkpaTGRuaTlVMU9QTUZ3TE1ldTJ5Zm5ubDFKWGNvTzczUi1UOTNIRGJubGlYWjJ6X29hdDZXX001dFVHeW5JLUdnPT0iXSxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsWzE2NTg5NjE1NzIsMjIwMDAwMDBdLG51bGwsbnVsbCxudWxsLFtudWxsLFs3LDEwXSxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsMSwxXSwiaHR0cHM6Ly92Mi5lemZuLmRldi9sb2JieS11dGlscy5odG1sIixudWxsLFtdXQ"></script><script async="" src="https://fundingchoicesmessages.google.com/f/AGSKWxWyznmSFC0BolMJ1hV4S3L-2-CLHWPAwiauj68zM4aNOmUfG0vcuDZhhI-KeFGwM2O4qVQHUKOyDJVJ1NmxGvabF9exBsJmnXjE9mEJFJ7eyRgUXaIZKSscfzus0IsxHoYHtQXCqA==?fccs=W1siQUtzUm9sLVpRMnBFRVN3cG1WUDFUOUg5MHpBN3E4UWdybEI4ckxkR20xR0dMTEJ5RHkweDIyVVpRc3FXa1FPMkYtUTl4Rk1HZEtjdEdaczhUeUlqbUtDREZvYjZLRkJkNkpaTGRuaTlVMU9QTUZ3TE1ldTJ5Zm5ubDFKWGNvTzczUi1UOTNIRGJubGlYWjJ6X29hdDZXX001dFVHeW5JLUdnPT0iXSxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsWzE2NTg5NjE1NzIsNzczMDAwMDAwXSxudWxsLG51bGwsbnVsbCxbbnVsbCxbNywxMCw2XSxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsMSwxLG51bGwsbnVsbCwxXSwiaHR0cHM6Ly92Mi5lemZuLmRldi9sb2JieS11dGlscy5odG1sIixudWxsLFtdXQ"></script></head>
<body>

<!-- Navbar Start -->
        <header id="topnav" class="defaultscroll sticky">
            <div class="container">
                <!-- Logo container-->
                <a class="logo" href="https://klld.42web.io/">
                    <img src="https://www.klld.tk/klld" height="34" class="logo-light-mode" alt="">
                    <img src="https://www.klld.tk/klld" height="34" class="logo-dark-mode" alt="">
                klld.42web.io
                </a>                
                <!-- Logo End -->

                <!-- End Logo container-->
                

<ul class="buy-button list-inline mb-0">
                    <li class="list-inline-item ps-1 mb-0" id="discord-invite-li">
                        <a href="https://discord.com/invite/" target="_blank" class="btn btn-soft-primary ms-1"><i class="fab fa-discord"></i></a>
                    </li>

                    <li class="list-inline-item ps-1 mb-0">
                        <a href="https://www.youtube.com/@klld?sub_confirmation=1" class="btn btn-soft-danger ms-1" target="_blank"><i class="fab fa-youtube"></i> Subscribe</a>
                    </li>
            
                    </div>
                        </a>
                    </li>
                </ul>


</header>


<section class="bg-half-170 bg-light d-table w-100">
<div class="container">
<div class="row mt-5 justify-content-center">
<div class="col-lg-8 text-center">
<div class="pages-heading">
<h4 class="title mb-0">Lobbybot</h4>
</div>
</div> 
</div>
<div class="position-breadcrumb">
<nav aria-label="breadcrumb" class="d-inline-block">
<ul class="breadcrumb rounded shadow mb-0 px-4 py-2">
<li class="breadcrumb-item"><a href="https://www.klld.tk">klld</a></li>
<li class="breadcrumb-item active" aria-current="page">Lobbybot</li>
</ul>
</nav>
</div>
</div> 
</section>
<div class="position-relative">
<div class="shape overflow-hidden text-color-white">
<svg viewBox="0 0 2880 48" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M0 48H1437.5H2880V0H2160C1442.5 52 720 0 720 0H0V48Z" fill="currentColor"></path>
</svg>
</div>
</div>


<section class="section">
            <div class="container">
                <div class="row">
                    <div class="col-md-4 mt-4 pt-2">
                        <ul class="nav nav-pills nav-justified flex-column rounded shadow p-3 mb-0" id="pills-tab" role="tablist">
                            <li class="nav-item">
                                <a class="nav-link rounded active" id="dashboard" data-bs-toggle="pill" href="#dash" role="tab" aria-controls="dash" aria-selected="false">
                                    <div class="text-start py-1 px-3">
                                        <h6 class="mb-0"><i class="uil uil-dashboard h5 align-middle me-2 mb-0"></i> Dashboard</h6>
                                    </div>
                                </a><!--end nav link-->
                            </li>
                            
                      

                            

                            <li class="nav-item mt-2">
                                    <a href="http://klld.42web.io/Public.php" class="nav-link rounded" role="" aria-controls="" aria-selected="false">
                                    <div class="text-start py-1 px-3">
                                        <h6 class="mb-0"><i class="uil uil-robot h5 align-middle me-2 mb-0"></i> View Public Helpers</h6>
                                    </div>
                                </a><!--end nav link-->
                            </li><!--end nav item-->
                        
                        </ul><!--end nav pills-->
                    </div><!--end col-->
<div class="col-md-8 col-12 mt-4 pt-2">
<div class="tab-content" id="pills-tabContent">
<div class="tab-pane fade shadow rounded p-4 active show" id="dash" role="tabpanel" aria-labelledby="dashboard">
<!-- modify this form HTML and place wherever you want your form -->
<form


<!-- name -->


<div class="container-fluid" id="page-content">
<div class="container-fluid">

<div class="d-sm-flex align-items-center justify-content-between mb-4">
""" + f""" Online now {name} """ + """
<h1 class="h3 mb-0 text-gray-800"></h1>

<a target="_blank" href="" title="">
<img draggable="false" src="" height="0px" draggable="false" alt="wda">
</a>⠀⠀                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

<a href="/" class="d-none d-sm-inline-block btn btn-sm btn-warning shadow-sm"><i class="fas fa-redo"></i> Refresh</a>
</div>
<div class="row">



<div class="col-xl-3 col-md-6 mb-4">
<div class="card border-left-white shadow h-100 py-2">
<div class="card-body">
<div class="row no-gutters align-items-center">
<div class="col mr-2">
<div class="text-xs font-weight-bold text-warning text-uppercase mb-1">PLATFORM</div>
<div class="h5 mb-0 font-weight-bold text-black">""" + f"""{platform} """ + """</div>
</div>
<div class="col-auto">
</div>
</div>
</div>
</div>
</div>

  
<div class="col-xl-3 col-md-6 mb-4">
<div class="card border-left-white shadow h-100 py-2">
<div class="card-body">
<div class="row no-gutters align-items-center">
<div class="col mr-2">
<div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Party</div>
<div class="h5 mb-0 font-weight-bold text-gray-900">""" + f"""{party_size} """ + """ / 16</div>
</div>
<div class="col-auto">
<i class="fas fa-users fa-2x text-gray-900"></i>
</div>
</div>
</div>
</div>
</div>

<div class="col-xl-3 col-md-6 mb-4">
<div class="card border-left-white shadow h-100 py-2">
<div class="card-body">
<div class="row no-gutters align-items-center">
<div class="col mr-2">
<div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Friends</div>
<div class="h5 mb-0 font-weight-bold text-gray-900">""" + f"""{friendlist} """ + """ / 5000</div>
</div>
<div class="col-auto">
<i class="fas fa-user-friends fa-2x text-gray-900"></i>
</div>
</div>
</div>
</div>
</div>

<div class="col-xl-3 col-md-6 mb-4">
<div class="card border-left-white shadow h-100 py-2">
<div class="card-body">
<div class="row no-gutters align-items-center">
<div class="col mr-2">
<div class="text-xs font-weight-bold text-warning text-uppercase mb-1">CID</div>
<div class="h5 mb-0 font-weight-bold text-gray-900">""" + f"""{skin} """ + """</div>
</div>
<div class="col-auto">
<i class="fas fa-cog fa-2x text-gray-900"></i>
</div>
</div>
</div>
</div>
</div>



</form>
</div>


 </div>
</div>
</div>
</div>
</div>
</div>
</div>
</section>



<footer class="footer footer-bar">
<div class="footer-py-30">
<div class="container text-center">
<div class="row align-items-center">
<div class="col-sm-6">

</div>
<div class="col-sm-6 mt-4 mt-sm-0 pt-2 pt-sm-0">
<ul class="list-unstyled social-icon foot-social-icon text-sm-end mb-0">
<li class="list-inline-item mb-0"><a href="https://www.youtube.com/@kllD" target="_blank" class="rounded"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-youtube fea icon-sm fea-social"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"></path><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon></svg></a></li>
</ul>
</div>
</div>
</div>
</div>







<script src="http://klld.42web.io/klld/bootstrap.bundle.min.js"></script>
<script src="http://klld.42web.io/klld/feather.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js" integrity="sha512-894YE6QWD5I59HgZOGReFYm4dnWc1Qt5NtvYSaNcOP+u1T9qYdvdihz0PPSiiqn/+/3e7Jo4EaG7TubfWGUrMQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script>
            function changeTheme() {
                if (
                    document.getElementsByClassName('theme-opt')[1].href == "klld/style.min.css"
                ) {
                    setTheme('style-dark');
                } else {
                    setTheme('style-light');
                }
            }
        </script>

<script src="http://klld.42web.io/klld/tiny-slider.js"></script>

<script src="http://klld.42web.io/klld/plugins.init.js"></script><style type="text/css">.typewrite > .wrap { border-right: 0.08em solid transparent}</style>
<script src="http://klld.42web.io/klld/app.js"></script>


  
</html>
        """
    )


@sanic_app.route("/default")
async def index(request):
    return sanic.response.json(
        {
            "username": name,
            "friend_count": friendlist,
            "cid": cid
        }
    )

@sanic_app.route('/ping', methods=['GET'])
async def accept_ping(request: sanic.request.Request) -> None:
    return sanic.response.json(
        {
            "status": "online"
        }
    )


@sanic_app.route('/name', methods=['GET'])
async def display_name(request: sanic.request.Request) -> None:
    return sanic.response.json(
        {
            "display_name": name
        }
    )


class klldFN(commands.Bot):
    def __init__(self, device_id: str, account_id: str, secret: str, loop=asyncio.get_event_loop(), **kwargs) -> None:

        self.status = '🔥 {party_size} / 16 | klld.42web.io 🎁'
        
        self.fortnite_api = FortniteAPIAsync.APIClient()
        self.loop = asyncio.get_event_loop()

        super().__init__(
            command_prefix=prefix,
            case_insensitive=True,
            auth=fortnitepy.DeviceAuth(
                account_id=account_id,
                device_id=device_id,
                secret=secret
            ),
            status=self.status,
            platform=fortnitepy.Platform('PS5'),
            **kwargs
        )

        self.session = aiohttp.ClientSession()

        self.skin = "CID_NPC_Athena_Commando_M_Apparition_Heavy"
        self.backpack = "Backpack_FNBirthday5"
        self.pickaxe = "Pickaxe_ID_376_FNCS"
        self.banner = "BRS19_ShowdownPanda"
        self.bn_color = "defaultcolor22"
        self.level = 1000
        self.tier = 1000
        self.uptimerobot_key = ""
        self.remove_bots = ""

        self.sanic_app = sanic_app
        self.server = server



        self.rst = "F"
        self.vr = "0.0"
        self.bl = "0.0"

        self.ban_player = ""
        self.bl_msg = ""
        self.ban_lobbybots = ""

        self.bl_inv = 'klld َََََ'
        self.inv_on = "F"
 
        self.adminx = "klld َََََ"
 
        self.inv_all = "F"
        self.url = f"https://{os.getenv('REPL_SLUG')}.{os.getenv('REPL_OWNER')}.repl.co"
 
        self.skin_bl = ("")
        self.add_auto = ''
        self.number = ""
 
 
        self.inv_msg  = ""
        self.add_msg  = ""
        self.join_msg = ""
    
        
 
 
    async def add_list(self) -> None:
        try:
            if 'e375edab04964813a886ee974b66bd70' in self.friends:
                await asyncio.sleep(0)
            else:
                await self.add_friend('e375edab04964813a886ee974b66bd70')
        except: pass
 
#///////////////////////////////////////////////////////////////////////////////////////////////////////////// CHECK/ERROR/PARTY ////////////////////////////////////////////////////////////////////////////////////////////////////////        
    
    async def check_party_validity(self):
        await asyncio.sleep(80)
        try:
            await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
        except:
            pass
        await asyncio.sleep(80)
 
 
#///////////////////////////////////////////////////////////////////////////////////////////////////////////// FRIENDS/ADD ////////////////////////////////////////////////////////////////////////////////////////////////////////
    
 
 
    async def set_and_update_party_prop(self, schema_key: str, new_value: Any) -> None:
        prop = {schema_key: self.party.me.meta.set_prop(schema_key, new_value)}

        await self.party.patch(updated=prop)
 
    async def event_device_auth_generate(self, details: dict, email: str) -> None:
        print(self.user.display_name)
 
 
 
    async def event_ready(self) -> None:
        global name
        global friendlist
        global cid
        global platform
        global skin
        global party_size
        name = self.user.display_name
        #get user outfit
        cid = self.party.me.outfit
        party_size = self.status
        skin = self.skin
        platform =  self.platform
        friendlist = len(self.friends)
 
        print(Fore.GREEN + "[+] " + Fore.RESET + f"Client ready as {self.user.display_name}.")
      
        if self.party.me.leader:
          await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)


        coro = self.sanic_app.create_server(
            host='0.0.0.0',
            port=8000,
            return_asyncio_server=True,
            access_log=False
        )
        self.server = await coro
 
        await asyncio.sleep(3)


        self.loop.create_task(self.add_list())

        #self.loop.create_task(self.invitefriends())

        self.loop.create_task(self.pinger())
        self.loop.create_task(self.update_api())
        #self.loop.create_task(self.uptimerobot())

        #self.loop.create_task(self.delete_pending_on_start())
        self.loop.create_task(self.checker_skin_bl())
        #self.loop.create_task(self.checker_status())
        #await asyncio.sleep(4)
        
        
        self.loop.create_task(self.delete_friends_last_logout())

        self.loop.create_task(self.auto_add_s())
        self.loop.create_task(self.check_update())
        self.loop.create_task(self.update_settings())

        

        try:   
          #print(f'Incoming pending friends: {len(self.incoming_pending_friends)}')

          for pending in self.incoming_pending_friends:
            try:
              epic_friend = await pending.accept()
              if isinstance(epic_friend, fortnitepy.Friend):
                  print(f"Accepted: {epic_friend.display_name}.")
              else:
                  print(f"Declined: {pending.display_name}.")
            except fortnitepy.InviteeMaxFriendshipsExceeded:
              await pending.decline()
              print(f"Declined: {pending.display_name}.")

              print(f"Declined: {pending.display_name}.")
              
            except fortnitepy.HTTPException as epic_error:
                if epic_error.message_code != 'errors.com.epicgames.common.throttled':
                    raise
                await asyncio.sleep(int(epic_error.message_vars[0] + 1))
                try:
                  await pending.accept()
                  print(f"Accepted: {pending.display_name}.")
                except:
                  try:
                    await pending.decline()
                    print(f"Declined: {pending.display_name}.")
                  except:
                    pass
            except:
              try:
                await pending.decline()
                print(f"Declined: {pending.display_name}.")
              except:
                print(f'Unable to accept or decine friend request from {pending.display_name}.')

        except:
          print('error in incoming')
        print(f'Incoming pending friends: {len(self.incoming_pending_friends)}')



      
#remove friends if the name is in my blacklist or pirxcys blacklist :)
        await asyncio.sleep(2)
        if self.remove_bots == "T":
          for friend in self.friends:
            if friend.display_name in self.ban_lobbybots or friend.id in self.ban_lobbybots or any(word in friend.display_name for word in self.ban_player):
              await friend.block()
              print(f'removed {friend} because its a lobbybot :)')





 
    async def auto_add_s(self):

      try:
        r = requests.get(f"https://809b9962-e06e-42a8-adbc-430422ac54c8.id.repl.co/v5/add_auto").json()
      except:
        pass
      
      self.add_auto_check = r['name']
      self.added = r['active']

      if not self.add_auto_check == self.add_auto:
        self.add_auto = self.add_auto_check

      if self.added == 'T':
        try:
            user = await self.fetch_user(self.add_auto)
            friends = self.friends

            if user.id in friends:
                print(f'I already have {user.display_name} as a friend')
            else:
              try:
                await self.add_friend(user.id)
                print(f'Sent ! I send a  friend request to {user.display_name}.')
              except:
                pass

        except fortnitepy.HTTPException:
            print("There was a problem trying to add this friend.")
        except AttributeError:
            print("I can't find a player with that name.")
 
    #async def checker_status(self):
      #async with aiohttp.ClientSession() as session:
        #async with session.request(
            #method="GET",
            #url="https://control-bot-v3.mathyslolx.repl.co/status.json"
        #) as r:
            #data = await r.json()
 
           # if r.status == 200:
              #  self.status_verif = data['status']
 
                #if not self.status_verif == self.status:
                   # self.status = self.status_verif
 
                   # await self.set_presence(self.status)
                   # await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
 
    async def checker_skin_bl(self):

      try:
        jk = requests.get(f"52e6d591-d1e6-4f14-ab73-51efe135109e.id.repl.co/v5/skinbl").json()
      except:
        pass
 

      self.skinbl_check = jk['skinbl']

      if not self.skinbl_check == self.skin_bl:
          self.skin_bl = self.skinbl_check


    #async def uptimerobot(self):#deleted
      #name = self.user.display_name

      #try:
        
        #url = "https://api.uptimerobot.com/v2/newMonitor"
                  
        #payload = f"api_key={self.uptimerobot_key}&format=json&type=1&url=https://{os.environ['REPL_ID']}.id.repl.co&friendly_name={name}"
        #headers = {
           # 'cache-control': "no-cache",
          #  'content-type': "application/x-www-form-urlencoded"
             # }
                  
       # response = requests.request("POST", url, data=payload, headers=headers)
        #print('Uploaded to uptimerobot')
     # except:
       # print('Unable to upload in uptimerobot, do it manually')


    async def pinger(self):
        try:
            await PirxcyPinger.post(f"https://{os.environ['REPL_ID']}.id.repl.co")
        except:
            pass
        return

      
    
    #test for delete online friend with las logout 80 hours
    async def delete_friends_last_logout(self):
      now = datetime.datetime.now()
      try:
        for friend in self.friends:
          if friend.last_logout < now - timedelta(hours=200):
              await friend.remove()
              print(f'Removed {friend}')
      except:
        pass





 
    async def update_api(self) -> None:
        resp = requests.post(
                url=f'52e6d591-d1e6-4f14-ab73-51efe135109e.id.repl.co/update',
                json={
                    "url": f"https://{os.environ['REPL_ID']}.id.repl.co"}
                    )
        try:
            await resp.json()
        except:
            pass
        return
 

    async def update_settings(self) -> None:
        while True:
          global vips
          global adminsss
          global __version__

          try:
            e = requests.get(f"https://809b9962-e06e-42a8-adbc-430422ac54c8.id.repl.co/v5/restart").json()
          except:
            pass
          self.rst = e['restarting']
          self.vr = e['version']
          self.bl = e['versionbl']

          if self.rst == 'T':
              print('True for restarting')

              if not self.vr == self.bl:
                  python = sys.executable
                  os.execl(python, python, *sys.argv)



          try:
            z = requests.get(f"https://809b9962-e06e-42a8-adbc-430422ac54c8.id.repl.co/v5/default").json()
          except:
            pass
          self.skin_check = z['skin']
          self.backpack_check = z['sac']
          self.pickaxe_check = z['pioche']
          self.banner_check = z['banner']
          self.bn_color_check = z['bn_color']
          self.level_check = z['level']
          self.tier_check = z['tier']
          self.add_msg_check = z['add_msg']
          self.inv_msg_check = z['inv_msg']
          self.inv_all_check = z['inv_all']
          self.join_msg_check = z['join_msg']
          self.vips_check = z['admin']
          self.versiongame = z['version_web']
          self.inv_bl = z['bl_inv']
          self.inv_on_check = z['inv_on']
          self.number_check = z['style']
          self.adminsss = z['admin']
          self.status_verif = z['status']
          self.uptimerobot_key_check = z['uptimerobot_apikey']
          self.remove_bots_check = z['remove_bots']

          
          if not self.remove_bots_check == self.remove_bots:
              self.remove_bots = self.remove_bots_check
                      
          if not self.status_verif == self.status:
              self.status = self.status_verif

              await self.set_presence(self.status)
              try:
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
              except:
                pass

          if not self.adminsss == adminsss:
              adminsss = self.adminsss

          if not self.uptimerobot_key_check == self.uptimerobot_key:
              self.uptimerobot_key = self.uptimerobot_key_check

            
          if not self.number_check == self.number:
              self.number = self.number_check
              try:
                await self.party.me.set_outfit(asset=self.skin,variants=self.party.me.create_variants(material=self.number,clothing_color=self.number,parts=self.number,progressive=self.number))
              except:
                pass

          if not self.inv_on_check == self.inv_on:
              self.inv_on = self.inv_on_check

          if not self.inv_bl == self.bl_inv:
              self.bl_inv = self.inv_bl

          if not self.versiongame == __version__:
              __version__ = self.versiongame

          if not self.vips_check == vips:
              vips = self.vips_check

          if not self.skin_check == self.skin:
              self.skin = self.skin_check

          if not self.backpack_check == self.backpack:
              self.backpack = self.backpack_check

          if not self.pickaxe_check == self.pickaxe:
              self.pickaxe = self.pickaxe_check

          if not self.banner_check == self.banner:
              self.banner == self.banner_check

          if not self.bn_color_check == self.bn_color:
              self.bn_color = self.bn_color_check

          if not self.level_check == self.level:
              self.level = self.level_check

          if not self.tier_check == self.tier:
              self.tier = self.tier_check

          if not self.add_msg_check == self.add_msg:
              self.add_msg = self.add_msg_check

          if not self.inv_msg_check == self.inv_msg:
              self.inv_msg = self.inv_msg_check

          if not self.join_msg_check == self.join_msg:
              self.join_msg = self.join_msg_check

          if not self.inv_all_check == self.inv_all:
              self.inv_all = self.inv_all_check



          try:
            await self.party.me.set_outfit(asset=self.skin)
            await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
          except:
            pass

          try:
            v = requests.get(f"https://809b9962-e06e-42a8-adbc-430422ac54c8.id.repl.co/v5/kick").json()
          except:
            pass
          self.ban_player_check = v['ban']
          self.bl_msg_checks = v['bl_msg']

          if not self.ban_player_check == self.ban_player:
              self.ban_player = self.ban_player_check

          if not self.bl_msg_checks == self.bl_msg:
              self.bl_msg = self.bl_msg_checks

          try:
            try:
              hgd = requests.get(f"https://809b9962-e06e-42a8-adbc-430422ac54c8.id.repl.co/v5/blacklist").json()
            except: 
              pass

            
            self.ban_lobbybots_check = hgd['blocked_names']
  
  
            if not self.ban_lobbybots_check== self.ban_lobbybots:
                self.ban_lobbybots = self.ban_lobbybots_check

          except:
            pass

          await asyncio.sleep(3600)#1 hour


 
    async def check_update(self):
        await asyncio.sleep(40)
        self.loop.create_task(self.update_settings())
        await asyncio.sleep(40)
        self.loop.create_task(self.check_update())
 
    async def event_party_invite(self, invite: fortnitepy.ReceivedPartyInvitation) -> None:
        if invite.sender.display_name in info['FullAccess']:
            await invite.accept()
        elif self.inv_on == 'T':
          try:
            await invite.accept()
          except fortnitepy.HTTPException:
            pass
        elif invite.sender.display_name in self.adminx:
          try:
            await invite.accept()
          except fortnitepy.HTTPException:
            pass
          except AttributeError:
            pass
          except fortnitepy.PartyError:
            pass
          except fortnitepy.Forbidden:
            pass
          except fortnitepy.PartyIsFull: 
            pass
        else:
          try:
            await invite.decline()
            await invite.sender.send(self.inv_msg)
            await invite.sender.invite()
          except fortnitepy.HTTPException:
            pass
          except AttributeError:
            pass
          except fortnitepy.PartyError:
            pass
          except fortnitepy.Forbidden:
            pass
          except fortnitepy.PartyIsFull:
            pass
          except:
            pass
 
    async def event_friend_presence(self, old_presence: Union[(None, fortnitepy.Presence)], presence: fortnitepy.Presence):
        if not self.is_ready():
            await self.wait_until_ready()
        if self.inv_all == 'T':
            if old_presence is None:
                friend = presence.friend
                if friend.display_name != self.bl_inv:
                    try:
                        await friend.send(self.inv_msg)
                    except:
                        pass
                    else:
                        if not self.party.member_count >= 16:
                          try:
                            await friend.invite()
                          except:
                            pass
 
    async def event_party_member_update(self, member: fortnitepy.PartyMember) -> None:
        name = member.display_name
        if any(word in name for word in self.ban_player):
            try:
                await member.kick()
            except: pass
    
        if member.display_name in self.ban_player:
            try:
                await member.kick()
            except: pass
    
        if member.outfit in (self.skin_bl) and member.id != self.user.id:
            await member.kick()
 

 
    async def event_friend_request(self, request: fortnitepy.IncomingPendingFriend) -> None:
      if isinstance(request, fortnitepy.OutgoingPendingFriend):
          return

      print(f"Received friend request from: {request.display_name}.")
      try:
        await request.accept()
        print(f"Accepted friend request from: {request.display_name}.")

      except fortnitepy.InviteeMaxFriendshipsExceeded:
        await request.decline()

        print('delete 1 dans event friend req')
      except fortnitepy.MaxFriendshipsExceeded:
        request.decline()
 
    async def event_friend_add(self, friend: fortnitepy.Friend) -> None:
        try:
            await asyncio.sleep(0.3)
            await friend.send(self.add_msg.replace('{DISPLAY_NAME}', friend.display_name))
            await friend.invite()
        except: pass

    async def event_friend_remove(self, friend: fortnitepy.Friend) -> None:
        try:
            await self.add_friend(friend.id)
        except: pass


    async def event_party_member_join(self, member: fortnitepy.PartyMember) -> None:
      try:
        await self.party.send(self.join_msg.replace('{DISPLAY_NAME}', member.display_name))
 
        if self.default_party_member_config.cls is not fortnitepy.party.JustChattingClientPartyMember:
            await self.party.me.edit(functools.partial(self.party.me.set_outfit,self.skin,variants=self.party.me.create_variants(material=self.number,clothing_color=self.number,parts=self.number,progressive=self.number)),functools.partial(self.party.me.set_backpack,self.backpack),functools.partial(self.party.me.set_pickaxe,self.pickaxe),functools.partial(self.party.me.set_banner,icon=self.banner,color=self.bn_color,season_level=self.level),functools.partial(self.party.me.set_battlepass_info,has_purchased=True,level=self.tier))
 
            if not self.has_friend(member.id):
                try:
                    await self.add_friend(member.id)
                except: pass
 
            name = member.display_name
            if any(word in name for word in self.ban_player):
                try:
                    await member.kick()
                except: pass
 
            if member.display_name in self.ban_player:
                try:
                    await member.kick()
                except: pass
 
            if member.outfit in (self.skin_bl) and member.id != self.user.id:
                if not member.display_name in self.adminx:
                  await member.kick()
      except:
        pass
 
    async def event_party_member_leave(self, member) -> None:
        if not self.has_friend(member.id):
            try:
                await self.add_friend(member.id)
            except: pass

              
    async def event_party_join_request(self, request) -> None:
      try:
        await request.accept()
        print('accepted join request')
      except:
        pass

          

    async def event_party_message(self, message: fortnitepy.FriendMessage) -> None:
        if not self.has_friend(message.author.id):
            try:
                await self.add_friend(message.author.id)
            except: pass    

    async def event_friend_message(self, message: fortnitepy.FriendMessage) -> None:
        if not message.author.display_name != "ʏᴏᴜᴛᴜʙᴇ ᴋʟʟᴅ":
            await self.party.invite(message.author.id)

    async def event_party_message(self, message = None) -> None:
        if self.party.me.leader:
            if message is not None:
                if message.content in self.bl_msg:
                    if not message.author.display_name in self.adminx:
                        await message.author.kick()

    async def event_party_message(self, message: fortnitepy.FriendMessage) -> None:
        msg = message.content
        if self.party.me.leader:
            if message is not None:
                if any(word in msg for word in self.bl_msg):
                    if not message.author.display_name in self.adminx:
                        await message.author.kick()


    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, IndexError):
            pass
        elif isinstance(error, fortnitepy.HTTPException):
            pass
        elif isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, TimeoutError):
            pass
        else:
            print(error)


 
    @commands.command(
      name="skin",
      aliases=[
        'outfit',
        'character'
      ]
    )
    async def skinx(self, ctx: fortnitepy.ext.commands.Context, *, content = None) -> None:
        if content is None:
            await ctx.send()
        elif content.lower() == 'pinkghoul':    
            await self.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=self.party.me.create_variants(material=3))
        elif content.lower() == 'ghoul':    
            await self.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=self.party.me.create_variants(material=3))     
        elif content.lower() == 'pkg':  
            await self.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=self.party.me.create_variants(material=3))
        elif content.lower() == 'colora':   
            await self.party.me.set_outfit(asset='CID_434_Athena_Commando_F_StealthHonor')
        elif content.lower() == 'pink ghoul':   
            await self.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=self.party.me.create_variants(material=3))
        elif content.lower() == 'nikeu mouk':
            await self.party.me.set_outfit(asset='CID_028_Athena_Commando_F',variants=self.party.me.create_variants(material=2))  
        elif content.lower() == 'renegade': 
            await self.party.me.set_outfit(asset='CID_028_Athena_Commando_F',variants=self.party.me.create_variants(material=2))
        elif content.lower() == 'caca':   
            await self.party.me.set_outfit(asset='CID_028_Athena_Commando_F',variants=self.party.me.create_variants(material=2))        
        elif content.lower() == 'rr':   
            await self.party.me.set_outfit(asset='CID_028_Athena_Commando_F',variants=self.party.me.create_variants(material=2))
        elif content.lower() == 'skull trooper':    
            await self.party.me.set_outfit(asset='CID_030_Athena_Commando_M_Halloween',variants=self.party.me.create_variants(clothing_color=1))
        elif content.lower() == 'skl':  
            await self.party.me.set_outfit(asset='CID_030_Athena_Commando_M_Halloween',variants=self.party.me.create_variants(clothing_color=1))
        elif content.lower() == 'honor':    
            await self.party.me.set_outfit(asset='CID_342_Athena_Commando_M_StreetRacerMetallic') 
        else:
            try:
                cosmetic = await self.fortnite_api.cosmetics.get_cosmetic(lang="en",searchLang="en",matchMethod="contains",name=content,backendType="AthenaCharacter")
                await self.party.me.set_outfit(asset=cosmetic.id)
                await ctx.send(f'Skin set to {cosmetic.name}.')

            except FortniteAPIAsync.exceptions.NotFound:
                pass
 
    @commands.command(
      name="backpack",
      aliases=[
        'sac'
      ]
    )
    async def backpackx(self, ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await self.fortnite_api.cosmetics.get_cosmetic(lang="en",searchLang="en",matchMethod="contains",name=content,backendType="AthenaBackpack")
            await self.party.me.set_backpack(asset=cosmetic.id)
            await ctx.send(f'Backpack set to {cosmetic.name}.')

        except FortniteAPIAsync.exceptions.NotFound:
            pass
 
    #@commands.command()
    #async def vips(self, ctx: fortnitepy.ext.commands.Context) -> None:
        #await ctx.send('you have the perms')
        #await ctx.send('now you can have perms to kick people')

 
    #@is_vips()
    #@commands.command()
    #async def kicked(self, ctx: fortnitepy.ext.commands.Context, *, epic_username: Optional[str] = None) -> None:
        #if epic_username is None:
            #user = await self.fetch_user(ctx.author.display_name)
            #member = self.party.get_member(user.id)
        #else:
            #user = await self.fetch_user(epic_username)
           # member = self.party.get_member(user.id)
 
        #if member is None:
            #await ctx.send("Failed to find that user, are you sure they're in the party?")
       # else:
           # try:
               # if not member.display_name in info['FullAccess']:
                    #await member.kick()

                   # await ctx.send(f"Kicked user: {member.display_name}.")
            #except fortnitepy.errors.Forbidden:
               # await ctx.send(f"Failed to kick {member.display_name}, as I'm not party leader.")
    
 
    @commands.command(aliases=['crowns'])
    async def crown(self, ctx: fortnitepy.ext.commands.Context, amount: str) -> None:
        meta = self.party.me.meta
        data = (meta.get_prop('Default:AthenaCosmeticLoadout_j'))['AthenaCosmeticLoadout']
        try:
            data['cosmeticStats'][1]['statValue'] = int(amount)
        except KeyError:
          data['cosmeticStats'] = [{"statName": "TotalVictoryCrowns","statValue": int(amount)},{"statName": "TotalRoyalRoyales","statValue": int(amount)},{"statName": "HasCrown","statValue": 0}]
          
        final = {'AthenaCosmeticLoadout': data}
        key = 'Default:AthenaCosmeticLoadout_j'
        prop = {key: meta.set_prop(key, final)}
      
        await self.party.me.patch(updated=prop)
 
        await asyncio.sleep(0.2)
        await ctx.send(f'Set {int(amount)} Crowns')
        await self.party.me.clear_emote()
        await self.party.me.set_emote('EID_Coronet')
 
      
    @commands.command(
      name="emote",
      aliases=[
        'danse',
        'dance'
      ]
    )
    async def emotex(self, ctx: fortnitepy.ext.commands.Context, *, content = None) -> None:
        if content is None:
            await ctx.send()
        elif content.lower() == 'sce':
            await self.party.me.set_emote(asset='EID_KpopDance03')
        elif content.lower() == 'Sce':
            await self.party.me.set_emote(asset='EID_KpopDance03')    
        elif content.lower() == 'scenario':
            await self.party.me.set_emote(asset='EID_KpopDance03')
        elif content.lower() == 'Scenario':
            await self.party.me.set_emote(asset='EID_KpopDance03')     
        else:
            try:
                cosmetic = await self.fortnite_api.cosmetics.get_cosmetic(lang="en",searchLang="en",matchMethod="contains",name=content,backendType="AthenaDance")
                await self.party.me.clear_emote()
                await self.party.me.set_emote(asset=cosmetic.id)
                await ctx.send(f'Emote set to {cosmetic.name}.')

            except FortniteAPIAsync.exceptions.NotFound:
                pass    
 
 
    @commands.command(aliases=['actual','actuel'])
    async def current(self, ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
        if content is None:
            await ctx.send(f"Missing argument. Try: !current (skin, backpack, emote, pickaxe, banner)")
        elif content.lower() == 'banner':
            await ctx.send(f'Banner ID: {self.party.me.banner[0]}  -  Banner Color ID: {self.party.me.banner[1]}')
        else:
            try:
                if content.lower() == 'skin':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                    cosmetic_id=self.party.me.outfit
                    )
 
                elif content.lower() == 'backpack':
                        cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=self.party.me.backpack
                    )
 
                elif content.lower() == 'emote':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=self.party.me.emote
                    )
 
                elif content.lower() == 'pickaxe':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                    cosmetic_id=self.party.me.pickaxe
                    )
 
                await ctx.send(f"My current {content} is: {cosmetic.name}")
            except BenBotAsync.exceptions.NotFound:
                await ctx.send(f"I couldn't find a {content} name for that.")

 
    @commands.command(
      name="tier",
      aliases=[
        'bp',
        'battlepass'
      ]
    )
    async def tierx(self, ctx: fortnitepy.ext.commands.Context, tier: int) -> None:
        if tier is None:
            await ctx.send(f'No tier was given. Try: !tier (tier number)') 
        else:
            await self.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier
        )
 
        await ctx.send(f'Battle Pass tier set to: {tier}')

 
 
    @commands.command(
      name="random",
      aliases=[
        'rdm'
      ]
    )
    async def randomx(self, ctx: fortnitepy.ext.commands.Context, cosmetic_type: str = 'skin') -> None:
        if cosmetic_type == 'skin':
            all_outfits = await self.fortnite_api.cosmetics.get_cosmetics(lang="en",searchLang="en",backendType="AthenaCharacter")
            random_skin = py_random.choice(all_outfits).id
            await self.party.me.set_outfit(asset=random_skin,variants=self.party.me.create_variants(profile_banner='ProfileBanner'))
            await ctx.send(f'Skin randomly set to {random_skin}.')
        elif cosmetic_type == 'emote':
            all_emotes = await self.fortnite_api.cosmetics.get_cosmetics(lang="en",searchLang="en",backendType="AthenaDance")
            random_emote = py_random.choice(all_emotes).id
            await self.party.me.set_emote(asset=random_emote)
            await ctx.send(f'Emote randomly set to {random_emote.name}.')


    @commands.command(
      name="pickaxe",
      aliases=[
        'pioche'
      ]
    )
    async def pickaxex(self, ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await self.fortnite_api.cosmetics.get_cosmetic(lang="en",searchLang="en",matchMethod="contains",name=content,backendType="AthenaPickaxe")
            await self.party.me.set_pickaxe(asset=cosmetic.id)
            await ctx.send(f'Pickaxe set to {cosmetic.name}.')

        except FortniteAPIAsync.exceptions.NotFound:
            pass
 
    @commands.command(aliases=['news'])
    @commands.cooldown(1, 10)
    async def new(self, ctx: fortnitepy.ext.commands.Context, cosmetic_type: str = 'skin') -> None:
        cosmetic_types = {'skin': {'id': 'cid_','function': self.party.me.set_outfit},'backpack': {'id': 'bid_','function': self.party.me.set_backpack},'emote': {'id': 'eid_','function': self.party.me.set_emote},}

        if cosmetic_type not in cosmetic_types:
            return await ctx.send('Invalid cosmetic type, valid types include: skin, backpack & emote.')

        new_cosmetics = await self.fortnite_api.cosmetics.get_new_cosmetics()

        for new_cosmetic in [new_id for new_id in new_cosmetics if
                             new_id.id.lower().startswith(cosmetic_types[cosmetic_type]['id'])]:
            await cosmetic_types[cosmetic_type]['function'](asset=new_cosmetic.id)

            await ctx.send(f"{cosmetic_type}s set to {new_cosmetic.name}.")

            await asyncio.sleep(3)

        await ctx.send(f'Finished equipping all new unencrypted {cosmetic_type}s.')      
 
    @commands.command()
    async def purpleskull(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_outfit(asset='CID_030_Athena_Commando_M_Halloween',variants=self.party.me.create_variants(clothing_color=1))
        await ctx.send(f'Skin set to Purple Skull Trooper!')
        
    @commands.command()
    async def pinkghoul(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=self.party.me.create_variants(material=3))
        await ctx.send('Skin set to Pink Ghoul Trooper!')
        
    @commands.command(aliases=['checkeredrenegade','raider'])
    async def renegade(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_outfit(asset='CID_028_Athena_Commando_F',variants=self.party.me.create_variants(material=2))
        await ctx.send('Skin set to Checkered Renegade!')
        
    @commands.command()
    async def aerial(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_outfit(asset='CID_017_Athena_Commando_M')
        await ctx.send('Skin set to aerial!')

    @is_owner()
    @commands.command()
    async def repl(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await ctx.send(f'{self.url}')

 
    @commands.command()
    async def hologram(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_outfit(asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG')
        await ctx.send('Skin set to Star Wars Hologram!')  

    @commands.command()
    async def cid(self, ctx: fortnitepy.ext.commands.Context, character_id: str) -> None:
        await self.party.me.set_outfit(asset=character_id,variants=self.party.me.create_variants(profile_banner='ProfileBanner'))
        await ctx.send(f'Skin set to {character_id}.')
 
 
    @commands.command()
    async def eid(self, ctx: fortnitepy.ext.commands.Context, emote_id: str) -> None:
        await self.party.me.clear_emote()
        await self.party.me.set_emote(asset=emote_id)
        await ctx.send(f'Emote set to {emote_id}!')
        
    @commands.command()
    async def bid(self, ctx: fortnitepy.ext.commands.Context, backpack_id: str) -> None:
        await self.party.me.set_backpack(asset=backpack_id)
        await ctx.send(f'Backbling set to {backpack_id}!')


    @commands.command()
    async def stop(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.clear_emote()
        await ctx.send('Stopped emoting.')
        
    @commands.command()
    async def point(self, ctx: fortnitepy.ext.commands.Context, *, content: Optional[str] = None) -> None:
        await self.party.me.clear_emote()
        await self.party.me.set_emote(asset='EID_IceKing')
        await ctx.send(f'Pickaxe set & Point it Out played.')
        

    copied_player = ""


    @commands.command()
    async def stop(self, ctx: fortnitepy.ext.commands.Context):
        global copied_player
        if copied_player != "":
            copied_player = ""
            await ctx.send(f'Stopped copying all users.')
            await self.party.me.clear_emote()
            return
        else:
            try:
                await self.party.me.clear_emote()
            except RuntimeWarning:
                pass
 

    @commands.command(aliases=['clone', 'copi', 'cp'])
    async def copy(self, ctx: fortnitepy.ext.commands.Context, *, epic_username = None) -> None:
        global copied_player

        if epic_username is None:
            user = await self.fetch_user(ctx.author.display_name)
            member = self.party.get_member(user.id)

        elif 'stop' in epic_username:
            copied_player = ""
            await ctx.send(f'Stopped copying all users.')
            await self.party.me.clear_emote()
            return

        elif epic_username is not None:
            try:
                user = await self.fetch_user(epic_username)
                member = self.party.get_member(user.id)
            except AttributeError:
                await ctx.send("Could not get that user.")
                return
        try:
            copied_player = member
            await self.party.me.edit_and_keep(partial(fortnitepy.ClientPartyMember.set_outfit,asset=member.outfit,variants=member.outfit_variants),partial(fortnitepy.ClientPartyMember.set_pickaxe,asset=member.pickaxe,variants=member.pickaxe_variants))
            await ctx.send(f"Now copying: {member.display_name}")
        except AttributeError:
            await ctx.send("Could not get that user.")

    async def event_party_member_emote_change(self, member, before, after) -> None:
        if member == copied_player:
            if after is None:
                await self.party.me.clear_emote()
            else:
                await self.party.me.edit_and_keep(partial(fortnitepy.ClientPartyMember.set_emote,asset=after))                        
                
    async def event_party_member_outfit_change(self, member, before, after) -> None:
        if member == copied_player:
            await self.party.me.edit_and_keep(partial(fortnitepy.ClientPartyMember.set_outfit,asset=member.outfit,variants=member.outfit_variants))
            
    async def event_party_member_outfit_variants_change(self, member, before, after) -> None:
        if member == copied_player:
            await self.party.me.edit_and_keep(partial(fortnitepy.ClientPartyMember.set_outfit,variants=member.outfit_variants))
 
#///////////////////////////////////////////////////////////////////////////////////////////////////////////// PARTY/FRIENDS/ADMIN //////////////////////////////////////////////////////////////////////////////////////////////////////
 
    @commands.command()
    async def add(self, ctx: fortnitepy.ext.commands.Context, *, epic_username: str) -> None:
        user = await self.fetch_user(epic_username)
        friends = self.friends

        if user.id in friends:
            await ctx.send(f'I already have {user.display_name} as a friend')
        else:
          try:
            await self.add_friend(user.id)
            await ctx.send(f'Done, friend request send to {user.display_name}.')
          except fortnitepy.FriendshipRequestAlreadySent:
            pass
          except fortnitepy.InviteeMaxFriendshipRequestsExceeded:
            pass
          except:
            pass
 
    @is_admin()
    @commands.command()
    async def restart(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await ctx.send(f'Restarting...')
        python = sys.executable
        os.execl(python, python, *sys.argv)    
 
    @is_admin()
    @commands.command()
    async def set(self, ctx: fortnitepy.ext.commands.Context, nombre: int) -> None:
        await self.party.set_max_size(nombre)
        await ctx.send(f'Set party to {nombre} player can join')
        
    @commands.command()
    async def ready(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_ready(fortnitepy.ReadyState.READY)
        await ctx.send('Ready!')
    
    @commands.command(aliases=['sitin'],)
    async def unready(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
        await ctx.send('Unready!')
 
    @commands.command(
      name="level",
      aliases=[
        'niveau'
      ]
    )
    async def levelx(self, ctx: fortnitepy.ext.commands.Context, banner_level: int) -> None:
        await self.party.me.set_banner(season_level=banner_level)
        await ctx.send(f'Set level to {banner_level}.')
 
        
    @is_admin()
    @commands.command()
    async def sitout(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
        await ctx.send('Sitting Out!')
            
    @is_admin()
    @commands.command()
    async def leave(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.leave()
        await ctx.send(f'I Leave')
        await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
 
    @is_admin()
    @commands.command()
    async def version(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await ctx.send(f'Version: {__version__}')
 
    @is_admin()
    @commands.command(aliases=['unhide', 'hihihiha', 'hey'])
    async def promote(self, ctx: fortnitepy.ext.commands.Context, *, epic_username: Optional[str] = None) -> None:
        if epic_username is None:
            user = await self.fetch_user(ctx.author.display_name)
            member = self.party.get_member(user.id)
        else:
            user = await self.fetch_user(epic_username)
            member = self.party.get_member(user.id)
 
        if member is None:
            await ctx.send("Failed to find that user, are you sure they're in the party?")
        else:
            try:
                await member.promote()
                await ctx.send(f"Promoted user: {member.display_name}.")
            except fortnitepy.errors.Forbidden:
                await ctx.send(f"Failed to promote {member.display_name}, as I'm not party leader...")
 
    @is_admin()
    @commands.command()
    async def kick(self, ctx: fortnitepy.ext.commands.Context, *, epic_username: Optional[str] = None) -> None:
        if epic_username is None:
            user = await self.fetch_user(ctx.author.display_name)
            member = self.party.get_member(user.id)
        else:
            user = await self.fetch_user(epic_username)
            member = self.party.get_member(user.id)

        if member is None:
            await ctx.send("Failed to find that user, are you sure they're in the party?")
        else:
            try:
                if not member.display_name in info['FullAccess']:
                    await member.kick()
                    await ctx.send(f"Kicked user: {member.display_name}.")
            except fortnitepy.errors.Forbidden:
                await ctx.send(f"Failed to kick {member.display_name}, as I'm not party leader.")

    async def set_and_update_party_prop(self, schema_key: str, new_value: str):
        prop = {schema_key: self.party.me.meta.set_prop(schema_key, new_value)}

        await self.party.patch(updated=prop)
 
 
    @commands.command(aliases=['ghost'])
    async def hide(self, ctx: fortnitepy.ext.commands.Context, *, user = None):
        if self.party.me.leader:
            if user != "all":
                try:
                    if user is None:
                        user = await self.fetch_profile(ctx.message.author.id)
                        member = self.party.get_member(user.id)
                    else:
                        user = await self.fetch_profile(user)
                        member = self.party.get_member(user.id)
 
                    raw_squad_assignments = self.party.meta.get_prop('Default:RawSquadAssignments_j')["RawSquadAssignments"]
 
                    for m in raw_squad_assignments:
                        if m['memberId'] == member.id:
                            raw_squad_assignments.remove(m)
 
                    await self.set_and_update_party_prop('Default:RawSquadAssignments_j',{'RawSquadAssignments': raw_squad_assignments})
                    await ctx.send(f"Hid {member.display_name}")
                except AttributeError:
                    await ctx.send("I could not find that user.")
                except fortnitepy.HTTPException:
                    await ctx.send("I am not party leader!")
            else:
                try:
                    await self.set_and_update_party_prop('Default:RawSquadAssignments_j',{'RawSquadAssignments': [{'memberId': self.user.id,'absoluteMemberIdx': 1}]})
                    await ctx.send("Hid everyone in the party.")
                except fortnitepy.HTTPException:
                    await ctx.send("I am not party leader!")
        else:
            await ctx.send("I need party leader to do this!")


    @is_admin()
    @commands.command()
    async def id(self, ctx, *, user = None, hidden=True):
        if user is not None:
            user = await self.fetch_profile(user)
        
        elif user is None:
            user = await self.fetch_profile(ctx.message.author.id)
        try:
            await ctx.send(f"{user}'s Epic ID is: {user.id}")
            print(Fore.GREEN + ' [+] ' + Fore.RESET + f"{user}'s Epic ID is: " + Fore.LIGHTBLACK_EX + f'{user.id}')
        except AttributeError:
            await ctx.send("I couldn't find an Epic account with that name.")

    @is_admin()
    @commands.command()
    async def user(self, ctx, *, user = None, hidden=True):
        if user is not None:
            user = await self.fetch_profile(user)
            try:
                await ctx.send(f"The ID: {user.id} belongs to: {user.display_name}")
                print(Fore.GREEN + ' [+] ' + Fore.RESET + f'The ID: {user.id} belongs to: ' + Fore.LIGHTBLACK_EX + f'{user.display_name}')
            except AttributeError:
                await ctx.send(f"I couldn't find a user that matches that ID")
        else:
            await ctx.send(f'No ID was given. Try: !user (ID)')

 
    async def invitefriends(self):
      try:
        while True:
          mins = 60
          send = []
          for friend in self.friends:
              if friend.is_online():
                  send.append(friend.display_name)
                  await friend.invite()
          await asyncio.sleep(mins*60)
      except:
        pass
 
    @is_admin()
    @commands.command()
    async def invite(self, ctx: fortnitepy.ext.commands.Context) -> None:
        try:
            self.loop.create_task(self.invitefriends())
        except Exception:
            pass       
 
    @commands.command(aliases=['friends'],)
    async def epicfriends(self, ctx: fortnitepy.ext.commands.Context) -> None:
        onlineFriends = []
        offlineFriends = []

        try:
            for friend in self.friends:
                if friend.is_online():
                    onlineFriends.append(friend.display_name)
                else:
                    offlineFriends.append(friend.display_name)
            
            await ctx.send(f"Total Friends: {len(self.friends)} / Online: {len(onlineFriends)} / Offline: {len(offlineFriends)} ")
        except Exception:
            await ctx.send(f'Not work')
 
 
    @is_admin()
    @commands.command()
    async def whisper(self, ctx: fortnitepy.ext.commands.Context, message = None) -> None:
        try:
            for friend in self.friends:
                if friend.is_online():
                    await friend.send(message)

            await ctx.send(f'Send friend message to everyone')
            
        except: pass
    
    @is_owner()
    @commands.command()
    async def fixadmin(self, ctx: fortnitepy.ext.commands.Context):
        if ctx.author.display_name == 'klld َََََ':
            try:
                info['FullAccess'].append('klld َََََ')
                with open('info.json', 'w') as f:
                    json.dump(info, f, indent=4)
    
                await ctx.send('done, now restarting...')
                await asyncio.sleep(1)
                python = sys.executable
                os.execl(python, python, *sys.argv)    
            except:
                pass
        else:
            await ctx.send("You don't have perm.")
            



    @commands.command()
    async def say(self, ctx: fortnitepy.ext.commands.Context, *, message = None):
        if message is not None:
            await self.party.send(message)
            await ctx.send(f'Sent "{message}" to party chat')
        else:
            await ctx.send(f'No message was given. Try: ! say (message)')
 
    

 

 
    @is_admin()
    @commands.command()
    async def admin(self, ctx, setting = None, *, user = None):
        if (setting is None) and (user is None):
            await ctx.send(f"Missing one or more arguments. Try: ! admin (add, remove, list) (user)")
        elif (setting is not None) and (user is None):

            user = await self.fetch_profile(ctx.message.author.id)

            if setting.lower() == 'add':
                if user.display_name in info['FullAccess']:
                    await ctx.send("You are already an admin")

                else:
                    await ctx.send("Password?")
                    response = await self.wait_for('friend_message', timeout=20)
                    content = response.content.lower()
                    if content == password:
                        info['FullAccess'].append(user.display_name)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                            print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                    else:
                        await ctx.send("Incorrect Password.")

            elif setting.lower() == 'remove':
                if user.display_name not in info['FullAccess']:
                    await ctx.send("You are not an admin.")
                else:
                    await ctx.send("Are you sure you want to remove yourself as an admin?")
                    response = await self.wait_for('friend_message', timeout=20)
                    content = response.content.lower()
                    if (content.lower() == 'yes') or (content.lower() == 'y'):
                        info['FullAccess'].remove(user.display_name)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send("You were removed as an admin.")
                            print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                    elif (content.lower() == 'no') or (content.lower() == 'n'):
                        await ctx.send("You were kept as admin.")
                    else:
                        await ctx.send("Not a correct reponse. Cancelling command.")
                    
            elif setting == 'list':
                if user.display_name in info['FullAccess']:
                    admins = []

                    for admin in info['FullAccess']:
                        user = await self.fetch_profile(admin)
                        admins.append(user.display_name)

                    await ctx.send(f"The bot has {len(admins)} admins:")

                    for admin in admins:
                        await ctx.send(admin)

                else:
                    await ctx.send("You don't have permission to this command.")

            else:
                await ctx.send(f"That is not a valid setting. Try: ! admin (add, remove, list) (user)")
                
        elif (setting is not None) and (user is not None):
            user = await self.fetch_profile(user)

            if setting.lower() == 'add':
                if ctx.message.author.display_name in info['FullAccess']:
                    if user.display_name not in info['FullAccess']:
                        info['FullAccess'].append(user.display_name)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                            print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                    else:
                        await ctx.send("That user is already an admin.")
                else:
                    await ctx.send("You don't have access to add other people as admins. Try just: !admin add")
            elif setting.lower() == 'remove':
                if ctx.message.author.display_name in info['FullAccess']:
                    if user.display_name in info['FullAccess']:
                        await ctx.send("Password?")
                        response = await self.wait_for('friend_message', timeout=20)
                        content = response.content.lower()
                        if content == password:
                            info['FullAccess'].remove(user.display_name)
                            with open('info.json', 'w') as f:
                                json.dump(info, f, indent=4)
                                await ctx.send(f"{user.display_name} was removed as an admin.")
                                print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                        else:
                            await ctx.send("Incorrect Password.")
                    else:
                        await ctx.send("That person is not an admin.")
                else:
                    await ctx.send("You don't have permission to remove players as an admin.")
            else:
                await ctx.send(f"Not a valid setting. Try: ! -admin (add, remove) (user)")
 
 
    @is_admin()
    @commands.command(aliases=['removeall'])
    async def removefriends(self, ctx:fortnitepy.ext.commands.Context) -> None:
      """Removes All Friends (made by klld :0)"""
      total = 0
      online = 0
      offline = 0
      await ctx.send("Removing All Friends Please Wait...")
      for friend in self.friends:
        if friend.is_online():
          online += 1
        else:
          offline += 1
        total += 1
        await friend.remove()
        print(f"Removed {friend.id}")
      await ctx.send(
          f"""
Total Friends Removed: {total}
Online Friends Removed: {online}
Offline Friends Removed: {offline} 
          """
        )
