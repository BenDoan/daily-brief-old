% rebase('base.tpl', title=title)
<h2>Brief - {{ today.strftime("%A %Y-%m-%d") }}</h2>
<div class="row">
    % for period in weather_data['properties']['periods'][:5]:
    <span class="weather-day col-md-2">
        <div class="inner">
            <div><img src="{{ period['icon'] }}" /></div>
            <div><strong>{{ period['name'] }}</strong>: {{ period['temperature'] }}&#8457;</div>
            <div>{{ period['detailedForecast'] }}</div>
        </div>
    </span>
    % end
</div>

<div class="row">
    <img src="{{ menu_img_url }}" class="menu" />
</div>

<div class="row">
    <ul>
        % for event in todays_events:
            <li>
                {{ event['summary'] }}: {{ event['time'].strftime('%A %I:%M %p') }}
            </li>
        % end
    </ul>
</div>

<style>
.weather-day {
    background-color: #eee;
    margin: 5px;
    height: auto;
}

.weather-day .inner img {
    display: block;
    margin-left: auto;
    margin-right: auto;
}

img.menu {
height: 500px;
}
</style>
