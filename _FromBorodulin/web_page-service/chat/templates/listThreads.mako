<%inherit file="/base.mako"/>

<%block name="title">
    Discussions list
</%block>

<div class="plain-text">Conference: ${section_title}</div>

<table border="1" frame="void" rules="all">
% for thread in threads:
    <% ident, pr_title, speaker = thread %>
    <tr><td>
        <a href="${base_url}/?identifier=${ident}">
            ${pr_title} 
            % if speaker and pr_title != "Organization":
                 (${speaker})
            % endif
        </a>
    </td></tr>
% endfor
</table>