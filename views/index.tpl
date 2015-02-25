<!DOCTYPE html>
<html>
<head>
    <title>Hipster Domain Finder - Obscure domain hacks</title>
    <link rel="stylesheet" href="/static/index.css">
</head>
<body>
    <div class="wrap">
        <header>
            <div class="title">Hipster Domain Finder</div>
            <div class="subtitle">
                Dot-com is so mainstream, find obscure domain hacks with Hipster Domain Finder.
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

        <footer>
            Portland made, <a href="https://domainr.com/">Domainr</a> powered.
        </footer>
    </div>

    <div class="template expansionTemp">
        [purchase options placeholder]
    </div>
</body>
</html>
