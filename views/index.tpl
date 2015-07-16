<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Hipster Domain Finder - Real word domain hacks</title>
    <link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Open+Sans">
    <link rel="stylesheet" href="/static/index.css">
    <link rel="icon" type="image/png" href="/static/logo.png">
</head>
<body>
    <div class="wrap">
        <header>
            <a href="/" class="title">Hipster Domain Finder</a>
            <div class="subtitle">
                Dot-com is so mainstream, find real word domain hacks with Hipster Domain Finder.
                <a href="https://github.com/bramgg/hipster-domain-finder">Read more on GitHub</a>.
            </div>
        </header>

        <main>
            % for d in domains:
                 <a target="_blank" href="/register/{{d}}" class="domain" data-opened="false">{{d}}</a>
            % end
        </main>

        <nav>
            <a href="/{{page + 1}}" class="side">Next</a>

            % if page > 1:
                <a href="/{{page - 1}}" class="side">Previous</a>
            % end
        </nav>

        <section class="mailing">
            Receive a Hipster Domain in your inbox every Monday.
            <form method='get' action='http://mailing.bram.gg/join/hdf'>
                <input type="email" name="email" placeholder="you@example.com">
                <br>
                <input type="submit" value="Yes please!">
            </form>
        </section>

        <section class="purchased">
            {{len(purchased)}} Hipster Domains purchased this week.
            <br>
            {{', '.join(purchased)}}
        </section>

        <footer>
            Portland made, <a href="https://domainr.com/">Domainr</a> powered.
            <br><br>
            By <a href="http://www.bram.gg/">Bram Hoskin</a>.
        </footer>
    </div>
</body>
</html>
