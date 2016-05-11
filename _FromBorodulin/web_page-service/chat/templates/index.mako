<%inherit file="/base.mako"/>

%if section_title:
    <span class="plain-text">
        Conference: ${section_title}
    </span><br>
%endif
%if presentation_title == "Organization":
    <span class="plain-text">
        ${presentation_title}
    </span><br>
%else:
    %if presentation_title:
        <span class="plain-text">
            Presentation: ${presentation_title}
        </span><br>
    %endif

    %if speaker:
        <span class="plain-text">
            Speaker: ${speaker}
        </span><br>
    %endif
%endif

<div id="disqus_thread"></div>

<script type="text/javascript"> 
/* * * CONFIGURATION VARIABLES * * */ 
var disqus_shortname = "${forum}"; 
var disqus_identifier = "${identifier}"; 

/* * * DON'T EDIT BELOW THIS LINE * * */ 
(function() { var dsq =  document.createElement('script'); 
dsq.type = 'text/javascript'; 
dsq.async = true;         
dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
(document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);        })(); 
</script> 

<noscript>
    <span class="plain-text">
        Please enable JavaScript to view the 
        <a href="https://disqus.com/?ref_noscript" rel="nofollow">comments powered by Disqus.</a>
    </span>
</noscript> 
