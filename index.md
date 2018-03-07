---
layout: default
pagination:
  enabled: true
---

{% for article in paginator.posts %}
  <article class="{% if forloop.first %}first{% elsif forloop.last %}last{% else %}middle{% endif %}">
		<div class="article-head">
			<small class="date">{{ article.date | date: "%b %d, %Y" }} | {{ article.comments }} | {{ article.lang}} |</small>
			<h2 class="title"><a href="{{ site.url }}{{ article.url }}">{{ article.title }}</a></h2>
		</div>
		<p class="excerpt">{{ article.excerpt }}</p>
    	<div>
				<a href="{{ site.url }}{{ article.url }}"><img class= "post-img" src="{{ article.image }}"></a>
			</div>
		<!-- <a href="{{ site.url }}{{ article.url }}" class="full-post-link js-pjax">Read more</a>	 -->
	</article>
	{% if forloop.last %}
  {% else %}
  <hr class="hr-post">
  {% endif %}
{% endfor %}

<hr>

{% if paginator.total_pages > 1 %}
<ul>
  {% if paginator.previous_page %}
  <li>
    <a href="{{ paginator.previous_page_path | prepend: site.baseurl }}">Newer</a>
  </li>
  {% endif %}
  {% if paginator.next_page %}
  <li>
    <a href="{{ paginator.next_page_path | prepend: site.baseurl }}">Older</a>
  </li>
  {% endif %}
</ul>
{% endif %}