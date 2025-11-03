# 🎵 Playlist Manager

A Python-based playlist management system with MySQL & JSON support using POM (Python Object Model) architecture.

## 📋 Project Structure

```
playlist-manager/
├── pom.py                    # Python Object Model Configuration
├── config.py                 # Centralized Configuration
├── main.py                   # Main Application
├── database.py               # MySQL Database Handler
├── requirements.txt          # Python Dependencies
├── playlists.json            # Default JSON Storage
├── .gitignore               # Git Ignore Rules
└── README.md                # Documentation
```

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/diptanshuverma012/playlist-manager.git
cd playlist-manager
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure MySQL (Optional)
Edit `config.py`:
```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'playlist_db'
}
```

### 4. Run Application
```bash
python main.py
```

## ✨ Features

✅ User Authentication  
✅ Create/Manage Playlists by Mood  
✅ Add/Delete/Rename Songs  
✅ Search Functionality  
✅ Favorite Mood Support  
✅ Export to TXT/CSV/JSON  
✅ MySQL & JSON Storage  
✅ Statistics Dashboard  

## 🔧 Configuration (config.py)

| Setting | Default | Description |
|---------|---------|-------------|
| USE_MYSQL | True | Use MySQL (False = JSON) |
| MYSQL_CONFIG | localhost | Database credentials |
| DEFAULT_PLAYLISTS | 4 moods | Initial playlists |

## 📦 POM Model Info

```python
python pom.py
```

## 🧪 Testing

```bash
pytest tests/
```

## 📝 License

MIT - 2025