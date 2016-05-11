<%inherit file="/base.mako"/>

<%block name="title">
    Archive
</%block>

<table border="1" frame="void" rules="all">
% for category in categories:
    <% cat_id, section_uuid, section_title = category %>
    <tr><td>
    <a href="${base_url}/listThreads?section_uuid=${section_uuid}">${section_title}</a>
    </td></tr>
% endfor
</table>
