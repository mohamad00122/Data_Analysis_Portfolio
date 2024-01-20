const apiKey = '1d8326ef13fa951f5112adb38edd26a3'; // Replace with your OpenWeatherMap API key
const searchBtn = document.getElementById('search-btn');
const searchInput = document.getElementById('search-input');

searchBtn.addEventListener('click', () => {
    const cityName = searchInput.value;
    fetchWeatherData(cityName);
});

function fetchWeatherData(city) {
    fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=imperial`) // Changed to imperial for Fahrenheit
    .then(response => response.json())
    .then(data => displayWeatherData(data))
    .catch(error => console.error('Error:', error));
}

function displayWeatherData(data) {
    const weatherInfo = document.querySelector('.weather-info');

    if (data.cod !== 200) {
        weatherInfo.style.display = 'none';
        alert(`Error: ${data.message}`);
        return;
    }

    const iconCode = data.weather[0].icon;
    const iconUrl = `http://openweathermap.org/img/w/${iconCode}.png`;
    document.getElementById('weather-icon').setAttribute('src', iconUrl);

    document.getElementById('city-name').textContent = data.name;
    document.getElementById('weather-description').textContent = data.weather[0].description;
    document.getElementById('temperature').textContent = `Temperature: ${data.main.temp}°F`; // Changed to °F for Fahrenheit
    document.getElementById('humidity').textContent = `Humidity: ${data.main.humidity}%`;
    document.getElementById('wind-speed').textContent = `Wind Speed: ${data.wind.speed} m/s`;
    document.getElementById('city-name').textContent = `${data.name}, ${data.sys.country}`;

    weatherInfo.style.display = 'block';
}

window.onload = () => {
    fetchWeatherData('London'); // Default city on load
};
