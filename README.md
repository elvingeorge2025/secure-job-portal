# Secure Job Posting & Recruitment Portal

A demo secure web application built with **Flask**, **Python**, and **MySQL**.

## Overview

This application allows:

- Applicants to register, log in, search jobs, and apply with a PDF CV.
- Recruiters (admins) to create, edit, delete jobs and view applicants.

Security features include:

- Secure password hashing (bcrypt)
- CSRF protection (Flask-WTF)
- Parameterized SQL queries (MySQL)
- Input validation and sanitization
- Role-based access control
- Secure PDF-only file uploads
- Audit logging for critical actions

## Project Structure

See the provided folder tree in your assignment (mirrored in this repo).

## Setup

1. Create virtual environment and install dependencies:

```bash
pip install -r requirements.txt
