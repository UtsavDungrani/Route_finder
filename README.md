# Sustainable Travel Route Finder 🌱

A Flask web application that helps users find the most eco-friendly travel routes between any two locations, with detailed carbon emission calculations and environmental impact analysis.

## 🌟 Features

- **Multi-modal Route Planning**: Find routes using walking, cycling, public transit, and driving
- **Carbon Emission Calculations**: Real-time CO₂ emission calculations for each route
- **Interactive Maps**: Visual route display using Leaflet.js and OpenStreetMap
- **Environmental Impact Analysis**: Compare routes and see emission savings
- **Responsive Design**: Modern, mobile-friendly interface
- **API Endpoints**: RESTful API for integration with other applications
- **Error Handling**: Comprehensive error handling and user feedback

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd new_treavel
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirments.txt
   ```

4. **Set up environment variables**

   ```bash
   # Create a .env file
   echo "ORS_API_KEY=your_openrouteservice_api_key" > .env
   echo "SECRET_KEY=your_secret_key" >> .env
   echo "FLASK_ENV=development" >> .env
   ```

5. **Run the application**

   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔧 Configuration

### Environment Variables

| Variable      | Description              | Default            |
| ------------- | ------------------------ | ------------------ |
| `ORS_API_KEY` | OpenRouteService API key | Demo key (limited) |
| `SECRET_KEY`  | Flask secret key         | Auto-generated     |
| `FLASK_ENV`   | Flask environment        | development        |
| `PORT`        | Application port         | 5000               |

### API Keys

**OpenRouteService API Key**:

- Get a free API key from [OpenRouteService](https://openrouteservice.org/dev/#/signup)
- The demo key has limited usage, get your own for production

## 📁 Project Structure

```
new_treavel/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── wsgi.py               # WSGI entry point
├── requirnments.txt      # Python dependencies
├── README.md             # This file
├── services/             # Business logic services
│   ├── __init__.py
│   ├── route_service.py  # Route finding service
│   └── emissions_service.py # Emission calculations
├── utils/                # Utility modules
│   ├── __init__.py
│   ├── exceptions.py     # Custom exceptions
│   └── validators.py     # Input validation
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── result.html       # Results page
│   ├── about.html        # About page
│   ├── error.html        # General error page
│   └── errors/           # Error pages
│       ├── 404.html      # Not found page
│       └── 500.html      # Server error page
└── static/               # Static files
    ├── css/
    │   └── custom.css    # Custom styles
    └── js/
        └── app.js        # JavaScript functionality
```

## 🛠️ API Endpoints

### Web Routes

- `GET /` - Home page with route finder form
- `POST /result` - Process route search and display results
- `GET /about` - About page with application information
- `GET /health` - Health check endpoint

### API Routes

- `POST /api/routes` - Get route data as JSON
  ```json
  {
    "origin": "New York, NY",
    "destination": "Boston, MA"
  }
  ```

### Response Format

```json
{
  "success": true,
  "routes": [
    {
      "mode": "transit",
      "distance": 306.5,
      "duration": 240,
      "emission": 20.8,
      "emission_per_km": 0.068,
      "geometry": [[lat, lng], ...]
    }
  ],
  "origin": "New York, NY",
  "destination": "Boston, MA",
  "best_route": {...}
}
```

## 🌍 Environmental Impact

### Emission Factors

| Transport Mode | CO₂ per km | Notes          |
| -------------- | ---------- | -------------- |
| Walking        | 0 kg       | Zero emissions |
| Cycling        | 0 kg       | Zero emissions |
| Public Transit | 0.068 kg   | Per passenger  |
| Driving        | 0.120 kg   | Average car    |

### Environmental Benefits

- **Carbon Footprint Reduction**: Choose routes with lower emissions
- **Air Quality Improvement**: Reduce local air pollution
- **Health Benefits**: Encourage walking and cycling
- **Cost Savings**: Save on fuel and parking costs

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-flask pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=.
```

## 🚀 Deployment

### Development

```bash
python app.py
```

### Production

```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

# Using Docker
docker build -t travel-finder .
docker run -p 5000:5000 travel-finder
```

### Environment Setup

For production deployment:

1. Set `FLASK_ENV=production`
2. Use a strong `SECRET_KEY`
3. Get your own `ORS_API_KEY`
4. Configure a reverse proxy (nginx)
5. Set up SSL certificates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Use meaningful commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenRouteService](https://openrouteservice.org/) for routing API
- [Leaflet.js](https://leafletjs.com/) for interactive maps
- [Bootstrap](https://getbootstrap.com/) for UI components
- [Font Awesome](https://fontawesome.com/) for icons

## 📞 Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check the code comments and this README
- **Community**: Join our discussions for help and ideas

## 🔮 Future Enhancements

- [ ] Real-time traffic integration
- [ ] Electric vehicle routing
- [ ] Multi-stop journey planning
- [ ] Carbon offset recommendations
- [ ] Mobile app development
- [ ] Integration with public transit APIs
- [ ] Weather-aware routing
- [ ] Accessibility route options

---

**Made with ❤️ for a greener future**
