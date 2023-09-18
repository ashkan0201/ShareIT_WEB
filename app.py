# Required library
import os
import sqlite3
import werkzeug.utils
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime
from glob2 import glob
