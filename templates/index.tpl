% rebase('base.tpl', title=title)
<h2>Brief</h2>
<div class="row">
    % for period in weather_data['properties']['periods']:
    <span class="weather-day col-md-2">
        <div class="inner">
            <div><img src="{{ period['icon'] }}" /></div>
            <div><strong>{{ period['name'] }}</strong></div>
            <div>{{ period['temperature'] }}&#8457;</div>
            <div>{{ period['shortForecast'] }}</div>
        </div>
    </span>
    % end
</div>

<div class="row">
    <img src="{{ menu_img_url }}" />
</div>

<div class="row">
    <ul>
        % for event in events:
            <li>
                {{ event['summary'] }}: {{ event['start'].get('dateTime', event['start'].get('date')) }}
            </li>
        % end
    </ul>
</div>

<style>
.weather-day {
    background-color: #eee;
    margin: 5px;
    height: 200px;
}

.weather-day .inner img {
    display: block;
    margin-left: auto;
    margin-right: auto;
}
</style>
