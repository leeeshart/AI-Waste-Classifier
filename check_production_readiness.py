#!/usr/bin/env python3
"""
Production Readiness Checker for EcoSort AI Waste Classifier
Validates that the application is ready for production deployment
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path


class ProductionReadinessChecker:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed_checks = []
        
    def add_error(self, message):
        self.errors.append(f"❌ {message}")
        
    def add_warning(self, message):
        self.warnings.append(f"⚠️  {message}")
        
    def add_success(self, message):
        self.passed_checks.append(f"✅ {message}")
    
    def check_python_version(self):
        """Check Python version is compatible"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.add_error(f"Python 3.8+ required, found {version.major}.{version.minor}")
        else:
            self.add_success(f"Python version {version.major}.{version.minor}.{version.micro}")
    
    def check_required_files(self):
        """Check that required files exist"""
        required_files = [
            'app_production.py',
            'config.py', 
            'security.py',
            'requirements.txt',
            'Dockerfile.backend',
            'Dockerfile.frontend',
            'docker-compose.yml',
            'nginx.conf',
            'deploy.sh'
        ]
        
        for file in required_files:
            if os.path.exists(file):
                self.add_success(f"Required file exists: {file}")
            else:
                self.add_error(f"Missing required file: {file}")
    
    def check_configuration(self):
        """Check configuration validity"""
        try:
            # Store original environment
            original_env = dict(os.environ)
            
            # Manually load production environment variables since dotenv might not be available
            if os.path.exists('.env.production'):
                with open('.env.production', 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key] = value
            
            # Test production config - force reload module to pick up new env vars
            os.environ['FLASK_ENV'] = 'production'
            
            # Remove cached module to force reload
            import sys
            if 'config' in sys.modules:
                del sys.modules['config']
            
            spec = importlib.util.spec_from_file_location("config", "config.py")
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            
            config = config_module.get_config()
            status = config.validate()
            
            if status['valid']:
                self.add_success("Configuration validation passed")
            else:
                for error in status['errors']:
                    self.add_error(f"Configuration error: {error}")
                    
            for warning in status['warnings']:
                self.add_warning(f"Configuration warning: {warning}")
            
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)
                
        except Exception as e:
            self.add_error(f"Configuration loading failed: {e}")
            # Restore original environment on error
            if 'original_env' in locals():
                os.environ.clear()
                os.environ.update(original_env)
    
    def check_security_modules(self):
        """Check security modules can be imported"""
        try:
            spec = importlib.util.spec_from_file_location("security", "security.py")
            security_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(security_module)
            
            # Test critical functions exist
            required_functions = [
                'rate_limit', 'require_api_key', 'validate_file',
                'sanitize_text_input', 'create_error_response', 'create_success_response'
            ]
            
            for func_name in required_functions:
                if hasattr(security_module, func_name):
                    self.add_success(f"Security function available: {func_name}")
                else:
                    self.add_error(f"Missing security function: {func_name}")
                    
        except Exception as e:
            self.add_error(f"Security module loading failed: {e}")
    
    def check_environment_files(self):
        """Check environment configuration files"""
        if os.path.exists('.env.example'):
            self.add_success("Environment example file exists")
        else:
            self.add_warning("No .env.example file found")
            
        if os.path.exists('.env.production'):
            self.add_success("Production environment file exists")
            
            # Check for default values that should be changed
            with open('.env.production', 'r') as f:
                content = f.read()
                
            if 'your-production-secret-key-here' in content:
                self.add_error("Production secret key not changed from default")
            elif 'dev-secret-key' in content:
                self.add_error("Using development secret key in production")
            else:
                self.add_success("Production secret key appears to be customized")
                
            if 'your-production-api-key-here' in content:
                self.add_warning("Production API key not changed from default")
            else:
                self.add_success("Production API key appears to be customized")
                
        else:
            self.add_warning("No .env.production file found - run generate_production_config.py")
    
    def check_docker_configuration(self):
        """Check Docker configuration validity"""
        # Check Dockerfile.backend
        if os.path.exists('Dockerfile.backend'):
            with open('Dockerfile.backend', 'r') as f:
                dockerfile_content = f.read()
                
            if 'gunicorn' in dockerfile_content:
                self.add_success("Dockerfile.backend uses gunicorn for production")
            else:
                self.add_warning("Dockerfile.backend may not use production WSGI server")
                
            if 'HEALTHCHECK' in dockerfile_content:
                self.add_success("Dockerfile.backend includes health check")
            else:
                self.add_warning("Dockerfile.backend missing health check")
        
        # Check docker-compose.yml
        if os.path.exists('docker-compose.yml'):
            with open('docker-compose.yml', 'r') as f:
                compose_content = f.read()
                
            services = ['frontend', 'backend', 'nginx', 'redis', 'postgres']
            for service in services:
                if service in compose_content:
                    self.add_success(f"Docker compose includes {service} service")
                else:
                    self.add_warning(f"Docker compose missing {service} service")
    
    def check_security_headers(self):
        """Check nginx security configuration"""
        if os.path.exists('nginx.conf'):
            with open('nginx.conf', 'r') as f:
                nginx_content = f.read()
                
            security_headers = [
                'X-Frame-Options',
                'X-XSS-Protection', 
                'X-Content-Type-Options',
                'Content-Security-Policy'
            ]
            
            for header in security_headers:
                if header in nginx_content:
                    self.add_success(f"Nginx includes security header: {header}")
                else:
                    self.add_warning(f"Nginx missing security header: {header}")
        else:
            self.add_error("nginx.conf file not found")
    
    def check_deployment_script(self):
        """Check deployment script"""
        if os.path.exists('deploy.sh'):
            if os.access('deploy.sh', os.X_OK):
                self.add_success("Deployment script is executable")
            else:
                self.add_warning("Deployment script exists but is not executable")
        else:
            self.add_error("deploy.sh script not found")
            
        if os.path.exists('start_backend.sh'):
            if os.access('start_backend.sh', os.X_OK):
                self.add_success("Backend start script is executable")
            else:
                self.add_warning("Backend start script exists but is not executable")
    
    def check_gitignore(self):
        """Check .gitignore configuration"""
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r') as f:
                gitignore_content = f.read()
                
            important_entries = ['.env', 'logs/', '*.log', '__pycache__/', 'node_modules/']
            for entry in important_entries:
                if entry in gitignore_content:
                    self.add_success(f"Gitignore includes: {entry}")
                else:
                    self.add_warning(f"Gitignore missing: {entry}")
        else:
            self.add_warning(".gitignore file not found")
    
    def run_all_checks(self):
        """Run all production readiness checks"""
        print("🔍 EcoSort Production Readiness Check")
        print("=" * 50)
        
        self.check_python_version()
        self.check_required_files()
        self.check_configuration()
        self.check_security_modules()
        self.check_environment_files()
        self.check_docker_configuration()
        self.check_security_headers()
        self.check_deployment_script()
        self.check_gitignore()
        
        self.print_results()
        
        return len(self.errors) == 0
    
    def print_results(self):
        """Print check results"""
        print("\n📊 Results Summary:")
        print(f"✅ Passed: {len(self.passed_checks)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print(f"❌ Errors: {len(self.errors)}")
        
        if self.passed_checks:
            print("\n✅ Passed Checks:")
            for check in self.passed_checks:
                print(f"  {check}")
        
        if self.warnings:
            print("\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if self.errors:
            print("\n❌ Errors:")
            for error in self.errors:
                print(f"  {error}")
        
        print("\n" + "=" * 50)
        
        if self.errors:
            print("❌ Production readiness check FAILED")
            print("Please fix the errors above before deploying to production.")
        elif self.warnings:
            print("⚠️  Production readiness check PASSED with warnings")
            print("Consider addressing the warnings for better security and reliability.")
        else:
            print("✅ Production readiness check PASSED")
            print("Application appears ready for production deployment!")


def main():
    checker = ProductionReadinessChecker()
    success = checker.run_all_checks()
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())