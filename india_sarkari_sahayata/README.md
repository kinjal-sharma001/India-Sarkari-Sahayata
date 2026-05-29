# India Sarkari Sahayata

**A production-ready Django web application to help Indian citizens discover and access government opportunities.**

## Features

- **Government Jobs**: Real-time job listings from Adzuna India API with advanced search and filtering
- **Government Schemes**: Comprehensive database of government welfare schemes with eligibility criteria
- **Scholarships**: Curated scholarship opportunities with deadline tracking and filtering
- **Resume Builder & Analyzer**: AI-powered resume creation and analysis with ATS scoring
- **User Authentication**: Secure account management with profile customization
- **AI Assistant**: Gemini-powered chatbot for government services guidance
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS

## Technology Stack

- **Backend**: Django 6.0.5 + Django REST Framework 3.17.1
- **Database**: SQLite3
- **Frontend**: Tailwind CSS (CDN), Vanilla JavaScript
- **APIs**: 
  - Adzuna Jobs API (Government Jobs)
  - Google Gemini 2.0 Flash (AI Features)
- **Security**: CSRF protection, secure authentication, environment-based configuration

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Windows PowerShell or equivalent terminal
- Virtual environment (venv or virtualenv)

### Installation

1. **Clone/Extract the project**:
   ```powershell
   cd "C:\Users\[YourUsername]\OneDrive\Desktop\India Sarkari Sahayata\India Sarkari Sahayata\india_sarkari_sahayata"
   ```

2. **Create and activate virtual environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (create `.env` file in project root):
   ```env
   DJANGO_SECRET_KEY=your-secure-secret-key-here
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   ADZUNA_APP_ID=your-adzuna-app-id
   ADZUNA_APP_KEY=your-adzuna-app-key
   GEMINI_API_KEY=your-gemini-api-key
   ```

5. **Run migrations**:
   ```powershell
   python manage.py migrate
   ```

6. **Create superuser** (for admin panel):
   ```powershell
   python manage.py createsuperuser
   ```

7. **Run development server**:
   ```powershell
   python manage.py runserver
   ```

   Access at: http://localhost:8000

## Configuration

### API Keys

- **Adzuna Jobs API**: Free tier available at https://developer.adzuna.com/
- **Google Gemini API**: Free tier available at https://ai.google.dev/

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key (production: keep secret) | `django-insecure-dev-only-key` |
| `DJANGO_DEBUG` | Debug mode (set to False in production) | `True` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `ADZUNA_APP_ID` | Adzuna API Application ID | Empty |
| `ADZUNA_APP_KEY` | Adzuna API Application Key | Empty |
| `GEMINI_API_KEY` | Google Gemini API Key | Empty |

## Project Structure

```
india_sarkari_sahayata/
├── accounts/                 # User authentication and profiles
├── api/                      # REST API endpoints (Jobs, Schemes, Scholarships)
├── apps/
│   ├── jobs/                # Job listings and management
│   ├── schemes/             # Government schemes
│   ├── scholarships/        # Scholarship management
│   └── web/                 # Public web pages
├── resume_builder/          # Resume builder and analyzer
├── templates/               # Django templates (HTML)
├── static/                  # CSS, JavaScript, images
├── india_sarkari_sahayata/  # Project settings and configuration
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── db.sqlite3             # SQLite database
```

## API Endpoints

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/jobs/search/?q=clerk` | Search government jobs |
| `GET` | `/api/schemes/` | List all schemes |
| `GET` | `/api/scholarships/` | List all scholarships |
| `POST` | `/api/ai/resume-analyzer/` | Analyze resume with AI |

### Authenticated Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/ai/scheme-recommender/` | Get personalized scheme recommendations |
| `POST` | `/api/ai/chat/` | Chat with AI assistant |

## Static Files

Static files are organized in:
- `static/css/` - Custom stylesheets
- `static/js/` - JavaScript utilities
- `static/icons/` - SVG icons and favicon
- `static/images/` - Images and illustrations

To collect static files:
```powershell
python manage.py collectstatic --noinput
```

## Admin Panel

Access Django admin at: http://localhost:8000/admin/

Default superuser credentials can be set during `createsuperuser` command.

### Manageable Models

- Schemes and Scheme Categories
- Scholarships
- Saved Jobs
- User Profiles
- Resume Templates

## Testing

Run tests with:
```powershell
python manage.py test
```

## Deployment Notes

### Before Production Deployment

1. Set `DJANGO_DEBUG=False` in environment variables
2. Generate a strong `DJANGO_SECRET_KEY`
3. Configure `DJANGO_ALLOWED_HOSTS` appropriately
4. Use PostgreSQL or MySQL instead of SQLite
5. Enable HTTPS and security headers
6. Set up proper error logging
7. Use a production WSGI server (Gunicorn, uWSGI)

### Collect Static Files

```powershell
python manage.py collectstatic --noinput
```

## Performance Optimization

- Database queries are indexed for fast lookups
- Pagination enabled for API endpoints (20 items per page)
- Static files served with proper caching headers
- API response compression available

## Troubleshooting

### ImportError: No module named 'django'
```powershell
pip install -r requirements.txt
```

### ModuleNotFoundError: No module named 'google.genai'
```powershell
pip install google-genai
```

### Database locked error
```powershell
# Delete and recreate database
del db.sqlite3
python manage.py migrate
```

### Static files not loading
```powershell
python manage.py collectstatic --noinput --clear
```

## Code Quality

The project follows:
- PEP 8 Python style guidelines
- Django best practices
- RESTful API conventions
- Semantic HTML structure
- Mobile-first responsive design

## License

This is an educational project developed for demonstration purposes.

## Contact & Support

For issues, questions, or feature requests, please review the code structure and documentation.

---

**Last Updated**: May 29, 2026
**Python Version**: 3.9+
**Django Version**: 6.0.5
**Status**: Production-Ready

