# 🕒 Mickey Mouse Clock

An interactive analog clock application built with Pygame that uses Mickey Mouse's iconic hands to display system time.

## Features
- **Real-time Sync**: Synchronizes perfectly with your local system time.
- **Smooth Rotation**: Uses custom rotation logic to ensure hands rotate around Mickey's "shoulder" rather than the center of the image.
- **Dynamic Display**: Updates every second to maintain accuracy.

## How it Works
The application calculates rotation angles using the following logic:
- **Seconds**: $6^\circ$ per second.
- **Minutes**: $6^\circ$ per minute + offset for seconds.
- **Hours**: $30^\circ$ per hour + offset for minutes.

## Requirements
- Python 3.x
- Pygame

## Controls
- **ESC / Close Window**: Exit the application.