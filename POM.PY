"""
POM (Page Object Model) - Python version for Playlist Manager
Organizes project structure and dependencies
"""

class POMConfig:
    """Project Object Model Configuration"""
    
    PROJECT = {
        "groupId": "com.playlist",
        "artifactId": "playlist-manager",
        "version": "1.0.0",
        "name": "Playlist Manager",
        "description": "Python-based playlist management with MySQL & JSON support",
        "packaging": "python",
        "author": "diptanshuverma012",
        "created": "2025-11-03 08:14:20"
    }
    
    DEPENDENCIES = {
        "runtime": [
            {"name": "mysql-connector-python", "version": "8.0.33"},
            {"name": "json", "version": "builtin"},
            {"name": "csv", "version": "builtin"},
            {"name": "os", "version": "builtin"},
            {"name": "random", "version": "builtin"},
        ],
        "testing": [
            {"name": "pytest", "version": "7.4.0"},
            {"name": "unittest", "version": "builtin"},
        ],
        "development": [
            {"name": "black", "version": "23.0.0"},
            {"name": "pylint", "version": "2.17.0"},
        ]
    }
    
    SOURCE_STRUCTURE = {
        "src": {
            "main": {
                "python": [
                    "main.py",
                    "database.py",
                ]
            },
            "resources": [
                "playlists.json",
                "config.py"
            ]
        }
    }
    
    BUILD_CONFIG = {
        "python_version": "3.8+",
        "entry_point": "main.py",
        "output_dir": "dist/",
        "test_runner": "pytest"
    }
    
    @classmethod
    def get_info(cls):
        """Print POM information"""
        return f"""
🎵 Playlist Manager - POM (Python Object Model)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project: {cls.PROJECT['name']} v{cls.PROJECT['version']}
Author: {cls.PROJECT['author']}
Created: {cls.PROJECT['created']}
Python Version: {cls.BUILD_CONFIG['python_version']}
Entry Point: {cls.BUILD_CONFIG['entry_point']}
Runtime Dependencies: {len(cls.DEPENDENCIES['runtime'])}
"""

    @classmethod
    def validate_environment(cls):
        """
        Validate the environment for running the application.
        
        Checks:
        - Python version (should be 3.7+)
        - Required dependencies are installed
        
        Returns:
            dict: Validation results with status and messages
        """
        import sys
        import importlib.util
        
        results = {
            'valid': True,
            'python_version': {
                'valid': False,
                'current': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                'required': '3.7+',
                'message': ''
            },
            'dependencies': {
                'valid': True,
                'missing': [],
                'installed': [],
                'message': ''
            }
        }
        
        # Check Python version
        if sys.version_info >= (3, 7):
            results['python_version']['valid'] = True
            results['python_version']['message'] = f"✅ Python {results['python_version']['current']} is compatible"
        else:
            results['python_version']['valid'] = False
            results['python_version']['message'] = f"❌ Python {results['python_version']['current']} is below minimum required version 3.7"
            results['valid'] = False
        
        # Check runtime dependencies (skip built-in modules)
        for dep in cls.DEPENDENCIES['runtime']:
            dep_name = dep['name']
            
            # Skip built-in modules
            if dep['version'] == 'builtin':
                results['dependencies']['installed'].append(f"{dep_name} (builtin)")
                continue
            
            # Check if module is installed
            spec = importlib.util.find_spec(dep_name.replace('-', '_'))
            if spec is not None:
                results['dependencies']['installed'].append(f"{dep_name} {dep['version']}")
            else:
                results['dependencies']['missing'].append(f"{dep_name} {dep['version']}")
                results['dependencies']['valid'] = False
                results['valid'] = False
        
        # Generate dependency message
        if results['dependencies']['valid']:
            results['dependencies']['message'] = f"✅ All {len(results['dependencies']['installed'])} dependencies are installed"
        else:
            missing_count = len(results['dependencies']['missing'])
            results['dependencies']['message'] = f"❌ {missing_count} dependencies are missing: {', '.join(results['dependencies']['missing'])}"
        
        return results
    
    @classmethod
    def generate_requirements(cls):
        """
        Automatically detect runtime dependencies and generate requirements.txt file.
        
        Returns:
            tuple: (success: bool, message: str, filename: str)
        """
        import os
        
        try:
            requirements_file = 'requirements.txt'
            
            with open(requirements_file, 'w') as f:
                # Header
                f.write("# Playlist Manager - Runtime Dependencies\n")
                f.write("# Auto-generated by POM.py\n\n")
                
                # Write runtime dependencies (skip built-in modules)
                f.write("# Runtime Dependencies\n")
                for dep in cls.DEPENDENCIES['runtime']:
                    if dep['version'] != 'builtin':
                        f.write(f"{dep['name']}=={dep['version']}\n")
                
                # Write testing dependencies
                f.write("\n# Testing Dependencies\n")
                for dep in cls.DEPENDENCIES['testing']:
                    if dep['version'] != 'builtin':
                        f.write(f"{dep['name']}=={dep['version']}\n")
                
                # Write development dependencies
                f.write("\n# Development Dependencies\n")
                for dep in cls.DEPENDENCIES['development']:
                    if dep['version'] != 'builtin':
                        f.write(f"{dep['name']}\n")
            
            abs_path = os.path.abspath(requirements_file)
            return True, f"Requirements file generated successfully with {len(cls.DEPENDENCIES['runtime'])} runtime dependencies", abs_path
        
        except Exception as e:
            return False, f"Failed to generate requirements file: {str(e)}", None


if __name__ == "__main__":
    print(POMConfig.get_info())
    
    # Run environment validation
    print("\n" + "="*50)
    print("🔍 Environment Validation")
    print("="*50)
    
    validation = POMConfig.validate_environment()
    print(f"\n{validation['python_version']['message']}")
    print(f"{validation['dependencies']['message']}")
    
    if validation['valid']:
        print("\n✅ Environment is valid and ready!")
    else:
        print("\n❌ Environment validation failed. Please fix the issues above.")
    
    # Generate requirements.txt
    print("\n" + "="*50)
    print("📝 Generating Requirements File")
    print("="*50)
    
    success, message, filepath = POMConfig.generate_requirements()
    print(f"\n{message}")
    if success:
        print(f"File location: {filepath}")