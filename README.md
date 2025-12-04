# PyCTSS — Centralized Terminal Session System

A lightweight Python CLI tool that emulates classic terminal-service behavior over LAN, inspired by CTSS and early Microsoft Terminal Services/RDS.

## Usage
- Enusre python is installed and available on SYS/USER Path
- Manually run `main.py`
- On windows you can use the `start.bat`, which will create a python venv, install dependencies and run the app

## Features
- File operations (CRUD)
- Client-to-client file sharing
- Real-time messaging
- LAN-based connectivity
- Multi-client support
- Clean, minimal CLI interface

## Limitations
- Basic authentication and security
- Messaging not fully simultaneous

## Improvements
- DNS-style middleware so clients don’t depend on the server’s raw address
- Cross-platform testing beyond Windows
- Separate client and server apps
- Fix items listed under limitations
- Add client-side caching to reduce server load

## Screenshots
<table>
  <tr>
    <td><img src="/assets/screenshots/img1.png" alt="SS1" width="500"></td>
    <td><img src="/assets/screenshots/img2.png" alt="SS2" width="500"></td>
  </tr>
  <tr>
    <td><img src="/assets/screenshots/img3.png" alt="SS3" width="500"></td>
    <td><img src="/assets/screenshots/img4.png" alt="SS4" width="500"></td>
  </tr>
  <tr>
    <td><img src="/assets/screenshots/img5.png" alt="SS5" width="500"></td>
    <td><img src="/assets/screenshots/img6.png" alt="SS6" width="500"></td>
  </tr>
</table>

## Learned
- Fundamentals of TCP/UDP networking
- Socket programming and data flow across network streams
- Basic multithreading
- Designing a custom protocol and why protocols matter
- Common security risks for internet-connected devices
- Different client–server communication models and their tradeoffs
