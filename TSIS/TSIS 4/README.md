# TSIS 4 Snake Game

Run:
```bash
pip install pygame psycopg2-binary
python3 main.py
```

Default database: `tsis4`. If PostgreSQL asks for password, write it in `config.py` → `DB_PASSWORD`.

Completed: PostgreSQL tables, username entry, auto-save, Top 10 leaderboard, personal best during gameplay, weighted timed food, poison food (-2 segments), speed/slow/shield power-ups, level 3 obstacles, JSON settings, all four screens.

Snake PNG files are not used. Snake is drawn fully with selected color. Food image `assets/images/apple.png` is kept.
