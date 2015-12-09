#!/usr/bin/env python
"""
Author: Rajat Gupta
"""

from beacons import app
import uuid


if __name__ == '__main__':
    app.secret_key = str(uuid.uuid4())
    app.run(debug=True)
