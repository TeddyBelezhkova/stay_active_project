# Stay Active — Corporate Activity Tracker

A full-stack Django web application designed to encourage physical activity, promote team engagement, and foster friendly competition across corporate departments.

Built as an individual project for the **SoftUni Django Basics** course (October 2026).

---

## Key Features

- **Workspace Dashboard**: Live stats tracking active participants, departments, logged workouts, and real-time awarded badge counts calculated from relational models.
- **Activity Logging (Full CRUD)**:
  - Log workouts with activity types, distances, dates, optional notes, proof photos, and privacy toggles.
  - Custom validation preventing future-dated entries.
  - Form field security locking participant re-assignment on edit (`disabled=True`).
  - Real-time 400ms debounced search by participant name/notes alongside activity type filtering.
- **Badge Showcase (Full CRUD)**:
  - Create, view, edit, and delete milestone badges.
  - Award badges directly to colleagues with instant profile updates.
  - Dedicated delete confirmation safeguard.
- **Fame Board & Social Feed**:
  - Live community feed displaying public workouts.
  - Quick reactions and comment cheers with duplicate prevention.
- **Custom Template Filters**:
  - `format_effort`: Standardized distance and unit formatting.
  - `workout_intensity`: Automated calculation of session intensity (Light, Moderate, High, Ultra Endurance).
- **Custom Error Handling**:
  - Branded, user-friendly `404 Not Found` page matching the application UI.

---

## Architecture & Tech Stack

- **Backend**: Python 3.11+, Django 5.x
- **Database**: SQLite (as per Django-Basics-Project-Requirements-Regular-Exam)
- **Frontend**: Custom responsive 3D slate neutral theme, CSS modern variables, vanilla JS debouncing
- **Apps Structure**:
  - `common`: Landing page, how-it-works guidelines, global navigation.
  - `participants`: Participant profiles, department hierarchies, and leaderboard metrics.
  - `activities`: Workout logging, badge catalog, social feed, reactions, comments, and custom template tags.

---

## Installation & Local Setup

The application is fully runnable using the default configuration and an empty database without any fixture scripts.

### 1. Clone the repository
```bash
git clone https://github.com/TeddyBelezhkova/stay_active_project.git
cd django_basics_project