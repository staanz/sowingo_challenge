#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sowingo Microservices Flask application entry point.

:copyright: (c) 2020 by Sowingo.com Corp.
"""

#
# This is the entry point of the microservice and kickstarts the Flask
# Application by calling the :method:`run_manage_py`.
#
if __name__ == '__main__':
    from api import run_manage_py
    run_manage_py()
