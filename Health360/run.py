"""
Health360 Execution Launcher
Convenience script to start the Health360 web analytics server.
"""

import sys
import os

# Ensure current folder is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 70)
    print("  HEALTH360: COMPREHENSIVE HEALTHCARE RISK & DISEASE ANALYSIS")
    print("  Healthcare Analytics Platform Server Active")
    print("=" * 70)
    print(f"  Access local application at: http://127.0.0.1:{port}")
    print("  Press Ctrl+C to terminate the development server.")
    print("=" * 70)
    app.run(host='127.0.0.1', port=port, debug=False)
