## -*- coding: utf-8 -*-
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>
            <%block name="title">
                Chat Service
            </%block>
        </title>
        <link href='http://fonts.googleapis.com/css?family=Roboto:300&subset=cyrillic,latin' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" href="./static/css/disqus.css?v4" type="text/css" />
    </head>
    
    <body ontouchstart="">
        <div class="header">
            <%block name="header">
                <div class="header-text">
                    <a class="nav" href="${base_url}/">Active discussion</a>
                    
                    <a class="nav" href="${base_url}/listCurrentThreads">List of discussions</a>
                    
                    <a class="nav" href="${base_url}/listCategories">Archive</a></div>
                </div>
            </%block>
        </div>

    <div class = "body">
        ${self.body()}
    </div>

        <div class="footer">
            <%block name="footer">
            <div class="footer-text">
                PetrSU SmartRoom Chat Service. 2015
            </div>
            </%block>
        </div>
    </body>
</html>